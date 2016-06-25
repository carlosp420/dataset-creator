Changelog
=========

0.3.11 (2016-06-25)
-------------------
* Upgraded seqrecord-expanded requirement.

0.3.10 (2015-12-01)
-------------------
* Fixed bug that produced FASTA sequences with underscores. Now all voucher codes
  will have their dashes replaced by underscores.

0.3.9 (2015-11-06)
------------------
* Create datasets using the GenBankFASTA format. This format has the following
  extra info in the description of sequences:
  >Aus_aus_CP100-10 [org=Aus aus] [Specimen-voucher=CP100-10] [note=ArgKin gene, partial cds.] [Lineage=]

0.3.8 (2015-10-30)
------------------
* Fixed making dataset as aminoacid seqs for MEGA format.
* Fixed making dataset as degenerated seqs for MEGA format.
* Fixed making dataset as degenerated seqs for TNT format.
* Fixed making dataset as aa seqs with specified outgroup for TNT format.
* Raise ValueError when asked to degenerate seqs that will go to partitioning
  based on codon positions.
* Dataset creator returns warnings if translated sequences have stop codons '*'.
* Cannot generate MEGA datasets with partitioning.

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
