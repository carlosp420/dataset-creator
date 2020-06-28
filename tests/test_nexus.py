# -*- coding: UTF-8 -*-
from copy import copy
import json
import os

try:
    # Needed for Python 2.6. Remove this import after dropping support for Python 2.6
    import unittest2 as unittest
except ImportError:
    import unittest

from seqrecord_expanded import SeqRecordExpanded
from seqrecord_expanded.exceptions import TranslationErrorMixedGappedSeq

from .data import test_data
from dataset_creator.dataset import Dataset
from dataset_creator.base_dataset import DatasetFooter
from dataset_creator.base_dataset import BasePairCount


NEXUS_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Nexus')


def get_test_data(type_of_data=None, filename="sample_data.txt"):
    """
    Parameters:
        type_of_data (str):     ``raw_data`` or ``seq_records``
    """
    with open(os.path.join(NEXUS_DATA_PATH, "..", filename), "r") as handle:
        raw_data = json.loads(handle.read())

    if type_of_data == 'raw_data':
        return raw_data
    elif type_of_data == 'seq_records':
        seq_records = []
        for i in raw_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            seq_records.append(seq_record)
        return seq_records


class TestNexus(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.seq_records = copy(get_test_data('seq_records'))

    def tearDown(self):
        del self.seq_records

    def test_nexus_header(self):
        dataset = Dataset(self.seq_records, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)

    def test_aminoacid_dataset(self):
        dataset = Dataset(self.seq_records, format='NEXUS', partitioning='by gene',
                          aminoacids=True)
        result = dataset.dataset_str
        with open(os.path.join(NEXUS_DATA_PATH, 'dataset_aa.nex'), 'r') as handle:
            expected = handle.read()
        self.assertEqual(expected.strip(), result)

    def test_dataset_when_seqrecord_taxonomy_is_none(self):
        raw_data = get_test_data('raw_data')
        raw_data[0]['taxonomy'] = None

        seq_records = []
        for i in raw_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            seq_records.append(seq_record)

        dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene')
        self.assertTrue('CP100_10      ' in dataset.dataset_str)

    def test_dataset_when_seqrecord_taxonomy_is_has_family(self):
        raw_data = get_test_data('raw_data')
        raw_data[0]['taxonomy'] = {'family': 'Aussidae', 'genus': 'Aus', 'species': 'aus'}

        seq_records = []
        for i in raw_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            seq_records.append(seq_record)

        dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene')
        self.assertTrue('CP100_10_Aussidae_Aus_aus    ' in dataset.dataset_str)

    def test_generation_of_warnings(self):
        self.seq_records[0].seq = 'TTTCAGTAG'
        dataset = Dataset(self.seq_records, format='NEXUS', partitioning='by gene',
                          aminoacids=True)
        expected = "Gene ArgKin, sequence CP100_10 contains stop codons '*'"
        self.assertEqual(expected, dataset.warnings[0])

    def test_generation_of_errors(self):
        self.seq_records[0].seq = 'TTTN--CAGTAG'
        with self.assertRaises(TranslationErrorMixedGappedSeq):
            Dataset(self.seq_records, format='NEXUS', partitioning='by gene',
                    aminoacids=True)


class TestDatasetFooter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.seq_records = get_test_data('seq_records')

    def tearDown(self):
        del self.seq_records

    def test_partitioning_parameter(self):
        dataset = Dataset(self.seq_records, format='NEXUS', partitioning='by gene')
        self.assertRaises(AttributeError, DatasetFooter, data=dataset.data,
                          codon_positions='ALL', partitioning='by genes')

    def test_codon_positions_parameter(self):
        dataset = Dataset(self.seq_records, format='NEXUS', partitioning='by gene')
        self.assertRaises(AttributeError, DatasetFooter, data=dataset.data,
                          codon_positions='1st-2nd, 3rd', partitioning='by gene')

    def test_make_charset_block(self):
        dataset = Dataset(self.seq_records, format='NEXUS', partitioning='by gene')
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
        dataset = Dataset(self.seq_records, format='NEXUS', codon_positions='ALL', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected.strip(), result)

    def test_dataset_1st_2nd_codon_positions_partitioned_by_gene(self):
        seq_records = get_test_data("seq_records", "sample_data_numbers.txt")
        dataset = Dataset(seq_records, format='NEXUS', codon_positions='1st-2nd', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st2nd_codons_numbers.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_1st_2nd_codon_positions_partitioned_as_1st2nd_3rd(self):
        seq_records = get_test_data("seq_records", "sample_data_numbers.txt")
        dataset = Dataset(seq_records, format='NEXUS', codon_positions='1st-2nd', partitioning='1st-2nd, 3rd')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st2nd_codons_partitioned_as_1st2nd_3rd_numbers.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_1st_2nd_codon_positions_partitioned_as_each_codon_position(self):
        seq_records = get_test_data("seq_records", "sample_data_numbers.txt")
        dataset = Dataset(seq_records, format='NEXUS', codon_positions='1st-2nd', partitioning='by codon position')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st2nd_codons_partitioned_as_each_numbers.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)


class TestBpCount(unittest.TestCase):
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
