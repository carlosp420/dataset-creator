import six

if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO
import os
import uuid

from Bio import AlignIO

from .nexus import DatasetFooter


def convert_nexus_to_phylip(dataset_as_nexus):
    fake_handle = StringIO(dataset_as_nexus.replace('-', '_'))
    nexus_al = AlignIO.parse(fake_handle, 'nexus')
    tmp_file = make_random_filename()
    AlignIO.write(nexus_al, tmp_file, 'phylip-relaxed')
    dataset_as_phylip = read_and_delete_tmp_file(tmp_file)
    return dataset_as_phylip


def make_random_filename():
    return '{0}.phy'.format(uuid.uuid4().hex)


def read_and_delete_tmp_file(filename):
    with open(filename, "r") as handle:
        contents = handle.read()

    if os.path.isfile(filename):
        os.remove(filename)

    return contents


class PhylipDatasetFooter(DatasetFooter):
    def make_charset_block(self):
        """
        Overriden function for Phylip dataset as the content is different and
        goes into a separate file.
        """
        out = self.make_charsets()
        return out.strip()

    def make_charsets(self):
        """
        Overriden function for Phylip dataset as the content is different and
        goes into a separate file.
        """
        count_start = 1
        out = ''
        for gene_code, lengths in self.data.gene_codes_and_lengths.items():
            count_end = lengths[0] + count_start - 1
            formatted_line = self.format_charset_line(gene_code, count_start, count_end)
            converted_line = formatted_line.replace('    charset', 'DNA,').replace(';', '')
            out += converted_line
            count_start = count_end + 1
        return out
