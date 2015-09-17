import unittest

from .data import test_data
from dataset_creator.dataset import Dataset
from dataset_creator.creator import Creator


class TestNexus(unittest.TestCase):
    def setUp(self):
        pass

    def test_nexus_header(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)


class TestDatasetFooter(unittest.TestCase):
    def setUp(self):
        pass

    def test_make_footer(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        creator = Creator(dataset.data, format='NEXUS', partitioning='by gene')
        expected = ''
        result = creator.dataset_footer
        self.assertEqual(expected, result)
