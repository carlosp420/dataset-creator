import os
import unittest

from dataset_creator.dataset import Dataset
from dataset_creator.creator import Creator

from .data import test_data

PHYLIP_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Phylip')


class TestPhylip(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_header(self):
        dataset = Dataset(test_data, format='PHYLIP', partitioning='by gene')
        creator = Creator(dataset.data, format='PHYLIP', partitioning='by gene')
        expected = '10 4739'
        result = creator.create_dataset_header()
        self.assertEqual(expected, result)
