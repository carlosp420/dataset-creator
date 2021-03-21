# -*- coding: UTF-8 -*-
import six
if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO

import os
from collections import namedtuple
import uuid

from Bio import AlignIO

from .exceptions import WrongParameterFormat


def get_seq(seq_record, codon_positions, aminoacids=False, degenerate=None):
    """
    Checks parameters such as codon_positions, aminoacids... to return the
    required sequence as string.

    Parameters:
        seq_record (SeqRecordExpanded object):
        codon_positions (str):
        aminoacids (boolean):

    Returns:
        Namedtuple containing ``seq (str)`` and ``warning (str)``.
    """
    Sequence = namedtuple('Sequence', ['seq', 'warning'])

    if codon_positions not in [None, '1st', '2nd', '3rd', '1st-2nd', 'ALL']:
        raise WrongParameterFormat("`codon_positions` argument should be any of the following"
                                   ": 1st, 2nd, 3rd, 1st-2nd or ALL")
    if aminoacids:
        aa = seq_record.translate()
        if '*' in aa:
            warning = "Gene {0}, sequence {1} contains stop codons '*'".format(seq_record.gene_code,
                                                                               seq_record.voucher_code)
        else:
            warning = None
        return Sequence(seq=aa, warning=warning)

    if degenerate:
        return Sequence(seq=seq_record.degenerate(degenerate), warning=None)

    if codon_positions == '1st':
        return Sequence(seq=seq_record.first_codon_position(), warning=None)
    elif codon_positions == '2nd':
        return Sequence(seq=seq_record.second_codon_position(), warning=None)
    elif codon_positions == '3rd':
        return Sequence(seq=seq_record.third_codon_position(), warning=None)
    elif codon_positions == '1st-2nd':
        return Sequence(seq=seq_record.first_and_second_codon_positions(), warning=None)
    else:  # None and ALL
        return Sequence(seq=str(seq_record.seq), warning=None)


def convert_nexus_to_format(dataset_as_nexus, dataset_format):
    """
    Converts nexus format to Phylip and Fasta using Biopython tools.

    :param dataset_as_nexus:
    :param dataset_format:
    :return:
    """
    fake_handle = StringIO(dataset_as_nexus)
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


def make_dataset_header(data, file_format, aminoacids):
    """Creates the dataset header for NEXUS files from ``#NEXUS`` to ``MATRIX``.

    Parameters:
        data (namedtuple):    with necessary info for dataset creation.
        file_format (str):    TNT, PHYLIP, NEXUS, FASTA
        aminoacids (boolean): If ``aminoacids is True`` the header will show
                              ``DATATYPE=PROTEIN`` otherwise it will be ``DNA``.
    """
    if aminoacids:
        datatype = 'PROTEIN'
    else:
        datatype = 'DNA'

    if file_format in ['NEXUS', 'PHYLIP', 'FASTA']:
        header = """
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX={0} NCHAR={1};
FORMAT INTERLEAVE DATATYPE={2} MISSING=? GAP=-;
MATRIX
""".format(data.number_taxa, data.number_chars, datatype)

    elif file_format == 'MEGA':
        return "#MEGA\n!TITLE title;"

    else:  # file_format: TNT
        if aminoacids:
            molecule_type = "prot"
        else:
            molecule_type = "dna"
        header = """
nstates {0};
xread
{1} {2}""".format(molecule_type, data.number_chars, data.number_taxa)

    return header.strip()
