from .exceptions import WrongParameterFormat


def get_seq(seq_record, codon_positions):
    """
    Checks parameters such as codon_positions, ... to return the required
    sequence as string

    :param seq_record: SeqRecordExpanded object.
    :return: str.
    """
    if codon_positions not in [None, '1st', '2nd', '3rd', '1st-2nd', 'ALL']:
        raise WrongParameterFormat("`codon_positions` argument should be any of the following"
                                   ": 1st, 2nd, 3rd, 1st-2nd or ALL")
    if codon_positions == '1st':
        return seq_record.first_codon_position()
    elif codon_positions == '2nd':
        return seq_record.second_codon_position()
    elif codon_positions == '3rd':
        return seq_record.third_codon_position()
    elif codon_positions == '1st-2nd':
        return seq_record.first_and_second_codon_positions()
    else:  # None and ALL
        return seq_record.seq
