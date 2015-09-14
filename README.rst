=========================================
Dataset creator for phylogenetic software
=========================================

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls|
        | |scrutinizer|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/dataset-creator/badge/?style=flat
    :target: https://readthedocs.org/projects/dataset-creator
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/carlosp420/dataset-creator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/carlosp420/dataset-creator

.. |requires| image:: https://requires.io/github/carlosp420/dataset-creator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/carlosp420/dataset-creator/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/carlosp420/dataset-creator/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/carlosp420/dataset-creator
.. |version| image:: https://img.shields.io/pypi/v/dataset_creator.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/dataset_creator

.. |downloads| image:: https://img.shields.io/pypi/dm/dataset_creator.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/dataset_creator

.. |wheel| image:: https://img.shields.io/pypi/wheel/dataset_creator.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/dataset_creator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dataset_creator.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/dataset_creator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dataset_creator.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/dataset_creator

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/carlosp420/dataset-creator/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/carlosp420/dataset-creator/

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
    >>> dataset = Dataset(seq_records, format='NEXUS', partitioning='by gene')
    >>> print(dataset.str)
    """#NEXUS
    blah blah
    """



Development
===========

To run the all tests run::

    tox
