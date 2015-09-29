import json
import os
import unittest

from seqrecord_expanded import SeqRecordExpanded

from dataset_creator.dataset import Dataset

PHYLIP_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Phylip')
SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')


class TestPhylip(unittest.TestCase):
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
        dataset = Dataset(self.data, format='PHYLIP', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(PHYLIP_DATA_PATH, 'dataset.phy')).read()
        self.assertEqual(expected, result)

    def test_charset_file(self):
        dataset = Dataset(self.data, format='PHYLIP', partitioning='by gene')
        result = dataset.extra_dataset_str
        expected = open(os.path.join(PHYLIP_DATA_PATH, 'charset_block_file.txt')).read()
        self.assertEqual(expected, result)
