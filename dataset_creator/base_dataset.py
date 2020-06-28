import re
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from .utils import get_seq


class DatasetBlock(object):
    """
    By default, the data sequences block generated is NEXUS and we use BioPython
    tools to convert it to other formats such as FASTA.
    However, sometimes the blo

    Parameters:
        data (named tuple):      containing:
                                  * gene_codes: list
                                  * number_chars: string
                                  * number_taxa: string
                                  * seq_records: list of SeqRecordExpanded objects
                                  * gene_codes_and_lengths: OrderedDict
        codon_positions (str):   str. Can be 1st, 2nd, 3rd, 1st-2nd, ALL (default).
        partitioning (str):
        aminoacids (boolean):
        degenerate (str):
        format (str):       NEXUS, PHYLIP or FASTA.
        outgroup (str):     Specimen code of taxon that should be used as outgroup.
    """
    def __init__(self, data, codon_positions, partitioning, aminoacids=None,
                 degenerate=None, format=None, outgroup=None):
        self.warnings = []
        self.data = data
        self.codon_positions = codon_positions
        self.partitioning = partitioning
        self.aminoacids = aminoacids
        self.degenerate = degenerate
        self.format = format
        self.outgroup = outgroup
        self._blocks = []

    def dataset_block(self):
        """Creates the block with taxon names and their sequences.

        Override this function if the dataset block needs to be different
        due to file format.

        Example:

            CP100_10_Aus_aus   ACGATRGACGATRA...
            CP100_11_Aus_bus   ACGATRGACGATRA...
            ...

        """
        self.split_data()
        out = []
        for block in self._blocks:
            out.append(self.convert_to_string(block))
        return '\n'.join(out).strip() + '\n;\nEND;'

    def split_data(self):
        """Splits the list of SeqRecordExpanded objects into lists, which are
        kept into a bigger list.

        If the file_format is Nexus, then it is only partitioned by gene. If it
        is FASTA, then it needs partitioning by codon positions if required.

        Example:

            >>> blocks = [
            ...     [SeqRecord1, SeqRecord2],  # for gene 1
            ...     [SeqRecord1, SeqRecord2],  # for gene 2
            ...     [SeqRecord1, SeqRecord2],  # for gene 3
            ...     [SeqRecord1, SeqRecord2],  # for gene 4
            ... ]

        """
        this_gene_code = None
        for seq_record in self.data.seq_records:
            if this_gene_code is None or this_gene_code != seq_record.gene_code:
                this_gene_code = seq_record.gene_code
                self._blocks.append([])
            list_length = len(self._blocks)
            self._blocks[list_length - 1].append(seq_record)

    def convert_to_string(self, block):
        """Makes gene_block as str from list of SeqRecordExpanded objects of a gene_code.

        Override this function if the dataset block needs to be different
        due to file format.

        This block will need to be split further if the dataset is FASTA or
        TNT and the partitioning scheme is 1st-2nd, 3rd.

        As the dataset is split into several blocks due to 1st-2nd, 3rd
        we cannot translate to aminoacids or degenerate the sequences.

        """
        if self.partitioning != '1st-2nd, 3rd':
            return self.make_datablock_by_gene(block)
        else:
            if self.format == 'FASTA':
                return self.make_datablock_considering_codon_positions_as_fasta_format(block)
            else:
                return self.make_datablock_by_gene(block)

    def make_datablock_considering_codon_positions_as_fasta_format(self, block):
        block_1st2nd = OrderedDict()
        block_1st = OrderedDict()
        block_2nd = OrderedDict()
        block_3rd = OrderedDict()

        for seq_record in block:  # splitting each block in two
            if seq_record.gene_code not in block_1st2nd:
                block_1st2nd[seq_record.gene_code] = []
            if seq_record.gene_code not in block_1st:
                block_1st[seq_record.gene_code] = []
            if seq_record.gene_code not in block_2nd:
                block_2nd[seq_record.gene_code] = []
            if seq_record.gene_code not in block_3rd:
                block_3rd[seq_record.gene_code] = []

            taxonomy_as_string = self.flatten_taxonomy(seq_record)
            taxon_id = '>{0}{1}'.format(seq_record.voucher_code,
                                        taxonomy_as_string)
            block_1st2nd[seq_record.gene_code].append('{0}\n{1}\n'.format(taxon_id,
                                                                          seq_record.first_and_second_codon_positions()))
            block_1st[seq_record.gene_code].append('{0}\n{1}\n'.format(taxon_id,
                                                                       seq_record.first_codon_position()))
            block_2nd[seq_record.gene_code].append('{0}\n{1}\n'.format(taxon_id,
                                                                       seq_record.second_codon_position()))
            block_3rd[seq_record.gene_code].append('{0}\n{1}\n'.format(taxon_id,
                                                                       seq_record.third_codon_position()))
        out = self.convert_block_dicts_to_string(block_1st2nd, block_1st, block_2nd, block_3rd)
        return out

    def convert_block_dicts_to_string(self, block_1st2nd, block_1st, block_2nd, block_3rd):
        """Takes into account whether we need to output all codon positions."""
        out = ""
        # We need 1st and 2nd positions
        if self.codon_positions in ['ALL', '1st-2nd']:
            for gene_code, seqs in block_1st2nd.items():
                out += '>{0}_1st-2nd\n----\n'.format(gene_code)
                for seq in seqs:
                    out += seq
        elif self.codon_positions == '1st':
            for gene_code, seqs in block_1st.items():
                out += '>{0}_1st\n----\n'.format(gene_code)
                for seq in seqs:
                    out += seq
        elif self.codon_positions == '2nd':
            for gene_code, seqs in block_2nd.items():
                out += '>{0}_2nd\n----\n'.format(gene_code)
                for seq in seqs:
                    out += seq

        # We also need 3rd positions
        if self.codon_positions in ['ALL', '3rd']:
            for gene_code, seqs in block_3rd.items():
                out += '\n>{0}_3rd\n----\n'.format(gene_code)
                for seq in seqs:
                    out += seq
        return out

    def make_datablock_by_gene(self, block):
        out = None
        max_taxon_id = 0
        for seq_record in block:
            taxon_id = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                            seq_record.taxonomy.get('genus', ''),
                                            seq_record.taxonomy.get('species', ''),
                                            )
            if len(taxon_id) > max_taxon_id:
                max_taxon_id = len(taxon_id)

        pad_number = max_taxon_id + 1
        if pad_number < 55:
            pad_number = 55

        for seq_record in block:
            if not out:
                out = '[{0}]\n'.format(seq_record.gene_code)
            taxonomy_as_string = self.flatten_taxonomy(seq_record)
            taxon_id = '{0}{1}'.format(seq_record.voucher_code,
                                       taxonomy_as_string)

            sequence = get_seq(seq_record, self.codon_positions,
                               aminoacids=self.aminoacids,
                               degenerate=self.degenerate)
            seq = sequence.seq
            if sequence.warning:
                self.warnings.append(sequence.warning)

            out += '{0}{1}\n'.format(taxon_id.ljust(pad_number), seq)
        return out

    def flatten_taxonomy(self, seq_record):
        out = ''
        if seq_record.taxonomy is None:
            return out
        else:
            try:
                out += "_" + seq_record.taxonomy['orden']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['superfamily']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['family']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['subfamily']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['tribe']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['subtribe']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['genus']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['species']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['subspecies']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['author']
            except KeyError:
                pass
            try:
                out += "_" + seq_record.taxonomy['hostorg']
            except KeyError:
                pass
            out = out.replace(" ", "_")
            out = re.sub("_$", "", out)
            return re.sub('_+', '_', out)


