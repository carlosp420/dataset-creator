import json
import os

from seqrecord_expanded import SeqRecordExpanded




def get_test_data(filename="sample_data.txt"):
    SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    with open(SAMPLE_DATA_PATH, 'r') as handle:
        sample_data = json.loads(handle.read())
    data = []
    append = data.append

    for i in sample_data:
        seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                       taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                       reading_frame=i['reading_frame'], table=i['table'])
        append(seq_record)
    return data
