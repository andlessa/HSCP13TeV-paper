#!/bin/sh

homeDIR="$( pwd )"


sphenoDir=$homeDIR/"SPheno"
madDir=$homeDIR/"MadGraph"

echo "Install SPheno? (y/n)"
read answer
if echo "$answer" | grep -iq "^y" ;then    #Get SPheno tarball
    spheno="SPheno-4.0.3.tar.gz"
    URL=http://www.hepforge.org/archive/spheno/$spheno
    mkdir $sphenoDir
    echo "[installer] getting SPheno"; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $spheno -C $sphenoDir --strip-components=1;
    echo "[installer] installing SPheno"; cd $sphenoDir; sed -i -e "s/F90 = ifort/F90 = gfortran/" Makefile; make; #The Makefile needs this fix
    cd $homeDIR;
    rm $spheno;
fi

madgraph="MG5_aMC_v2.6.2.tar.gz"
URL=https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/$madgraph
echo -n "Install MadGraph (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then
	mkdir MG5;
	echo "[installer] getting MadGraph5"; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $madgraph -C MG5 --strip-components 1;
	cd $homeDIR
	rm $madgraph;
	echo "[installer] replacing MadGraph files with fixes";
    cp ./madgraphFixes/mg5_configuration.txt MG5/input/;
    cp ./madgraphFixes/madgraph_interface.py MG5/madgraph/interface/;
fi

spheno="SPheno-4.0.3.tar.gz"
URL=http://www.hepforge.org/archive/spheno/$spheno
echo -n "Install SPheno (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then
	mkdir SPheno;
	echo "[installer] getting SPheno"; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $spheno -C SPheno --strip-components 1;
	echo "[installer] installing SPheno";
    cd SPheno;
    sed -i '/.*F90 =/s/.*/F90 = gfortran/' Makefile;
    make;
	cd $homeDIR;
	rm $spheno;
fi


echo "DONE"