class DatasetFooter(object):
    """Builds charset block:

    Parameters:
        data (namedtuple):      with necessary info for dataset creation.
        codon_positions (str):  `1st`, `2nd`, `3rd`, `1st-2nd`, `ALL`.
        partitioning (str):     `by gene`, `by codon position`, `1st-2nd, 3rd`.
        outgroup (str):         voucher code to be used as outgroup for NEXUS
                                and TNT files.

    Example:

        >>>
        begin mrbayes;
        charset ArgKin = 1-596;
        charset COI-begin = 597-1265;
        charset COI_end = 1266-2071;
        charset ef1a = 2072-3311;
        charset RpS2 = 3312-3722;
        charset RpS5 = 3723-4339;
        charset wingless = 4340-4739;
        set autoclose=yes;
        prset applyto=(all) ratepr=variable brlensp=unconstrained:Exp(100.0) shapepr=exp(1.0) tratiopr=beta(2.0,1.0);
        lset applyto=(all) nst=mixed rates=gamma [invgamma];
        unlink statefreq=(all);
        unlink shape=(all) revmat=(all) tratio=(all) [pinvar=(all)];
        mcmc ngen=10000000 printfreq=1000 samplefreq=1000 nchains=4 nruns=2 savebrlens=yes [temp=0.11];
         sump relburnin=yes [no] burninfrac=0.25 [2500];
         sumt relburnin=yes [no] burninfrac=0.25 [2500] contype=halfcompat [allcompat];
        END;

    """
    def __init__(self, data, codon_positions=None, partitioning=None,
                 outgroup=None):
        self.data = data
        self.codon_positions = codon_positions
        self.partitioning = partitioning
        self.outgroup = outgroup

        self._validate_partitioning(partitioning)
        self._validate_codon_positions(codon_positions)
        self.charset_block = self.make_charset_block()
        self.partition_line = self.make_partition_line()

    def _validate_partitioning(self, partitioning):
        if partitioning is None:
            self.partitioning = 'by gene'
        elif partitioning not in ['by gene', 'by codon position', '1st-2nd, 3rd']:
            raise AttributeError("Partitioning parameter should be one of these: "
                                 "None, 'by gene', 'by codon position', '1st-2nd, 3rd")

    def _validate_codon_positions(self, codon_positions):
        if codon_positions is None:
            self.codon_positions = 'ALL'
        elif codon_positions not in ['1st', '2nd', '3rd', '1st-2nd', 'ALL']:
            raise AttributeError("Codon positions parameter should be one of these: "
                                 "None, '1st', '2nd', '3rd', '1st-2nd', 'ALL'")

    def make_charset_block(self):
        """
        Override this function for Phylip dataset as the content is different and
        goes into a separate file.
        """
        out = 'begin mrbayes;\n'
        out += self.make_charsets()
        return out.strip()

    def make_charsets(self):
        """
        Override this function for Phylip dataset as the content is different and
        goes into a separate file.
        """
        count_start = 1
        out = ''
        for gene_code, lengths in self.data.gene_codes_and_lengths.items():
            count_end = lengths[0] + count_start - 1
            out += self.format_charset_line(gene_code, count_start, count_end)
            count_start = count_end + 1
        return out

    def format_charset_line(self, gene_code, count_start, count_end):
        slash_number = self.make_slash_number()
        suffixes = self.make_gene_code_suffixes()
        corrected_count = self.correct_count_using_reading_frames(gene_code, count_start, count_end)

        out = ''
        for index, val in enumerate(suffixes):
            out += '    charset {0}{1} = {2}{3};\n'.format(gene_code, suffixes[index],
                                                           corrected_count[index], slash_number)
        return out

    def make_slash_number(self):
        """
        Charset lines have \2 or \3 depending on type of partitioning and codon
        positions requested for our dataset.

        :return:
        """
        if self.partitioning == 'by codon position' and self.codon_positions == '1st-2nd':
            return '\\2'
        elif self.partitioning in ['by codon position', '1st-2nd, 3rd'] and self.codon_positions in ['ALL', None]:
            return '\\3'
        else:
            return ''

    def make_gene_code_suffixes(self):
        try:
            return self.suffix_for_one_codon_position()
        except KeyError:
            return self.suffix_for_several_codon_positions()

    def suffix_for_one_codon_position(self):
        sufixes = {
            '1st': '_pos1',
            '2nd': '_pos2',
            '3rd': '_pos3',
        }
        return [sufixes[self.codon_positions]]

    def suffix_for_several_codon_positions(self):
        if self.codon_positions == 'ALL' and self.partitioning == 'by gene':
            return ['']
        elif self.codon_positions == '1st-2nd' and self.partitioning in ['by gene', '1st-2nd, 3rd']:
            return ['_pos12']
        elif self.codon_positions == '1st-2nd' and self.partitioning == 'by codon position':
            return ['_pos1', '_pos2']

        if self.partitioning == 'by codon position':
            return ['_pos1', '_pos2', '_pos3']
        elif self.partitioning == '1st-2nd, 3rd':
            return ['_pos12', '_pos3']

    def correct_count_using_reading_frames(self, gene_code, count_start, count_end):
        reading_frame = self.data.reading_frames[gene_code]
        bp = BasePairCount(reading_frame, self.codon_positions, self.partitioning, count_start, count_end)
        return bp.get_corrected_count()

    def make_partition_line(self):
        out = 'partition GENES = {0}: '.format(len(self.data.gene_codes) * len(self.make_gene_code_suffixes()))
        out += ', '.join(self.add_suffixes_to_gene_codes())
        out += ';'
        out += '\n\nset partition = GENES;'
        return out

    def add_suffixes_to_gene_codes(self):
        """Appends pos1, pos2, etc to the gene_code if needed."""
        out = []
        for gene_code in self.data.gene_codes:
            for sufix in self.make_gene_code_suffixes():
                out.append('{0}{1}'.format(gene_code, sufix))
        return out

    def dataset_footer(self):
        return self.make_footer()

    def make_footer(self):
        outgroup = self.get_outgroup()

        footer = """{0}\n{1}

set autoclose=yes;{2}
prset applyto=(all) ratepr=variable brlensp=unconstrained:Exp(100.0) shapepr=exp(1.0) tratiopr=beta(2.0,1.0);
lset applyto=(all) nst=mixed rates=gamma [invgamma];
unlink statefreq=(all);
unlink shape=(all) revmat=(all) tratio=(all) [pinvar=(all)];
mcmc ngen=10000000 printfreq=1000 samplefreq=1000 nchains=4 nruns=2 savebrlens=yes [temp=0.11];
 sump relburnin=yes [no] burninfrac=0.25 [2500];
 sumt relburnin=yes [no] burninfrac=0.25 [2500] contype=halfcompat [allcompat];
END;
    """.format(self.charset_block, self.partition_line, outgroup)
        return footer.strip()

    def get_outgroup(self):
        """Generates the outgroup line from the voucher code specified by the
        user.
        """
        if self.outgroup is not None:
            outgroup_taxonomy = ''
            for i in self.data.seq_records:
                if self.outgroup == i.voucher_code:
                    outgroup_taxonomy = '{0}_{1}'.format(i.taxonomy['genus'],
                                                         i.taxonomy['species'])
                    break
            outgroup = '\noutgroup {0}_{1};'.format(self.outgroup,
                                                    outgroup_taxonomy)
        else:
            outgroup = ''
        return outgroup


