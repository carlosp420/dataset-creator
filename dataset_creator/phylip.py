from .nexus import DatasetFooter


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
