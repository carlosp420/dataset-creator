from .utils import get_seq
from .nexus import DatasetBlock


class MegaDatasetBlock(DatasetBlock):
    def dataset_block(self):
        self.split_data()
        return self.convert_blocks_to_string()

    def convert_blocks_to_string(self):
        """
        New method, only in MegaDatasetBlock class.

        :return: flattened data blocks as string
        """
        taxa_ids = [[]] * int(self.data.number_taxa)
        sequences = [''] * int(self.data.number_taxa)

        for block in self._blocks:
            for index, seq_record in enumerate(block):
                taxa_ids[index] = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                                       seq_record.taxonomy['genus'],
                                                       seq_record.taxonomy['species'],
                                                       )
                sequences[index] += get_seq(seq_record, self.codon_positions)

        out = ''
        for index, value in enumerate(taxa_ids):
            out += '#{0}\n{1}\n'.format(taxa_ids[index], sequences[index])
        return out
