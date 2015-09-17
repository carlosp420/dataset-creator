from collections import namedtuple
from collections import OrderedDict

from .exceptions import WrongParameterFormat
from .creator import Creator


class Dataset(object):
    """
    User's class for making datasets of several formats. It needs as input a
    list of SeqRecord-expanded objects with as much info as possible:

    Arguments:
        - seq_records        - list. SeqRecordExpanded objects. The list should
                               be sorted by gene_code and then voucher code.
        - format             - str. NEXUS, PHYLIP, TNT, MEGA
        - partitioning       - str. Partitioning scheme: 'by gene' (default),
                               'by codon position', '1st-2nd, 3rd'
        - codon_positions    - str. Can be 1st, 2nd, 3rd, 1st-2nd, ALL (default).

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

    Example:

        >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene',
        ...                   codon_positions='1st',
        ...                   )
        >>> print(dataset.dataset_str)
        '#NEXUS
        blah blah
        '
    """
    def __init__(self, seq_records, format=None, partitioning=None,
                 codon_positions=None):
        self.seq_records = seq_records
        self.gene_codes = None
        self.number_taxa = None
        self.number_chars = None

        self.format = format
        self.partitioning = partitioning
        self.codon_positions = codon_positions

        self.data = None
        self._gene_codes_and_lengths = OrderedDict()
        self._prepare_data()
        self.dataset_str = self._create_dataset()

    def _prepare_data(self):
        """
        Creates named tuple with info needed to create a dataset.

        :return: named tuple
        """
        self._extract_genes()
        self._extract_total_number_of_chars()
        self._extract_number_of_taxa()

        Data = namedtuple('Data', ['gene_codes', 'number_taxa', 'number_chars',
                                   'seq_records'])
        self.data = Data(self.gene_codes, self.number_taxa, self.number_chars,
                         self.seq_records)

    def _extract_genes(self):
        gene_codes = [i.gene_code for i in self.seq_records]
        unique_gene_codes = list(set(gene_codes))
        unique_gene_codes.sort(key=str.lower)
        self.gene_codes = unique_gene_codes

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
        for seq_record in self.seq_records:
            if seq_record.gene_code not in self._gene_codes_and_lengths:
                self._gene_codes_and_lengths[seq_record.gene_code] = []
            seq = self._get_seq(seq_record)
            self._gene_codes_and_lengths[seq_record.gene_code].append(len(seq))

    def _get_seq(self, seq_record):
        """
        Checks parameters such as codon_positions, ... to return the required
        sequence as string

        :param seq_record: SeqRecordExpanded object.
        :return: str.
        """
        if self.codon_positions not in [None, '1st', '2nd', '3rd', '1st-2nd', 'ALL']:
            raise WrongParameterFormat("`codon_positions` argument should be any of the following"
                                       ": 1st, 2nd, 3rd, 1st-2nd or ALL")
        if self.codon_positions == '1st':
            return seq_record.first_codon_position()
        elif self.codon_positions == '2nd':
            return seq_record.second_codon_position()
        elif self.codon_positions == '3rd':
            return seq_record.third_codon_position()
        elif self.codon_positions == '1st-2nd':
            return seq_record.first_and_second_codon_positions()
        else:  # None and ALL
            return seq_record.seq

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

    def _create_dataset(self):
        creator = Creator(self.data, format=self.format,
                          partitioning=self.partitioning,
                          gene_codes_and_lengths=self._gene_codes_and_lengths)
        dataset_str = creator.dataset_str
        return dataset_str
