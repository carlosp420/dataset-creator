def dataset_header(data):
    """
    :param data: named tuple with necessary info for dataset creation.
    """
    header = """
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX={0} NCHAR={1};
FORMAT INTERLEAVE DATATYPE=DNA MISSING=? GAP=-;
MATRIX
""".format(data.number_taxa, data.number_chars)
    return header.strip()


def dataset_block():
    return None