class BasePairCount(object):
    """
    Uses reading frame info, partitioning method and number of codon positions
    to return corrected base pair count for charset lines.

    Example:

        >>> bp_count = BasePairCount(reading_frame=1, codon_positions='1st-2nd',
        ...                          partitioning='by codon position',
        ...                          count_start=100, count_end=512)
        >>> bp_count.get_corrected_count()
        [
            '100-512',
            '101-513',
        ]
    """
    def __init__(self, reading_frame=None, codon_positions=None, partitioning=None,
                 count_start=None, count_end=None):
        self._partitioning = self._set_partitioning(partitioning)
        self._codon_positions = self._set_codon_positions(codon_positions)
        self._reading_frame = self._set_reading_frame(reading_frame)
        self._count_start = self._set_count_start(count_start)
        self._count_end = self._set_count_end(count_end)

    def _set_codon_positions(self, codon_positions):
        if not codon_positions:
            raise ValueError("_codon_positions argument is needed. Can't be None")
        else:
            return codon_positions

    def _set_reading_frame(self, reading_frame):
        if not reading_frame and self._partitioning in ['by codon position', '1st-2nd, 3rd']:
            raise ValueError("_reading_frame argument is needed. Can't be None")
        else:
            return reading_frame

    def _set_partitioning(self, partitioning):
        if not partitioning:
            raise ValueError("_partitioning argument is needed. Can't be None")
        else:
            return partitioning

    def _set_count_start(self, count_start):
        if not count_start:
            raise ValueError("codon_start argument is needed. Can't be None")
        else:
            return count_start

    def _set_count_end(self, count_end):
        if not count_end:
            raise ValueError("codon_end argument is needed. Can't be None")
        else:
            return count_end

    def get_corrected_count(self):
        if self._codon_positions == '1st-2nd' and self._partitioning in ['by gene',
                                                                         'by codon position',
                                                                         '1st-2nd, 3rd']:
            return self._using_1st2nd_codons()

        if self._codon_positions == 'ALL' and self._partitioning == 'by codon position':
            return self._using_all_codons_partition_by_codon_position()

        if self._codon_positions in ['ALL', '1st', '2nd', '3rd'] and self._partitioning == 'by gene':
            return self._using_all_codons_partition_by_gene()

        if self._codon_positions in ['1st', '2nd', '3rd'] and self._partitioning in ['by codon position', '1st-2nd, 3rd']:
            return self._using_one_codon_position_partitioned_by_codon_position(self._codon_positions)

        if self._codon_positions == 'ALL' and self._partitioning == '1st-2nd, 3rd':
            return self._using_all_codons_partition_by_1st2nd_3rd()

    def _using_1st2nd_codons(self):
        return [
            '{0}-{1}'.format(self._count_start, self._count_end),
            '{0}-{1}'.format(self._count_start + 1, self._count_end),
        ]

    def _using_all_codons_partition_by_codon_position(self):
        if self._reading_frame == 1:
            return [
                '{0}-{1}'.format(self._count_start, self._count_end),
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
            ]

        elif self._reading_frame == 2:
            return [
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
                '{0}-{1}'.format(self._count_start, self._count_end),
            ]

        else:
            return [
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
                '{0}-{1}'.format(self._count_start, self._count_end),
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
            ]

    def _using_one_codon_position_partitioned_by_codon_position(self, position):
        return [
            '{0}-{1}'.format(self._count_start, self._count_end),
        ]

    def _using_all_codons_partition_by_gene(self):
        return [
            '{0}-{1}'.format(self._count_start, self._count_end,)
        ]

    def _using_all_codons_partition_by_1st2nd_3rd(self):
        if self._reading_frame == 1:
            return [
                '{0}-{1}\\3 {2}-{3}'.format(self._count_start, self._count_end,
                                            self._count_start + 1,
                                            self._count_end),
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
            ]

        elif self._reading_frame == 2:
            return [
                '{0}-{1}\\3 {2}-{3}'.format(self._count_start + 1,
                                            self._count_end,
                                            self._count_start + 2,
                                            self._count_end),
                '{0}-{1}'.format(self._count_start, self._count_end),
            ]

        else:
            return [
                '{0}-{1}\\3 {2}-{3}'.format(self._count_start + 2,
                                            self._count_end,
                                            self._count_start,
                                            self._count_end),
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
            ]
