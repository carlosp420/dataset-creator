import os
import unittest

from dataset_creator.dataset import Dataset

from .data import test_data

FASTA_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Fasta')


class TestGenBankFASTA(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dataset(self):
        dataset = Dataset(test_data, format='GenBankFASTA', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_genbankfasta.fas')).read()
        self.assertEqual(expected, result)
