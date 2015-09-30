from . import nexus
from . import tnt
from . import mega
from .phylip import PhylipDatasetFooter
from .utils import convert_nexus_to_format
from .utils import make_dataset_header


class Creator(object):
    """
    Create dataset and extra files for formats FASTA, NEXUS, PHYLIP, TNT and MEGA.
    We will create a NEXUS fomatte dataset first and use BioPython tools to
    convert to FASTA and PHYLIP formats.

    Parameters:
        data (named tuple):     containing:
                                  * gene_codes: list
                                  * number_chars: string
                                  * number_taxa: string
                                  * seq_recods: list of SeqRecordExpanded objetcs
                                  * gene_codes_and_lengths
        format (str):           NEXUS, PHYLIP, TNT, MEGA
        codon_positions (str):  Can be 1st, 2nd, 3rd, 1st-2nd, ALL (default).
        partitioniong (str):    'by gene', 'by codon position', '1st-2nd, 3rd'
        aminoacids (bolean):    To create aminoacid sequences instead of returning
                                nucleotides.
        degenerate (str):       Method to degenerate nucleotide sequences,
                                following Zwick et al. Can be ``S``, ``Z``,
                                ``SZ`` and ``normal``.

    Attributes:
        extra_dataset_str (str):    Charset block in Phylip formatted datasets.

    Example:

        >>> dataset_creator = Creator(data, format='NEXUS', codon_positions='ALL',
        ...                           partitioning='by gene')
        >>> dataset_creator.dataset_str
        '#NEXUS
        blah blah
        '
    """
    def __init__(self, data, format=None, codon_positions=None, partitioning=None,
                 aminoacids=None, degenerate=None):
        self.warnings = []
        self.data = data
        self.format = format
        self.codon_positions = codon_positions
        self.partitioning = partitioning
        self.aminoacids = aminoacids
        self.degenerate = degenerate
        self.dataset_header = self.create_dataset_header()
        self.dataset_block = self.create_dataset_block()
        self.dataset_footer = self.create_dataset_footer()
        self.dataset_str = self.put_everything_together()
        self.extra_dataset_str = self.create_extra_dataset_file()

    def create_dataset_header(self):
        return make_dataset_header(self.data, file_format=self.format)

    def create_dataset_block(self):
        if self.format in ['NEXUS', 'PHYLIP', 'FASTA']:
            return nexus.DatasetBlock(self.data, self.codon_positions,
                                      self.partitioning,
                                      self.aminoacids,
                                      self.degenerate).dataset_block()
        elif self.format == 'MEGA':
            return mega.MegaDatasetBlock(self.data, self.codon_positions,
                                         self.partitioning).dataset_block()
        else:  # TNT
            return tnt.TntDatasetBlock(self.data, self.codon_positions,
                                       self.partitioning).dataset_block()

    def create_dataset_footer(self):
        return nexus.DatasetFooter(self.data, codon_positions=self.codon_positions,
                                   partitioning=self.partitioning).dataset_footer()

    def create_extra_dataset_file(self):
        phylip_footer = PhylipDatasetFooter(self.data,
                                            codon_positions=self.codon_positions,
                                            partitioning=self.partitioning)
        return phylip_footer.make_charset_block()

    def put_everything_together(self):
        header_and_datablock = '{0}\n\n{1}'.format(self.dataset_header,
                                                   self.dataset_block)
        if self.format == 'NEXUS':
            return '{0}\n\n{1}'.format(header_and_datablock, self.dataset_footer)

        elif self.format == 'PHYLIP':
            self.extra_dataset_str = self.create_extra_dataset_file()
            return convert_nexus_to_format(header_and_datablock, 'phylip-relaxed')

        elif self.format == 'FASTA':
            return convert_nexus_to_format(header_and_datablock, 'fasta')

        elif self.format == 'TNT':
            return '{0}\n\n{1}'.format(self.dataset_header, self.dataset_block)

        else:  # MEGA
            return '{0}\n\n{1}'.format(self.dataset_header, self.dataset_block)
