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
    """
    def __init__(self, data, partitioning):
        self.data = data
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
                print(seq_record.gene_code)
                out = '[{0}]\n'.format(seq_record.gene_code)
            taxon_id = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                            seq_record.taxonomy['genus'],
                                            seq_record.taxonomy['species'],
                                            )
            out += '{0}{1}\n'.format(taxon_id.ljust(55), seq_record.seq)
        return out


class DatasetFooter(object):
    """
    :param data: named tuple with necessary info for dataset creation.
    """
    def __init__(self, data, gene_codes_and_lengths):
        self.data = data
        self.gene_codes_and_lengths = gene_codes_and_lengths
        print(">>>>", gene_codes_and_lengths)

    def make_charset_block(self):
        out = ''

    def make_footer(self):
        footer = """
begin mrbayes;
    charset ArgKin = 1-596;
    charset COI-begin = 597-1265;
    charset COI_end = 1266-2071;
    charset ef1a = 2072-3311;
    charset RpS2 = 3312-3722;
    charset RpS5 = 3723-4339;
    charset wingless = 4340-4739;
partition GENES = 7: ArgKin, COI-begin, COI_end, ef1a, RpS2, RpS5, wingless;

set partition = GENES;

set autoclose=yes;
prset applyto=(all) ratepr=variable brlensp=unconstrained:Exp(100.0) shapepr=exp(1.0) tratiopr=beta(2.0,1.0);
lset applyto=(all) nst=mixed rates=gamma [invgamma];
unlink statefreq=(all);
unlink shape=(all) revmat=(all) tratio=(all) [pinvar=(all)];
mcmc ngen=10000000 printfreq=1000 samplefreq=1000 nchains=4 nruns=2 savebrlens=yes [temp=0.11];
 sump relburnin=yes [no] burninfrac=0.25 [2500];
 sumt relburnin=yes [no] burninfrac=0.25 [2500] contype=halfcompat [allcompat];
END;
    """.format(self.data.number_taxa, self.data.number_chars)
        return footer.strip()
