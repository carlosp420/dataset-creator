import unittest

from dataset_creator import Dataset
from .data import test_data


class TestApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_extract_genes(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.genes
        self.assertEqual(expected, result)
