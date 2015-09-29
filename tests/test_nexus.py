import os
import unittest

from .data import test_data
from dataset_creator.dataset import Dataset
from dataset_creator.nexus import DatasetFooter
from dataset_creator.nexus import BasePairCount


NEXUS_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Nexus')


class TestNexus(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_nexus_header(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)

    def test_aminoacid_dataset(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          aminoacids=True)
        result = dataset.dataset_str
        with open(os.path.join(NEXUS_DATA_PATH, 'dataset_aa.nex'), 'r') as handle:
            expected = handle.read()
        self.assertEqual(expected, result)


class TestDatasetFooter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_partitioning_parameter(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        self.assertRaises(AttributeError, DatasetFooter, data=dataset.data,
                          codon_positions='ALL', partitioning='by genes')

    def test_codon_positions_parameter(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        self.assertRaises(AttributeError, DatasetFooter, data=dataset.data,
                          codon_positions='1st-2nd, 3rd', partitioning='by gene')

    def test_make_charset_block(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        footer = DatasetFooter(data=dataset.data, codon_positions='ALL', partitioning='by gene')
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

    def test_make_partition_line(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        footer = DatasetFooter(data=dataset.data, codon_positions='ALL', partitioning='by gene')
        expected = """
partition GENES = 7: ArgKin, COI-begin, COI_end, ef1a, RpS2, RpS5, wingless;

set partition = GENES;
"""
        result = footer.make_partition_line()
        self.assertEqual(expected.strip(), result)

    def test_dataset_all_codon_positions_partitioned_by_gene(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_1st_2nd_codon_positions_partitioned_by_gene(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='1st-2nd', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st2nd_codons.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_1st_2nd_codon_positions_partitioned_as_1st2nd_3rd(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='1st-2nd', partitioning='1st-2nd, 3rd')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st2nd_codons_partitioned_as_1st2nd_3rd.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_1st_2nd_codon_positions_partitioned_as_each_codon_position(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='1st-2nd', partitioning='by codon position')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st2nd_codons_partitioned_as_each.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)


class TestBpCount(unittest.TestCase):
    def setUp(self):
        pass

    def test_parameter_reading_frame(self):
        self.assertRaises(ValueError, BasePairCount, codon_positions='1st-2nd',
                          partitioning='by codon position', count_start=100, count_end=512)

    def test_parameter_codon_positions(self):
        self.assertRaises(ValueError, BasePairCount, reading_frame=1,
                          partitioning='by codon position', count_start=100, count_end=512)

    def test_parameter_partitioning(self):
        self.assertRaises(ValueError, BasePairCount, codon_positions='1st-2nd',
                          reading_frame=1, count_start=100, count_end=512)

    def test_parameter_count_start(self):
        self.assertRaises(ValueError, BasePairCount, codon_positions='1st-2nd',
                          partitioning='by codon position', reading_frame=1, count_end=512)

    def test_parameter_count_end(self):
        self.assertRaises(ValueError, BasePairCount, codon_positions='1st-2nd',
                          partitioning='by codon position', count_start=100, reading_frame=1)
