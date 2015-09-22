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
        self._reading_frame = self._set_reading_frame(reading_frame)
        self._codon_positions = self._set_codon_positions(codon_positions)
        self._partitioning = self._set_partitioning(partitioning)
        self._count_start = self._set_count_start(count_start)
        self._count_end = self._set_count_end(count_end)

    def _set_reading_frame(self, reading_frame):
        if not reading_frame:
            raise ValueError("_reading_frame argument is needed. Can't be None")
        else:
            return reading_frame

    def _set_codon_positions(self, codon_positions):
        if not codon_positions:
            raise ValueError("_codon_positions argument is needed. Can't be None")
        else:
            return codon_positions

    def _set_partitioning(self, partitioning):
        if not partitioning:
            raise ValueError("_partitioning argument is needed. Can't be None")
        else:
            return partitioning

    def _set_count_start(self, count_start):
        if not count_start:
            raise ValueError("codon_start argument is needed. Can't be None")
        else:
            return count_start

    def _set_count_end(self, count_end):
        if not count_end:
            raise ValueError("codon_end argument is needed. Can't be None")
        else:
            return count_end

    def get_corrected_count(self):
        if self._codon_positions == '1st-2nd' and self._partitioning in ['by gene',
                                                                         'by codon position',
                                                                         '1st-2nd, 3rd']:
            return self._using_1st2nd_codons()

        if self._codon_positions == 'ALL' and self._partitioning == 'by codon position':
            return self._using_all_codons_partition_by_codon_position()

        if self._codon_positions in ['ALL', '1st', '2nd', '3rd'] and self._partitioning == 'by gene':
            return self._using_all_codons_partition_by_gene()

        if self._codon_positions == 'ALL' and self._partitioning == '1st-2nd, 3rd':
            return self._using_all_codons_partition_by_1st2nd_3rd()

    def _using_1st2nd_codons(self):
        return [
            '{0}-{1}'.format(self._count_start, self._count_end),
            '{0}-{1}'.format(self._count_start + 1, self._count_end),
        ]

    def _using_all_codons_partition_by_codon_position(self):
        if self._reading_frame == 1:
            return [
                '{0}-{1}'.format(self._count_start, self._count_end),
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
            ]

        elif self._reading_frame == 2:
            return [
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
                '{0}-{1}'.format(self._count_start, self._count_end),
            ]

        else:
            return [
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
                '{0}-{1}'.format(self._count_start, self._count_end),
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
            ]

    def _using_all_codons_partition_by_gene(self):
        return [
            '{0}-{1}'.format(self._count_start, self._count_end,)
        ]

    def _using_all_codons_partition_by_1st2nd_3rd(self):
        if self._reading_frame == 1:
            return [
                '{0}-{1}\\3 {2}-{3}'.format(self._count_start, self._count_end,
                                            self._count_start + 1,
                                            self._count_end),
                '{0}-{1}'.format(self._count_start + 2, self._count_end),
            ]

        elif self._reading_frame == 2:
            return [
                '{0}-{1}\\3 {2}-{3}'.format(self._count_start + 1,
                                            self._count_end,
                                            self._count_start + 2,
                                            self._count_end),
                '{0}-{1}'.format(self._count_start, self._count_end),
            ]

        else:
            return [
                '{0}-{1}\\3 {2}-{3}'.format(self._count_start + 2,
                                            self._count_end,
                                            self._count_start,
                                            self._count_end),
                '{0}-{1}'.format(self._count_start + 1, self._count_end),
            ]
