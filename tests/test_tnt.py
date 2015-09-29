import copy
import os
import unittest

from dataset_creator.dataset import Dataset

from .data import test_data

TNT_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Tnt')


class TestTnt(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.data = copy.copy(test_data)

    def test_dataset(self):
        dataset = Dataset(self.data, format='TNT', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(TNT_DATA_PATH, 'dataset.tnt')).read()
        self.assertEqual(expected, result)
