import unittest

from seqrecord_expanded import SeqRecordExpanded

from dataset_creator.base_dataset import DatasetBlock


class TestDatasetBlock(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_flatten_taxonomy(self):
        seq = {
                  'seq': '????????????',
                  'voucher_code': "CP100-11",
                  'taxonomy': {
                      "orden": "Lepidoptera",
                      "family": "Nymphalidae",
                      "subfamily": "Satyrinae",
                      "tribe": "Satyrini",
                      "subtribe": "Euptychiina",
                      "genus": "Euptychia",
                      "species": "",
                  },
                  'gene_code': 'ef1a',
                  'reading_frame': 2,
                  'table': 1,
              }
        dataset_block = DatasetBlock(data="", codon_positions="ALL", partitioning="")
        seq_record = SeqRecordExpanded(
            seq['seq'],
            voucher_code=seq['voucher_code'],
            taxonomy=seq['taxonomy'],
            gene_code=seq['gene_code'],
            reading_frame=seq['reading_frame'],
            table=seq['table'],
        )
        expected = "_Lepidoptera_Nymphalidae_Satyrinae_Satyrini_Euptychiina_Euptychia"
        result = dataset_block.flatten_taxonomy(seq_record)
        self.assertEqual(expected, result)

    def test_flatten_taxonomy__no_taxonomy(self):
        seq = {
            'seq': '????????????',
            'voucher_code': "CP100-11",
            'gene_code': 'ef1a',
            'reading_frame': 2,
            'table': 1,
        }
        dataset_block = DatasetBlock(data="", codon_positions="ALL", partitioning="")
        seq_record = SeqRecordExpanded(
            seq['seq'],
            voucher_code=seq['voucher_code'],
            gene_code=seq['gene_code'],
            reading_frame=seq['reading_frame'],
            table=seq['table'],
        )
        expected = ""
        result = dataset_block.flatten_taxonomy(seq_record)
        self.assertEqual(expected, result)
