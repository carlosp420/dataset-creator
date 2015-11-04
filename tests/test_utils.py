import unittest

from seqrecord_expanded import SeqRecordExpanded

from dataset_creator.utils import get_seq
from dataset_creator.exceptions import WrongParameterFormat


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.seq_record = SeqRecordExpanded('ATACGGTAG', table=1, reading_frame=1,
                                            voucher_code="CP100-10", gene_code="wingless")

    def test_get_seq(self):
        self.assertRaises(WrongParameterFormat, get_seq, seq_record=self.seq_record,
                          codon_positions='1st-3rd')

    def test_get_seq_sequence(self):
        """Test the returned sequence and warning"""
        result = get_seq(self.seq_record, codon_positions='ALL', aminoacids=True)
        self.assertEqual("IR*", result.seq)
        self.assertEqual("Gene wingless, sequence CP100-10 contains stop codons '*'",
                         result.warning)
