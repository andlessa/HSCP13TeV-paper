#!/usr/bin/env python



""".. module:: runRandomScan.
        :synopsis: Simple example of how to run the RandomScan code for scanning the MSSM parameter space

.. moduleauthor:: Andre Lessa
"""


from RandomScan import scan,plotScan,writeSummary,getPoints 
import numpy as np
import os
import multiprocessing
import time



t0 = time.time()
ncpus = 4
npts = 100
pool = multiprocessing.Pool(processes=ncpus)

parRanges = {'EXTPAR' : {1: [-3000.,3000.], 2: [-3000.,3000.], 23 : [-3000.,3000.]}}
yExpr='decays[1000024].totalwidth'
outdir = './test_scan'
inputTemplate='./data/gauginos/MSSM_scan.in'
args = (yExpr,parRanges,npts,outdir,inputTemplate,)
children = [pool.apply_async(scan, args=args) for i in range(ncpus)]
points = children[0].get()
for p in children[1:]:
    points = np.concatenate((points,p.get()))
print('done in',(time.time()-t0)/60., 'min (real)')

plotScan(points)
 
 
print(min(points[:,-1]))
print(len(points[points[:,-1]<1e-2]))
 
subset = points[points[:,-1]<1e-14]
subset = subset[subset[:,-1]>1e-22]
plotScan(subset)
print(len(subset))
 
parsExpr = ["blocks['EXTPAR'][23]","blocks['EXTPAR'][1]","blocks['EXTPAR'][2]","decays[1000024].totalwidth"]
slhaFolder = outdir
points,slhaFiles = getPoints(parsExpr,slhaFolder)
header = ['mu (GeV)', 'M1 (GeV)', 'M2 (GeV)', 'Width (GeV)']
outfile = os.path.join(slhaFolder,'summary.txt')
writeSummary(points,header,outfile,slhaFiles=slhaFiles)

