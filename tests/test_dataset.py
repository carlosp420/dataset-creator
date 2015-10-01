import json
import os
import unittest

from seqrecord_expanded import SeqRecordExpanded

from dataset_creator import Dataset
from .data import test_data


NEXUS_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Nexus')


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_extract_genes(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.gene_codes
        self.assertEqual(expected, result)

    def test_extract_number_of_chars(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '4739'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_wrong_argument(self):
        self.assertRaises(AttributeError,
                          Dataset, test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='5th position')

    def test_extract_number_of_chars_first_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='1st')
        expected = '1580'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_second_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='2nd')
        expected = '1578'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_third_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='3rd')
        expected = '1581'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_first_and_second_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='1st-2nd')
        expected = '3158'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_taxa(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)

    def test_prepared_data(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.data.gene_codes
        self.assertEqual(expected, result)

    def test_dataset_nexus(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_using_default_parameters(self):
        dataset = Dataset(test_data, format='NEXUS')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_wrong_partitioning_parameter(self):
        self.assertRaises(AttributeError, Dataset, seq_records=test_data, format='NEXUS',
                          codon_positions='1st', partitioning='1st-2nd-3rd')

    def test_dataset_nexus_1st_codon_position(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='1st', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st_codon.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_3rd_codon_position(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='3rd', partitioning='by codon position')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_3rd_codon.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_3rd_codon_position_partitioned_as_1st2nd_3rd(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='3rd', partitioning='1st-2nd, 3rd')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_3rd_codon.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_all_codon_positions_partitioned_by_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL', partitioning='by codon position')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_partitioned_as_each.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_all_codon_positions_partitioned_as_1st2nd_3rd(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL', partitioning='1st-2nd, 3rd')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_partitioned_as_1st2nd_3rd.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_with_gene_missing_reading_frame(self):
        SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')
        with open(SAMPLE_DATA_PATH, 'r') as handle:
            sample_data = json.loads(handle.read())

        data = []
        append = data.append
        for i in sample_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            if i['gene_code'] == 'ArgKin':
                seq_record.reading_frame = None
            append(seq_record)

        self.assertRaises(ValueError, Dataset, data, format='NEXUS', codon_positions='ALL',
                          partitioning='1st-2nd, 3rd', aminoacids=True)

    def test_degenerate(self):
        SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')
        with open(SAMPLE_DATA_PATH, 'r') as handle:
            sample_data = json.loads(handle.read())

        data = []
        append = data.append
        for i in sample_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            append(seq_record)

        with open(os.path.join(NEXUS_DATA_PATH, 'dataset_degenerated.nex'), 'r') as handle:
            expected = handle.read().strip()

        dataset = Dataset(data, format='NEXUS', codon_positions='ALL',
                          partitioning='by gene', degenerate='S')
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_using_outgroup(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL',
                          outgroup='CP100-19')
        expected = 'outgroup CP100-19_Aus_jus;'
        result = dataset.dataset_str
        self.assertTrue(expected in result)
