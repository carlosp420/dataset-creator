import copy
import os
import unittest

from dataset_creator.dataset import Dataset

from .data import test_data

PHYLIP_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Phylip')


class TestPhylip(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.data = copy.copy(test_data)

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
