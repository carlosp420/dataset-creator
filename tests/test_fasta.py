import os
import unittest

from dataset_creator.dataset import Dataset

from .data import test_data

FASTA_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Fasta')


class TestFasta(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dataset(self):
        dataset = Dataset(test_data, format='FASTA', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd(self):
        dataset = Dataset(test_data, format='FASTA', partitioning='1st-2nd, 3rd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_1st2nd_3rd.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_1st2nd_codon_positions(self):
        dataset = Dataset(test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='1st-2nd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_1st2nd.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_1st_codon_position(self):
        dataset = Dataset(test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='1st')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_1st.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_2nd_codon_position(self):
        dataset = Dataset(test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='2nd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_2nd.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_3rd_codon_position(self):
        dataset = Dataset(test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='3rd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_3rd.fas')).read()
        self.assertEqual(expected, result)
