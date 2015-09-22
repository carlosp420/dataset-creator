from . import nexus
from .phylip import convert_nexus_to_phylip


class Creator(object):
    """
    Create dataset and extra files for formats FASTA, NEXUS, PHYLIP, TNT and MEGA.
    We will create a NEXUS fomatte dataset first and use BioPython tools to
    convert to FASTA and PHYLIP formats.

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
        - partitioniong:     - 'by gene', 'by codon position', '1st-2nd, 3rd'

    Example:

        >>> dataset_creator = Creator(data, format='NEXUS', codon_positions='ALL',
        ...                           partitioning='by gene')
        >>> dataset_creator.dataset_str
        '#NEXUS
        blah blah
        '
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
        return nexus.dataset_header(self.data)

    def create_dataset_block(self):
        return nexus.DatasetBlock(self.data, self.codon_positions,
                                  self.partitioning).dataset_block()

    def create_dataset_footer(self):
        return nexus.DatasetFooter(self.data, codon_positions=self.codon_positions,
                                   partitioning=self.partitioning).dataset_footer()

    def create_extra_dataset_file(self):
        pass

    def put_everything_together(self):
        dataset_as_nexus = '{0}\n\n{1}\n\n{2}'.format(self.dataset_header,
                                                      self.dataset_block,
                                                      self.dataset_footer)
        if self.format == 'NEXUS':
            return dataset_as_nexus

        elif self.format == 'PHYLIP':
            return convert_nexus_to_phylip(dataset_as_nexus)
