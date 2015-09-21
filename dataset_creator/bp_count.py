class BasePairCount(object):
    """
    Uses reading frame info, partitioning method and number of codon positions
    to return corrected base pair count for charset lines.

    Example:

        >>> bp_count = BasePairCount(reading_frame=1, codon_positions='1st-2nd',
        ...                          partitioning='by codon position',
        ...                          count_start=100, count_end=512)
        >>> bp_count.get_corrected_count()
        [
            '100-512',
            '101-513',
        ]
    """
    def __init__(self, reading_frame=None, codon_positions=None, partitioning=None,
                 count_start=None, count_end=None):
        self._reading_frame = reading_frame
        self._codon_positions = codon_positions
        self._partitioning = partitioning
        self._count_start = count_start
        self._count_end = count_end

        if self._reading_frame is None:
            raise ValueError("_reading_frame argument is needed. Can't be None")
        elif self._codon_positions is None:
            raise ValueError("_codon_positions argument is needed. Can't be None")
        elif self._partitioning is None:
            raise ValueError("_partitioning argument is needed. Can't be None")
        elif self._count_start is None:
            raise ValueError("codon_start argument is needed. Can't be None")
        elif self._count_end is None:
            raise ValueError("codon_end argument is needed. Can't be None")

    def get_corrected_count(self):
        if self._codon_positions == '1st-2nd' and self._partitioning == 'by codon position':
            if self._reading_frame in [1, 2, 3]:
                return [
                    '{0}-{1}'.format(self._count_start, self._count_end),
                    '{0}-{1}'.format(self._count_start + 1, self._count_end),
                ]
