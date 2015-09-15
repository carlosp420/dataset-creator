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
    """
    def __init__(self, seq_records, format=None, partitioning=None):
        self.seq_records = seq_records
        self.genes = None
        self.number_chars = None
        self.data = None
        self._prepare_data()
        self.dataset_str = self.create_dataset()

    def _prepare_data(self):
        """
        Creates named tuple with info needed to create a dataset.

        :return: named tuple
        """
        self._extract_genes()
        self._extract_total_number_of_chars()
        return None

    def create_dataset(self):
        creator = Creator(self.data)
        dataset_str = creator.dataset_str
        return dataset_str

    def _extract_genes(self):
        gene_codes = [i.gene_code for i in self.seq_records]
        unique_gene_codes = list(set(gene_codes))
        unique_gene_codes.sort(key=str.lower)
        self.genes = unique_gene_codes

    def _extract_total_number_of_chars(self):
        """
        :return: number of characters as string
        """
        gene_codes_and_lengths = self._get_gene_codes_and_seq_lengths()

        sum = 0
        for k, v in gene_codes_and_lengths.items():
            sum += sorted(v, reverse=True)[0]
        self.number_chars = str(sum)

    def _get_gene_codes_and_seq_lengths(self):
        gene_codes_and_lengths = dict()
        for i in self.seq_records:
            if i.gene_code not in gene_codes_and_lengths:
                gene_codes_and_lengths[i.gene_code] = []
            gene_codes_and_lengths[i.gene_code].append(len(i.seq))
        return gene_codes_and_lengths

    def extract_number_of_taxa(self):
        pass
