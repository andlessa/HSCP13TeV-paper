# HSCP13TeV-paper
Material for the HSCP - 13 TeV paper
This repository holds the main code used for the HSCP 13 TeV release paper.
It is based on the 13 TeV and 8 TeV CMS searches for long-lived particles:

  * [CMS-PAS-EXO-16-036](http://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/EXO-16-036/)
  * [CMS-EXO-13-006](https://arxiv.org/abs/1502.02522) and [CMS-PAS-EXO-13-006](https://cds.cern.ch/record/1648902/files/EXO-13-006-pas.pdf)
  * [CMS-EXO-12-026](https://twiki.cern.ch/twiki/bin/view/CMSPublic/PhysicsResultsEXO12026)


## Basic Installation ##

The HSCP SModelS branch and the HSCP SModelS Database branch are already included as subtrees.
Furthermore the following codes may be useful:

  * [MadGraph](https://launchpad.net/mg5amcnlo)

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


### Generating MSSM SLHA files ###

In order to scan the MSSM parameter space, SPheno must be installed.
The file [runRandomScan.py](runRandomScan.py) illustrates how to run a random
scan over the desired MSSM parameters within specified ranges.


For optimizing some observable using a simple MCMC scan, see the example file
[runMCMCWalk.py](runMCMCWalk.py)

These files also illustrate how to make simple plots of the scans.

## Analysing Results and Plotting ##

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
