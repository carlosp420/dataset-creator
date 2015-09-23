import six
if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO

import os
import uuid

from Bio import AlignIO

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


def convert_nexus_to_format(dataset_as_nexus, dataset_format):
    """
    Converts nexus format to Phylip and Fasta using BioPython tools.

    :param dataset_as_nexus:
    :param dataset_format:
    :return:
    """
    fake_handle = StringIO(dataset_as_nexus.replace('-', '_'))
    nexus_al = AlignIO.parse(fake_handle, 'nexus')
    tmp_file = make_random_filename()
    AlignIO.write(nexus_al, tmp_file, dataset_format)
    dataset_as_fasta = read_and_delete_tmp_file(tmp_file)
    return dataset_as_fasta


def make_random_filename():
    return '{0}.txt'.format(uuid.uuid4().hex)


def read_and_delete_tmp_file(filename):
    with open(filename, "r") as handle:
        contents = handle.read()

    if os.path.isfile(filename):
        os.remove(filename)

    return contents
