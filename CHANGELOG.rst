Changelog
=========
0.3.7 (2015-10-30)
------------------
* Fixed 2nd, 3rd codon positions bug that returned empty FASTA datasets.

0.3.6 (2015-10-30)
------------------
* Fixed 3rd codon positions bug that returned FASTA datasets with 3rd codon
  positions even if they were not needed.

0.3.5 (2015-10-29)
------------------
* If user provides outgroup, then TNT datasets will place its sequences in first
  position in the dataset blocks.

0.3.4 (2015-10-02)
------------------
* Fixed bug that did not show DATATYPE=PROTEIN in Nexus files when aminoacid
  sequences were requested by user.

0.3.3 (2015-10-02)
------------------
* Fixed bug that raised an exception when SeqExpandedRecords did not have data
  in the ``taxonomy`` field.

0.3.2 (2015-10-01)
------------------
* Fixed bug that raised an exception when user wanted partitioned dataset as
  1st-2nd and 3rd codon positions of only one codon.

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
