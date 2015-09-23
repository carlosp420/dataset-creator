import six

if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO

from Bio import AlignIO

from .nexus import DatasetFooter
from .utils import make_random_filename
from .utils import read_and_delete_tmp_file


def convert_nexus_to_phylip(dataset_as_nexus):
    fake_handle = StringIO(dataset_as_nexus.replace('-', '_'))
    nexus_al = AlignIO.parse(fake_handle, 'nexus')
    tmp_file = make_random_filename(file_format='phy')
    AlignIO.write(nexus_al, tmp_file, 'phylip-relaxed')
    dataset_as_phylip = read_and_delete_tmp_file(tmp_file)
    return dataset_as_phylip


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
