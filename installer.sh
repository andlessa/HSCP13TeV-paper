#!/bin/bash

homeDIR="$( pwd )"


sphenoDir=$homeDIR/"SPheno"
madDir=$homeDIR/"MadGraph"

echo "Install SPheno? (y/n)"
read ins
if [ "$ins" == "y" ]; then
    #Get SPheno tarball
    spheno="SPheno-4.0.3.tar.gz"
    URL=http://www.hepforge.org/archive/spheno/$spheno
    mkdir $sphenoDir
    echo "[installer] getting SPheno"; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $spheno -C $sphenoDir --strip-components=1;
    echo "[installer] installing SPheno"; cd $sphenoDir; sed -i -e "s/F90 = ifort/F90 = gfortran/" Makefile; make; #The Makefile needs this fix
    cd $homeDIR;
    rm $spheno;
fi

echo "Install MadGraph? (y/n)"
read ins
if [ "$ins" == "y" ]; then
    #Get MadGraph
    mad="MG5_aMC_v2.6.0.tar.gz"
    URL=https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/$mad
    mkdir $madDir
    echo "[installer] getting MadGraph"; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $mad -C $madDir --strip-components=1;
    mkdir $madDir/models/$MODEL
    cp $homeDIR/mg5_configuration.txt $madDir/input/
    cd $homeDIR;
    rm $mad;
fi


echo "DONE"
