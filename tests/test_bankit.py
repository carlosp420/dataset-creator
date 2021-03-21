import os
import unittest

from dataset_creator.dataset import Dataset
from dataset_creator.enums import DatasetFormat

from .data import test_data

FASTA_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Fasta')


class TestBankit(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dataset(self):
        dataset = Dataset(test_data, format=DatasetFormat.BANKIT.value, partitioning='by gene')
        result = dataset.dataset_str
        with open(os.path.join(FASTA_DATA_PATH, 'dataset_bankit.fas')) as handle:
            expected = handle.read()
            self.assertEqual(expected, result)
