# HSCP13TeV-paper
Material for the HSCP - 13 TeV paper
This repository holds the main code used for the HSCP 13 TeV release paper.
It is based on the 13 TeV CMS search for long-lived particles [CMS-PAS-EXO-16-036](http://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/EXO-16-036/).


## Basic Installation ##

The HSCP SModelS branch and the HSCP SModelS Database branch are already included as subtrees.
Furthermore the following codes may be useful:

  * [SPheno](https://spheno.hepforge.org/)
  * [MadGraph](https://sarah.hepforge.org/)

The script installer.sh will try to fetch the appropriate tarballs and try to install them.


## Running ##

Not for now

## Plotting ##

Not for now


## Updating SModelS ##

To update the subtrees smodels and smodels-database, run:

``
git subtree pull --prefix=smodels-database --squash git@github.com:SModelS/smodels-database.git hscp-patch
git subtree pull --prefix=smodels --squash git@github.com:SModelS/smodels.git hscp-patch
``
