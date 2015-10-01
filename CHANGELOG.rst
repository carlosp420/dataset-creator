Changelog
=========

0.3.1 (2015-10-01)
------------------
* Fixed bug that raised an exception when user wanted partitioned dataset by
  codon positions of only one codon.

0.3.0 (2015-10-01)
------------------
* Accepts voucher code as string that will be used to generate the outgroup
  string needed for NEXUS and TNT files.

0.2.0 (2015-09-30)
------------------
* Creates datasets as degenerated sequences using the method by Zwick et al.

0.1.1 (2015-09-30)
------------------

* It will issue errors if reading frames are not specified unless they
  are strictly necessary to build the dataset (datasets need to be divided by
  codon positions).
* Added documentation using sphinx-doc
* Creates datasets as aminoacid sequences.

0.1.0 (2015-09-23)
------------------

* Creates Nexus, Tnt, Fasta, Phylip and Mega dataset formats.

0.0.1 (2015-06-10)
------------------

* First release on PyPI.
