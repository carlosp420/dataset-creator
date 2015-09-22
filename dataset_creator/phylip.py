import io
import os
import uuid

from Bio import AlignIO


def convert_nexus_to_phylip(dataset_as_nexus):
    fake_handle = io.StringIO(dataset_as_nexus.replace('-', '_'))
    nexus_al = AlignIO.parse(fake_handle, 'nexus')
    tmp_file = make_random_filename()
    AlignIO.write(nexus_al, tmp_file, 'phylip-relaxed')
    dataset_as_phylip = read_and_delete_tmp_file(tmp_file)
    return dataset_as_phylip


def make_random_filename():
    return '{}.phy'.format(uuid.uuid4().hex)


def read_and_delete_tmp_file(filename):
    with open(filename, "r") as handle:
        contents = handle.read()

    if os.path.isfile(filename):
        os.remove(filename)

    return contents
