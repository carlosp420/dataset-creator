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
                        * gene_codes_and_lengths
        - format    - str. NEXUS, PHYLIP, TNT, MEGA
        - gene_codes_and_lengths      - dict of gene_code and length of sequence
                                        as inferred from the longest DNA seq for
                                        each gene.
        - codon_positions    - str. Can be 1st, 2nd, 3rd, 1st-2nd, ALL (default).

    Example:

        >>> dataset_creator = Creator(data, format='NEXUS', codon_positions='ALL',
        ...                           partitioning='by gene')
    """
    def __init__(self, data, format=None, codon_positions=None, partitioning=None):
        self.data = data
        self.format = format
        self.codon_positions = codon_positions
        self.partitioning = partitioning
        self.dataset_header = self.create_dataset_header()
        self.dataset_block = self.create_dataset_block()
        self.dataset_footer = self.create_dataset_footer()
        self.dataset_str = self.put_everything_together()

    def create_dataset_header(self):
        if self.format == 'NEXUS':
            return nexus.dataset_header(self.data)

    def create_dataset_block(self):
        if self.format == 'NEXUS':
            return nexus.DatasetBlock(self.data, self.codon_positions,
                                      self.partitioning).dataset_block()

    def create_dataset_footer(self):
        if self.format == 'NEXUS':
            return nexus.DatasetFooter(self.data, self.codon_positions,
                                       self.partitioning).dataset_footer()

    def create_extra_dataset_file(self):
        pass

    def put_everything_together(self):
        return '{0}\n\n{1}\n\n{2}'.format(self.dataset_header, self.dataset_block,
                                          self.dataset_footer)
