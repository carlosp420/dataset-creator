from .utils import get_seq
from .base_dataset import DatasetBlock


class GenBankFASTADatasetBlock(DatasetBlock):
    def convert_to_string(self, block):
        """
        Takes a list of SeqRecordExpanded objects corresponding to a gene_code
        and produces the gene_block as string.

        :param block:
        :return: str.
        """
        out = ""
        for seq_record in block:
            taxon_id = ">{0}_{1}_{2} [org={0} {1}] [Specimen-voucher={2}] " \
                       "[note={3} gene, partial cds.] [Lineage={4}]".format(
                seq_record.taxonomy['genus'],
                seq_record.taxonomy['species'],
                seq_record.voucher_code,
                seq_record.gene_code,
                seq_record.lineage,
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
