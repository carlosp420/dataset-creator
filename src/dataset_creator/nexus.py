from .utils import get_seq


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
    - codon_positions
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
    """
    def __init__(self, data, codon_positions=None):
        self.data = data
        self.codon_positions = codon_positions
        self.charset_block = self.make_charset_block()
        self.partition_line = self.make_partition_line()

    def make_charset_block(self):
        out = 'begin mrbayes;\n'
        count = 1
        for gene_code, lengths in self.data.gene_codes_and_lengths.items():
            gene_length = lengths[0] + count - 1
            formatted_gene_code = self.format_with_codon_positions(gene_code)
            out += '    charset {0} = {1}-{2};\n'.format(formatted_gene_code, count, gene_length)
            count = gene_length + 1
        return out.strip()

    def format_with_codon_positions(self, gene_code):
        """Appends pos1, pos2, etc to the gene_code if needed."""
        sufixes = {
            '1st': '_pos1',
            '2nd': '_pos2',
            '3rd': '_pos3',
            '1st-2nd': '_pos12',
            'ALL': '',
        }
        return '{0}{1}'.format(gene_code, sufixes[self.codon_positions])

    def make_partition_line(self):
        out = 'partition GENES = {0}: '.format(len(self.data.gene_codes))
        out += ', '.join(self.data.gene_codes)
        out += ';'
        out += '\n\nset partition = GENES;'
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
