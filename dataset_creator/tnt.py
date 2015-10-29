from .utils import get_seq
from .base_dataset import DatasetBlock


class TntDatasetBlock(DatasetBlock):
    def dataset_block(self):
        self.split_data()
        out = []
        for block in self._blocks:
            if self.outgroup is not None:
                block = self.put_outgroup_at_start_of_block(block)
            out.append(self.convert_to_string(block))
        return '\n'.join(out).strip() + '\n;\nproc/;'

    def put_outgroup_at_start_of_block(self, block):
        other_sequences = []

        for seq_record in block:
            if seq_record.voucher_code == self.outgroup:
                outgroup_sequence = seq_record
            else:
                other_sequences.append(seq_record)
        return [outgroup_sequence] + other_sequences

    def convert_to_string(self, block):
        """
        Takes a list of SeqRecordExpanded objects corresponding to a gene_code
        and produces the gene_block as string.

        :param block:
        :return: str.
        """
        out = None
        for seq_record in block:
            if not out:
                out = '&[dna]\n'.format(seq_record.gene_code)
            taxon_id = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                            seq_record.taxonomy['genus'],
                                            seq_record.taxonomy['species'],
                                            )
            seq = get_seq(seq_record, self.codon_positions)
            out += '{0}{1}\n'.format(taxon_id.ljust(55), seq)
        return out
