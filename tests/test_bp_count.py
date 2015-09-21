import unittest

from dataset_creator.bp_count import BasePairCount


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
