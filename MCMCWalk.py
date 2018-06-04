#!/usr/bin/env python



""".. module:: MCMCWalk.
        :synopsis: Simple MCMC code to find points in the MSSM parameter space
                   in order to maximize a given observable (likelihood)

.. moduleauthor:: Andre Lessa
"""

import numpy as np
import random,os,pyslha
import logging as logger
import matplotlib.pyplot as plt
import itertools,copy
import tempfile
from scanHelpers import getSpectrum,getInputFile,pars2x,x2pars
  

def getNextStep(x0,sigma=10.):
    """
    Generates the next parameter space point
    starting from the x0 point according to a normal
    distribution centered on zero with width sigma.
    
    :param x0: 1-D numpy array with the point in parameter space
    :param sigma: width of the normal distribution
    
    :return: 1-D numpy array with the next point
    """
    
    x = np.array([random.normalvariate(xv,sigma) for xv in x0])    
    return x    

def getLikelihood(y):
    """
    Compute the likelihood for the value y.
    
    :param y: value of observable (float)    
    :return: likelihood value (float)
    """
    
    if y is None:
        return None
    
    likelihood = 1./((abs(y)/1e-15) + 1.)
    
    return likelihood

def acceptPoint(x,y,L0,fakeEff=0.05,xmin=100.,xmax=None):
    """
    Checks if the new point should be accepted or not.
    The new point is accepted if likelihood(x) > oldLikelihood
    or in fakeEff percent of the cases.
    
    :param x: parameter space point (1-D numpy array)
    :param y: value of observable (float)    
    :param L0: likelihood for the previous point (float)
    :param fakeEff: fraction of smaller likelihood point which are accepted (float)
    :param xmin: Minimum value for any value in x
    :param xmax: Maximum value for any value in x
    
    :return: True/False
    
    """
    
    if not xmin is None and min(abs(x)) < xmin:
        return False
    if not xmax is None and max(abs(x)) > xmax:
        return False
    
    L = getLikelihood(y)
    if L is None:
        return False
    elif L > L0:
        return True
    elif random.random() < fakeEff:
        return True
    else:
        return False        

def walk(yExpr,pars0,npts=100,ntries=100,fakeEff=0.05,sigmaStep=50.,
        outdir=None,templateFile='MSSM_scan.in'):
    """
    Walk in parameter space starting from the parameter point x0, till it generates npts
    good points.
    
    :param yExpr: expression for computing the y observable (to be optimized) in string format  (e.g. 'decays[1000024].totalwidth')
    :param pars0: dictionary with parameters for initial point (e.g. {'EXTPAR' : { 1 : 100., 2: 300., 23: 500}}) 
    :param npts: total number of points to be generated (int)
    :param ntries: maximum number of tries (int)
    :param fakeEff: fraction of smaller likelihood point which are accepted (float)
    :param sigmaStep: Width for the nextStep draw function (float)
    :param outdir: output folder. If None, the generated files will not be stored
    :param templateFile: Path to the template input file
    
    
    :return: 2-D array with each acceptable point and its likelihood
    
    """

    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    
    chain = []
    inputTemplate = pyslha.readSLHAFile(templateFile,
                                        ignorenomass=True,ignorenobr=True)
    
    slhaInput = getInputFile(pars0,inputTemplate)
    if not slhaInput:
        logger.error('Error generating file for initial parameters: %s' %str(pars0))
        return np.array(chain)
    
    outfile = None
    if outdir:
        outfile = tempfile.mkstemp(prefix='mcmc_%i_'%len(chain),
                                           suffix='.slha',dir=outdir)
        os.close(outfile[0])
        outfile = outfile[1]
        os.remove(outfile)
        
    slhaData = getSpectrum(slhaInput,outfile)
    if not slhaData:
        logger.error("Error computing spectrum for initial point")
        return False
    
    os.remove(slhaInput)
    x0 = pars2x(pars0)
    try:
        y = eval(yExpr,slhaData.__dict__)
    except:
        logger.error("Error evaluating y-observable. Is the expression given by yExpr correct?")
        return False
    
    L0 = getLikelihood(y)
    if L0 is None:
        logger.error('Likelihood calculation fails for the initial point')
        return np.array(chain)
    
    ntry = 0
    pars = copy.deepcopy(pars0)
    while len(chain) < npts and ntry < ntries:
        ntry += 1
        x = getNextStep(x0,sigmaStep)
        pars = x2pars(x.tolist(), pars)
        slhaInput = getInputFile(pars,inputTemplate)
        slhaData = getSpectrum(slhaInput)
        os.remove(slhaInput)
        if slhaData is None:
            continue
        y = eval(yExpr,slhaData.__dict__)            
        if acceptPoint(x,y,L0,fakeEff):
            if outdir:
                outfile = tempfile.mkstemp(prefix='mcmc_%i_'%len(chain),
                                           suffix='.slha',dir=outdir)
                os.close(outfile[0])
                outfile = outfile[1]
                os.remove(outfile)
                pyslha.write(outfile,slhaData)
            ntry = 0
            L0 = getLikelihood(y)
            x0 = x
            y0 = y            
            chain.append(np.append(x0,y0))
    
    return np.array(chain)


def plotChain(chain,pars,doLog=True,doLines=True):
    
    ndim = len(pars)
    plt.figure(figsize=(15,15))
    nplot = 401+10*ndim
    if doLog:
        Y = np.log10(chain[:,-1])
    else:
        Y = chain[:,-1]
    cm = plt.cm.get_cmap('RdYlBu')
    for var1,var2 in itertools.product(pars,pars):
        ix = pars.index(var1)
        iy = pars.index(var2)
        if ix >= iy:
            continue
        plt.subplot(nplot)                    
        plt.scatter(chain[:,ix],chain[:,iy],c=Y,s=50,vmin=min(Y),vmax=max(Y),cmap=cm)
        if doLines:
            plt.plot(chain[:,ix],chain[:,iy],'--')
        plt.colorbar()
        plt.xlabel(var1)
        plt.ylabel(var2)
        nplot += 1  
    
    plt.show()
