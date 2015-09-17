import unittest

from dataset_creator import Dataset
from dataset_creator.exceptions import WrongParameterFormat
from .data import test_data


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_extract_genes(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.gene_codes
        self.assertEqual(expected, result)

    def test_extract_number_of_chars(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '4739'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_wrong_argument(self):
        self.assertRaises(WrongParameterFormat,
                          Dataset, test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='5th position')

    def test_extract_number_of_chars_first_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='1st')
        expected = '1580'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_second_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='2nd')
        expected = '1578'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_third_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='3rd')
        expected = '1581'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_first_and_second_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='1st-2nd')
        expected = '3158'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_taxa(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)

    def test_prepared_data(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.data.gene_codes
        self.assertEqual(expected, result)

    def test_dataset_nexus(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = open('dataset.nex', 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)
