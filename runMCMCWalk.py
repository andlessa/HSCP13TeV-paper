#!/usr/bin/env python



""".. module:: runMCMCWalk.
        :synopsis: Simple example of how to run the MCMC code for scanning the MSSM parameter space

.. moduleauthor:: Andre Lessa
"""


from MCMCWalk import walk,plotChain
import numpy as np


#Select a point to run:
scanPoints = np.loadtxt('./data/gauginos/slha_tanb10/summary.txt',comments='#',usecols=(0,1,2))
Yvalues = np.loadtxt('./data/gauginos/slha_tanb10/summary.txt',comments='#',usecols=(3))
slhaFiles = np.loadtxt('./data/gauginos/slha_tanb10/summary.txt',comments='#',usecols=(4),dtype='str')
subset = scanPoints[Yvalues<1e-14]
Ysubset = Yvalues[Yvalues<1e-14]
slhaSubset = slhaFiles[Yvalues<1e-14]
x = subset[0]
#Define the MCMC input paramaters:
npts = 10
fakeEff = 0.05
sigmaStep = 0.5
ntries = 100
pars = {'EXTPAR' : {1: x[1], 2: x[2], 23 : [0]}}
yExpr='decays[1000024].totalwidth'
chain = walk(yExpr,pars,npts,ntries,fakeEff,sigmaStep,'./data/gauginos/slha_tanb10/mcmc_%i'%0,'./data/gauginos/MSSM_scan.in')
#Plot Results:
plotChain(chain)