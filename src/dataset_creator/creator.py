from . import nexus


class Creator(object):
    """
    Create dataset and extra files for formats FASTA, NEXUS, PHYLIP, TNT and MEGA.

    Parameters:
        - data      - named tuple containing:
        - format    - str. NEXUS, PHYLIP, TNT, MEGA
                        * gene_codes: list
                        * number_chars: string
                        * number_taxa: string
                        * seq_recods: list of SeqRecordExpanded objetcs

    Example:

        >>> dataset_creator = Creator(data, format='NEXUS',
        ...                           partitioning='by gene')
    """
    def __init__(self, data, format=None, partitioning=None):
        self.data = data
        self.format = format
        self.partitioning = partitioning
        self.dataset_str = None
        self.dataset_header = None
        self.dataset_block = None

    def create_dataset_header(self):
        if self.format == 'NEXUS':
            self.dataset_header = nexus.dataset_header(self.data)

    def create_dataset_blocks(self):
        if self.format == 'NEXUS':
            self.dataset_block = nexus.dataset_block()

    def create_dataset_footer(self):
        pass

    def create_extra_dataset_file(self):
        pass
