import unittest

from .data import test_data
from dataset_creator.dataset import Dataset
from dataset_creator.creator import Creator


class TestCreator(unittest.TestCase):
    def setUp(self):
        pass

    def test_nexus_header(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        creator = Creator(dataset.data, format='NEXUS')
        expected = """
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX=10 NCHAR=4739;
FORMAT INTERLEAVE DATATYPE=DNA MISSING=? GAP=-;
MATRIX
"""
        result = creator.dataset_header
        self.assertEqual(expected.strip(), result)
