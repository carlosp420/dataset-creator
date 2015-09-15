from .creator import Creator


class Dataset(object):
    """
    User's class for making datasets of several formats. It needs as input a
    list of SeqRecord-expanded objects with as much info as possible:

        * reading_frames
        * gene_codes
        * translation tables
        * taxonomy
        * sequences

    Attributes:
        - _gene_codes_and_lengths     - a dictionary of the form gene_code: list
                                        The list contains sequence lengths for its
                                        sequences. We assume the longest to be the
                                        real gene_code sequence length.
    """
    def __init__(self, seq_records, format=None, partitioning=None):
        self.seq_records = seq_records
        self.genes = None
        self.number_chars = None
        self.number_taxa = None
        self.data = None
        self._gene_codes_and_lengths = dict()
        self._prepare_data()
        self.dataset_str = self.create_dataset()

    def _prepare_data(self):
        """
        Creates named tuple with info needed to create a dataset.

        :return: named tuple
        """
        self._extract_genes()
        self._extract_total_number_of_chars()
        self._extract_number_of_taxa()

    def _extract_genes(self):
        gene_codes = [i.gene_code for i in self.seq_records]
        unique_gene_codes = list(set(gene_codes))
        unique_gene_codes.sort(key=str.lower)
        self.genes = unique_gene_codes

    def _extract_total_number_of_chars(self):
        """
        sets `self.number_chars` to the number of characters as string.
        """
        self._get_gene_codes_and_seq_lengths()

        sum = 0
        for seq_length in self._gene_codes_and_lengths.values():
            sum += sorted(seq_length, reverse=True)[0]
        self.number_chars = str(sum)

    def _get_gene_codes_and_seq_lengths(self):
        for i in self.seq_records:
            if i.gene_code not in self._gene_codes_and_lengths:
                self._gene_codes_and_lengths[i.gene_code] = []
            self._gene_codes_and_lengths[i.gene_code].append(len(i.seq))

    def _extract_number_of_taxa(self):
        """
        sets `self.number_taxa` to the number of taxa as string
        """
        n_taxa = dict()
        for i in self.seq_records:
            if i.gene_code not in n_taxa:
                n_taxa[i.gene_code] = 0
            n_taxa[i.gene_code] += 1
        number_taxa = sorted([i for i in n_taxa.values()], reverse=True)[0]
        self.number_taxa = str(number_taxa)

    def create_dataset(self):
        creator = Creator(self.data)
        dataset_str = creator.dataset_str
        return dataset_str
