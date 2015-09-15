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
    def __init__(self, seq_records):
        self.dataset_str = self.create_dataset()
        self.genes = None
        self.number_chars = None
        self.data = self._prepare_data()

    def create_dataset(self):
        creator = Creator(self.data)
        dataset_str = creator.dataset_str
        return dataset_str

    def extract_genes(self):
        pass

    def extract_total_number_of_chars(self):
        pass

    def extract_number_of_taxa(self):
        pass

    def _prepare_data(self):
        pass
