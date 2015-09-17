from . import nexus


class Creator(object):
    """
    Create dataset and extra files for formats FASTA, NEXUS, PHYLIP, TNT and MEGA.

    Parameters:
        - data      - named tuple containing:
                        * gene_codes: list
                        * number_chars: string
                        * number_taxa: string
                        * seq_recods: list of SeqRecordExpanded objetcs
        - format    - str. NEXUS, PHYLIP, TNT, MEGA
        - gene_codes_and_lengths      - dict of gene_code and length of sequence
                                        as inferred from the longest DNA seq for
                                        each gene.

    Example:

        >>> dataset_creator = Creator(data, format='NEXUS', partitioning='by gene')
    """
    def __init__(self, data, format=None, partitioning=None, gene_codes_and_lengths=None):
        self.data = data
        self.format = format
        self.partitioning = partitioning
        self.gene_codes_and_lengths = gene_codes_and_lengths
        self.dataset_str = None
        self.dataset_header = self.create_dataset_header()
        self.dataset_block = self.create_dataset_block()
        self.dataset_footer = self.create_dataset_footer()

    def create_dataset_header(self):
        if self.format == 'NEXUS':
            return nexus.dataset_header(self.data)

    def create_dataset_block(self):
        if self.format == 'NEXUS':
            return nexus.DatasetBlock(self.data, self.partitioning).dataset_block()

    def create_dataset_footer(self):
        if self.format == 'NEXUS':
            return nexus.DatasetFooter(self.data, self.gene_codes_and_lengths).dataset_footer()

    def create_extra_dataset_file(self):
        pass
