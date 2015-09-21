from .utils import get_seq
from .bp_count import BasePairCount


def dataset_header(data):
    """
    :param data: named tuple with necessary info for dataset creation.
    """
    header = """
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX={0} NCHAR={1};
FORMAT INTERLEAVE DATATYPE=DNA MISSING=? GAP=-;
MATRIX
""".format(data.number_taxa, data.number_chars)
    return header.strip()


class DatasetBlock(object):
    """
    Parameters:
        - data      - named tuple containing:
                        * gene_codes: list
                        * number_chars: string
                        * number_taxa: string
                        * seq_recods: list of SeqRecordExpanded objetcs
                        * gene_codes_and_lengths: OrderedDict
        - codon_positions    - str. Can be 1st, 2nd, 3rd, 1st-2nd, ALL (default).
        - partitioning
    """
    def __init__(self, data, codon_positions, partitioning):
        self.data = data
        self.codon_positions = codon_positions
        self.partitioning = partitioning
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
            seq = get_seq(seq_record, self.codon_positions)
            out += '{0}{1}\n'.format(taxon_id.ljust(55), seq)
        return out


class DatasetFooter(object):
    """
    :param data: named tuple with necessary info for dataset creation.
    :param codon_positions: 1st, 2nd, 3rd, 1st-2nd, ALL
    :param partitioning: 'by gene', 'by codon position', '1st-2nd, 3rd'
    """
    def __init__(self, data, codon_positions=None, partitioning=None):
        self.data = data
        self.codon_positions = codon_positions
        self.partitioning = partitioning
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
        out = 'begin mrbayes;\n'
        out += self.make_charsets()
        return out.strip()

    def make_charsets(self):
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
        elif self.codon_positions in [None, 'ALL'] and self.partitioning == 'by gene':
            return ['']

        if self.partitioning == 'by codon position':
            return ['_pos1', '_pos2', '_pos3']
        elif self.partitioning == '1st-2nd, 3rd':
            return 'ArgKing_pos12 \\3   \n  Argking-pos3 \\3'
        else:
            return ['']

    def correct_count_using_reading_frames(self, gene_code, count_start, count_end):
        reading_frame = self.data.reading_frames[gene_code]

        if self.codon_positions == 'ALL' and self.partitioning == 'by codon position':
            if reading_frame == 1:
                return self.fix_count_for_reading_frame1(count_start, count_end)
            elif reading_frame == 2:
                return self.fix_count_for_reading_frame2(count_start, count_end)
            else:
                return self.fix_count_for_reading_frame3(count_start, count_end)

        if self.codon_positions in ['ALL', '1st', '2nd', '3rd'] and self.partitioning == 'by gene':
            return ['{0}-{1}'.format(count_start, count_end)]

        if self.codon_positions == '1st-2nd' and self.partitioning in ['by gene', '1st-2nd, 3rd']:
            return ['{0}-{1}'.format(count_start, count_end)]

        if self.codon_positions == '1st-2nd' and self.partitioning == 'by codon position':
            bp = BasePairCount(reading_frame, self.codon_positions, self.partitioning, count_start, count_end)
            return bp.get_corrected_count()

    def fix_count_for_reading_frame1(self, count_start, count_end):
        return [
            '{0}-{1}'.format(count_start, count_end),
            '{0}-{1}'.format(count_start + 1, count_end),
            '{0}-{1}'.format(count_start + 2, count_end),
        ]

    def fix_count_for_reading_frame2(self, count_start, count_end):
        return [
            '{0}-{1}'.format(count_start + 1, count_end),
            '{0}-{1}'.format(count_start + 2, count_end),
            '{0}-{1}'.format(count_start, count_end),
        ]

    def fix_count_for_reading_frame3(self, count_start, count_end):
        return [
            '{0}-{1}'.format(count_start + 2, count_end),
            '{0}-{1}'.format(count_start, count_end),
            '{0}-{1}'.format(count_start + 1, count_end),
        ]

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
        footer = """{0}\n{1}

set autoclose=yes;
prset applyto=(all) ratepr=variable brlensp=unconstrained:Exp(100.0) shapepr=exp(1.0) tratiopr=beta(2.0,1.0);
lset applyto=(all) nst=mixed rates=gamma [invgamma];
unlink statefreq=(all);
unlink shape=(all) revmat=(all) tratio=(all) [pinvar=(all)];
mcmc ngen=10000000 printfreq=1000 samplefreq=1000 nchains=4 nruns=2 savebrlens=yes [temp=0.11];
 sump relburnin=yes [no] burninfrac=0.25 [2500];
 sumt relburnin=yes [no] burninfrac=0.25 [2500] contype=halfcompat [allcompat];
END;
    """.format(self.charset_block, self.partition_line)
        return footer.strip()
