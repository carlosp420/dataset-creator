import json
import os
import unittest

from seqrecord_expanded import SeqRecordExpanded
from dataset_creator.dataset import Dataset

TNT_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Tnt')
SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')


class TestTnt(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        with open(SAMPLE_DATA_PATH, 'r') as handle:
            sample_data = json.loads(handle.read())
        self.data = []
        append = self.data.append

        for i in sample_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            append(seq_record)

    def test_dataset(self):
        dataset = Dataset(self.data, format='TNT', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(TNT_DATA_PATH, 'dataset.tnt')).read()
        self.assertEqual(expected, result)
