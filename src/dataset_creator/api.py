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
        self.dataset_str = None

    def create_dataset(self):
        self.dataset_str = '#NEXUS dataset'

    def extract_genes(self):
        pass

    def extract_total_number_of_chars(self):
        pass

    def extract_number_of_taxa(self):
        pass
