Usage
=====

1. Create an **aminoacid dataset** from your nucleotide sequences:

.. code-block:: python

    >>> Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...         aminoacids=True)

2. Create dataset with **degenerated nucleotide** sequences using the method by
`Zwick et al. <http://www.phylotools.com/ptdegenoverview.htm>`_:

.. code-block:: python

    >>> # degenerate method can be 'S', 'Z', 'SZ' and 'normal'
    >>> Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...         degenerate='S')

3. Create dataset specifying the **outgroup** by its voucher code:

.. code-block:: python

    >>> Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...         outgroup='CP100-10)

