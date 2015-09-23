import six

if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO

from Bio import AlignIO

from .utils import make_random_filename
from .utils import read_and_delete_tmp_file


def convert_nexus_to_fasta(dataset_as_nexus):
    fake_handle = StringIO(dataset_as_nexus.replace('-', '_'))
    nexus_al = AlignIO.parse(fake_handle, 'nexus')
    tmp_file = make_random_filename(file_format='fas')
    AlignIO.write(nexus_al, tmp_file, 'fasta')
    dataset_as_fasta = read_and_delete_tmp_file(tmp_file)
    return dataset_as_fasta
