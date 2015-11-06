User's Guide
============

1. ``dataset-creator`` needs a list of SeqRecordExpanded objects::

.. code-block:: python

    >>> from seqrecord_expanded import SeqRecord
    >>>
    >>> # `table` is the Translation Table code based on NCBI
    >>> seq_record1 = SeqRecord('ACTACCTA', reading_frame=2, gene_code='RpS5',
    ...                         table=1, voucher_code='CP100-10',
    ...                         taxonomy={'genus': 'Aus', 'species': 'bus'})
    >>>
    >>> seq_record2 = SeqRecord('ACTACCTA', reading_frame=2, gene_code='RpS5',
    ...                         table=1, voucher_code='CP100-10',
    ...                         taxonomy={'genus': 'Aus', 'species': 'bus'})
    >>>
    >>> seq_record3 = SeqRecord('ACTACCTA', reading_frame=2, gene_code='wingless',
    ...                         table=1, voucher_code='CP100-10',
    ...                         taxonomy={'genus': 'Aus', 'species': 'bus'})
    >>>
    >>> seq_record4 = SeqRecord('ACTACCTA', reading_frame=2, gene_code='winglesss',
    ...                         table=1, voucher_code='CP100-10',
    ...                         taxonomy={'genus': 'Aus', 'species': 'bus'})
    >>>
    >>> seq_records = [
    ...    seq_record1, seq_record2, seq_record3, seq_record4,
    ... ]


2. Create an **aminoacid dataset** from your nucleotide sequences:

.. code-block:: python

    >>> from dataset_creator import Dataset
    >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...                   codon_positions='ALL', aminoacids=True)

3. Create dataset with **degenerated nucleotide** sequences using the method by
`Zwick et al. <http://www.phylotools.com/ptdegenoverview.htm>`_:

.. code-block:: python

    >>> # The degenerate method can be 'S', 'Z', 'SZ' and 'normal'
    >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...                   codon_positions='ALL', degenerate='S')

4. Create dataset specifying the **outgroup** by its voucher code:

.. code-block:: python

    >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...                   outgroup='CP100-10)

5. Codon positions can be ``1st``, ``2nd``, ``3rd``, ``1st-2nd``, ``ALL`` (default).

.. code-block:: python

    >>> dataset = Dataset(seq_records, format='TNT', partitioning='by codon position',
    ...                   codon_positions='ALL')

    >>> dataset = Dataset(seq_records, format='PHYLIP', partitioning='1st-2nd, 3rd',
    ...                   codon_positions='ALL')

    >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...                   codon_positions='1st')

6. The dataset is returned as a string:

.. code-block:: python

    >>> print(dataset.dataset_str)
    #NEXUS
    blah blah ...

API Guide
=========

.. include:: dataset_creator.rst
