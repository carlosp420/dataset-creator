import unittest

from .data import test_data
from dataset_creator.dataset import Dataset
from dataset_creator.creator import Creator
from dataset_creator.nexus import DatasetFooter


class TestNexus(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_nexus_header(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)


class TestDatasetFooter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_make_charset_block(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        footer = DatasetFooter(dataset.data)
        expected = """
begin mrbayes;
    charset ArgKin = 1-596;
    charset COI-begin = 597-1265;
    charset COI_end = 1266-2071;
    charset ef1a = 2072-3311;
    charset RpS2 = 3312-3722;
    charset RpS5 = 3723-4339;
    charset wingless = 4340-4739;
        """
        result = footer.charset_block
        self.assertEqual(expected.strip(), result)
