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
        if self.aminoacids:
            molecule_type = "protein"
        else:
            molecule_type = "dna"

        out = None

        max_taxon_id = 0
        for seq_record in block:
            taxon_id = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                            seq_record.taxonomy['genus'],
                                            seq_record.taxonomy['species'],
                                            )
            if len(taxon_id) > max_taxon_id:
                max_taxon_id = len(taxon_id)

        pad_number = max_taxon_id + 1
        if pad_number < 55:
            pad_number = 55

        for seq_record in block:
            if not out:
                out = '&[{0}]\n'.format(molecule_type, seq_record.gene_code)
            taxon_id = '{0}_{1}_{2}'.format(seq_record.voucher_code,
                                            seq_record.taxonomy['genus'],
                                            seq_record.taxonomy['species'],
                                            )
            sequence = get_seq(seq_record, self.codon_positions, self.aminoacids,
                               self.degenerate)
            seq = sequence.seq
            if sequence.warning:
                self.warnings.append(sequence.warning)

            out += '{0}{1}\n'.format(taxon_id.ljust(pad_number), seq)
        return out
