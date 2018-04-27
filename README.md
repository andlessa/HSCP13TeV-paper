# HSCP13TeV-paper
Material for the HSCP - 13 TeV paper
This repository holds the main code used for the HSCP 13 TeV release paper.
It is based on the 13 TeV CMS search for long-lived particles [CMS-PAS-EXO-16-036](http://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/EXO-16-036/).


## Basic Installation ##

The HSCP SModelS branch and the HSCP SModelS Database branch are already included as subtrees.
Furthermore the following codes may be useful:

  * [SPheno](https://spheno.hepforge.org/) (optional)
  * [MadGraph](https://sarah.hepforge.org/)

The script installer.sh will try to fetch the appropriate tarballs and try to install them.


## Running SModelS ##

SModelS can run as usual with the input SLHA files. However the corresponding
particles.py file ([particles-IDM](particles-IDM.py) or [particles-SUSY](particles-SUSY.py))
must be used for the respective input model.

### Computing Cross-Sections ###

The cross-sections for the MSSM scenario can be computed as usual with smodelsTools.py.
However, for the IDM model MadGraph5 must be used. Running:

``
./runGetXSecs.py -p <parameter file>
`` 

will use the parameters defined in the parameter file (see example in [xsec_parameters.ini](xsec_parameters.ini))
and run MG5 to compute the cross-sections (using the processes defined in [proc_card-IDM.dat](inputCards/proc_card-IDM.dat)).
The results will be used to generate a SLHA file with cross-sections, which can then be used as input to SModelS.

## Plotting ##

For plotting 1D histograms of excluded and allowed points:

``
./plots/plotExcHist.py
``

For plotting the contributions from each SMS topology:

``
./plots/plotTxnameHist.py
``

The input files should be ROOT files, which can be generated running [data/dataToROOT.py](data/dataToROOT.py)
and [data/slhaToROOT.py](data/slhaToROOT.py) for the SModelS output files and SLHA files.
Note that distinct options should be used for the MSSM and IDM models.

## Data ##

The data (SLHA files and SModelS output) is stored in the [data/](data/) folder
as tarballs.

## Updating SModelS ##

To update the subtrees smodels and smodels-database, run:

``
git subtree pull --prefix=smodels-database --squash git@github.com:SModelS/smodels-database.git hscp-patch
git subtree pull --prefix=smodels --squash git@github.com:SModelS/smodels.git hscp-patch
``
