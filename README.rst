=========================================
Dataset creator for phylogenetic software
=========================================

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |requires| |coveralls|
        | |quantified-code|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations|

.. |travis| image:: https://travis-ci.org/carlosp420/dataset-creator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/carlosp420/dataset-creator

.. |requires| image:: https://requires.io/github/carlosp420/dataset-creator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/carlosp420/dataset-creator/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/carlosp420/dataset-creator/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/carlosp420/dataset-creator

.. |version| image:: https://img.shields.io/pypi/v/dataset-creator.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/dataset-creator

.. |wheel| image:: https://img.shields.io/pypi/wheel/dataset-creator.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/dataset-creator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dataset-creator.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/dataset-creator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dataset-creator.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/dataset-creator

.. |quantified-code| image:: https://www.quantifiedcode.com/api/v1/project/f059ab475f2547758722b80ea528c457/badge.svg
  :target: https://www.quantifiedcode.com/app/project/f059ab475f2547758722b80ea528c457
  :alt: Code issues

Takes SeqRecordExpanded objects and creates datasets for phylogenetic software

* Free software: BSD license

Installation
============

::

    pip install dataset_creator

Usage
=====
.. code-block:: python

    >>> from seqrecord_expanded import SeqRecord
    >>> from dataset_creator import Dataset
    >>>
    >>> seq_record1 = SeqRecord('ACTACCTA')
    >>> seq_record2 = SeqRecord('ACTACCTA')
    >>>
    >>> seq_records = [
    ...    seq_record1, seq_record2,
    ... ]
    >>> # codon positions can be 1st, 2nd, 3rd, 1st-2nd, ALL (default)
    >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene',
    ...                   codon_positions='1st',
    ...                   )
    >>> print(dataset.str)
    """#NEXUS
    blah blah
    """



Development
===========

To run the all tests run::

    tox
