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
            [100, 512],
            [101, 513],
        ]
    """
