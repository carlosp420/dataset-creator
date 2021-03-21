from .utils import get_seq
from .base_dataset import DatasetBlock


class BankitDatasetBlock(DatasetBlock):
    def convert_to_string(self, block):
        """
        Takes a list of SeqRecordExpanded objects corresponding to a gene_code
        and produces the gene_block as string.

        :param block:
        :return: str.
        """
        out = ""
        for seq_record in block:
            taxon_id = ">{0}_{1} [organism={2} {3}] [Specimen_voucher={0}] " \
                       "{1} gene, partial cds".format(
                seq_record.voucher_code,
                seq_record.gene_code,
                seq_record.taxonomy['genus'],
                seq_record.taxonomy['species'],
            )
            sequence = get_seq(seq_record, self.codon_positions, self.aminoacids,
                               self.degenerate)
            seq = sequence.seq
            if sequence.warning:
                self.warnings.append(sequence.warning)

            n = 60
            seq = [seq[i:i + n] for i in range(0, len(seq), n)]
            out += '{0}\n{1}\n'.format(taxon_id, "\n".join(seq))
        return out
