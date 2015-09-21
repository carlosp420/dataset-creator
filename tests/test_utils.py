import unittest

from seqrecord_expanded import SeqRecordExpanded

from dataset_creator.utils import get_seq
from dataset_creator.exceptions import WrongParameterFormat


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_seq(self):
        seq_record = SeqRecordExpanded('ATACGGAT')
        self.assertRaises(WrongParameterFormat, get_seq, seq_record=seq_record,
                          codon_positions='1st-3rd')
