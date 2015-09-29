Usage
=====

Create an aminoacid dataset from your nucleotide sequences:

.. code-block:: python

    >>> Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...         aminoacids=True)
