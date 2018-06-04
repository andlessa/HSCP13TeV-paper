
# coding: utf-8

# In[9]:


import numpy as np
import random,os,pyslha
import logging as logger

import copy
import tempfile
from scanHelpers import getInputFile,getSpectrum,x2pars,pars2x


def scan(yExpr,parRanges,npts=100,outdir=None,inputTemplate='MSSM_scan.in'):
    """
    Performs a random scan of the parameter space within the ranges
    degined in parRanges
    
    :param yExpr: expression for computing the y observable (to be optimized) in string format  (e.g. 'decays[1000024].totalwidth')    
    :param parsRanges: dictionary with parameters and their ranges 
                       (e.g. {'EXTPAR' : { 1 : [100.,1000.], 2: [300.,1000.], 23: [500,1000]}}) 
    :param npts: total number of points to be generated (int)
    :param outdir: output folder. If None, the generated files will not be stored
    :param inputTemplate: Path to the template input file
    
    :return: 2-D array with each point and its corresponding y-value
    
    """
    
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    
    
    if not len(pars2x(parRanges))%2 == 0:
        logger.error("Parameter ranges are not properly defined")
        return False
    
    #Get limits for the scan:
    pars = copy.deepcopy(parRanges)    
    xmin = pars2x(parRanges)[0::2]
    xmax = pars2x(parRanges)[1::2]
    
    points = []
    while len(points) < npts:
        x = np.array([random.uniform(xm,xmax[i]) for i,xm in enumerate(xmin)])
        if min(abs(x)) < 100.:
            continue
        pars = x2pars(x.tolist(), pars)
        slhaInput = getInputFile(pars,inputTemplate)
        slhaData = getSpectrum(slhaInput)
        os.remove(slhaInput)
        if slhaData is None:
            continue
        try:
            y = eval(yExpr,slhaData.__dict__)
        except:
            raise Exception("Error evaluating y-observable. Is the expression given by yExpr correct?")

        if outdir:
            outfile = tempfile.mkstemp(prefix='point_%i_'%len(points),
                                       suffix='.slha',dir=outdir)
            os.close(outfile[0])
            outfile = outfile[1]
            os.remove(outfile)
            pyslha.write(outfile,slhaData)
        points.append(np.append(x,y))
            
    return np.array(points)

