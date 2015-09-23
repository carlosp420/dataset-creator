import os
import unittest

from dataset_creator.dataset import Dataset

from .data import test_data

MEGA_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Mega')


class TestMega(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dataset(self):
        dataset = Dataset(test_data, format='MEGA', partitioning='by gene')
        result = dataset.dataset_str
        expected = open(os.path.join(MEGA_DATA_PATH, 'dataset.meg')).read()
        self.assertEqual(expected, result)
