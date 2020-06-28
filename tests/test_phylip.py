import os
import unittest

from dataset_creator.dataset import Dataset
from .generate_test_data import get_test_data

PHYLIP_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Phylip')
SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')


class TestPhylip(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.test_data = get_test_data()

    def tearDown(self):
        del self.test_data

    def test_dataset(self):
        dataset = Dataset(self.test_data, format='PHYLIP', partitioning='by gene')
        result = dataset.dataset_str
        with open(os.path.join(PHYLIP_DATA_PATH, 'dataset.phy'), 'r') as handle:
            expected = handle.read()
            self.assertEqual(expected.strip(), result.strip())

    def test_charset_file(self):
        dataset = Dataset(self.test_data, format='PHYLIP', partitioning='by gene')
        result = dataset.extra_dataset_str
        with open(os.path.join(PHYLIP_DATA_PATH, 'charset_block_file.txt'), 'r') as handle:
            expected = handle.read()
            self.assertEqual(expected.strip(), result)
