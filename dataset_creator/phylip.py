from .utils import get_seq


def dataset_header(data):
    """
    :param data: named tuple with necessary info for dataset creation.
    """
    return '{0} {1}'.format(data.number_taxa, data.number_chars)
