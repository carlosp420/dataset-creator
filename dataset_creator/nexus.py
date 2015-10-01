from .utils import get_seq


class DatasetBlock(object):
    """
    Parameters:
        data (named tuple):      containing:
                                  * gene_codes: list
                                  * number_chars: string
                                  * number_taxa: string
                                  * seq_recods: list of SeqRecordExpanded objetcs
                                  * gene_codes_and_lengths: OrderedDict
        codon_positions (str):   str. Can be 1st, 2nd, 3rd, 1st-2nd, ALL (default).
        partitioning (str):
        aminoacids (boolean):
        degenerate (str):
    """
    def __init__(self, data, codon_positions, partitioning, aminoacids=None,
                 degenerate=None):
        self.warnings = []
        self.data = data
        self.codon_positions = codon_positions
        self.partitioning = partitioning
        self.aminoacids = aminoacids
        self.degenerate = degenerate
        self._blocks = []

    def dataset_block(self):
        self.split_data()
        out = []
        for block in self._blocks:
            out.append(self.convert_to_string(block))
        return '\n'.join(out).strip() + '\n;\nEND;'

    def split_data(self):
        """
        Splits the list of SeqRecordExpanded objects into lists, which are kept into
        a bigger list:

        Example:

            >>> blocks = [
            ...     [SeqRecord1, SeqRecord2],  # for gene 1
            ...     [SeqRecord1, SeqRecord2],  # for gene 2
            ...     [SeqRecord1, SeqRecord2],  # for gene 3
            ...     [SeqRecord1, SeqRecord2],  # for gene 4
            ... ]

        :param data: list of SeqRecordExpanded objects
        :return: list in the variable `self._blocks`
        """
        this_gene_code = None

        for seq_record in self.data.seq_records:
            if this_gene_code is None or this_gene_code != seq_record.gene_code:
                this_gene_code = seq_record.gene_code
                self._blocks.append([])
            list_length = len(self._blocks)
            self._blocks[list_length - 1].append(seq_record)

    def convert_to_string(self, block):
        """
        Takes a list of SeqRecordExpanded objects corresponding to a gene_code
        and produces the gene_block as string.

        :param block:
        :return: str.
        """
        out = None
        for seq_record in block:
            if not out:
                out = '[{0}]\n'.format(seq_record.gene_code)
            taxon_id = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                            seq_record.taxonomy['genus'],
                                            seq_record.taxonomy['species'],
                                            )
            if self.aminoacids is True:
                seq = seq_record.translate()
            elif self.aminoacids is not True and self.degenerate is not None:
                seq = seq_record.degenerate(method=self.degenerate)
            else:
                seq = get_seq(seq_record, self.codon_positions)

            out += '{0}{1}\n'.format(taxon_id.ljust(55), seq)
        return out


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
        "
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
        "
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

        if self._codon_positions in ['1st', '2nd', '3rd'] and self._partitioning == 'by codon position':
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
