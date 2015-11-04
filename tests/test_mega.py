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

    def test_dataset_as_aminoacids(self):
        dataset = Dataset(test_data, format='MEGA', partitioning='by gene',
                          aminoacids=True)
        result = dataset.dataset_str
        expected = open(os.path.join(MEGA_DATA_PATH, 'dataset_aa.meg')).read()
        self.assertEqual(expected, result)

    def test_dataset_as_degenerate(self):
        dataset = Dataset(test_data, format='MEGA', partitioning='by gene',
                          degenerate='S')
        result = dataset.dataset_str
        expected = open(os.path.join(MEGA_DATA_PATH, 'dataset_degenerate.meg')).read()
        self.assertEqual(expected, result)

    def test_dataset_as_degenerate_bad_partitioning_scheme(self):
        self.assertRaises(ValueError, Dataset, test_data, format='MEGA',
                          partitioning='1st-2nd, 3rd', degenerate='S')

    def test_partitioning_dataset_in_mega_format(self):
        self.assertRaises(ValueError, Dataset, test_data, format='MEGA',
                          partitioning='1st-2nd, 3rd')
