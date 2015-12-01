import os
import unittest

from dataset_creator.dataset import Dataset

from .generate_test_data import get_test_data


FASTA_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Fasta')


class TestFasta(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.test_data = get_test_data()

    def tearDown(self):
        del self.test_data

    def test_dataset(self):
        dataset = Dataset(self.test_data, format='FASTA', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset.fas')).read()
        self.assertEqual(expected, result)

    def test_dataset_with_gaps(self):
        seq = self.test_data[0].seq
        seq = list(seq)
        seq[:3] = "---"
        self.test_data[0].seq = "".join(seq)

        dataset = Dataset(self.test_data, format='FASTA', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_with_gaps.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd(self):
        dataset = Dataset(self.test_data, format='FASTA', partitioning='1st-2nd, 3rd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_1st2nd_3rd.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_1st2nd_codon_positions(self):
        dataset = Dataset(self.test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='1st-2nd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_1st2nd.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_1st_codon_position(self):
        dataset = Dataset(self.test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='1st')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_1st.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_2nd_codon_position(self):
        dataset = Dataset(self.test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='2nd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_2nd.fas')).read()
        self.assertEqual(expected, result)

    def test_partitioned_by_1st2nd_3rd_only_3rd_codon_position(self):
        dataset = Dataset(self.test_data, format='FASTA', partitioning='1st-2nd, 3rd',
                          codon_positions='3rd')
        result = dataset.dataset_str
        expected = open(os.path.join(FASTA_DATA_PATH, 'dataset_3rd.fas')).read()
        self.assertEqual(expected, result)
