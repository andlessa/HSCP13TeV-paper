
# coding: utf-8

# In[9]:


import numpy as np
import random,os,pyslha,glob
import logging as logger
import matplotlib.pyplot as plt
import itertools,copy
import tempfile
from getSpectrum import getInputFile,getSpectrum,x2pars,pars2x


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


def getPoints(parsExpr,slhaFolder):
    """
    Reads all SLHA files in the slhaFolder and returns list of points
    with the values for the parameters defined in pars.
    
    :param parsExpr: list of string expressions for computing the desired parameters
                      (e.g. ['blocks['EXTPAR'][23],'blocks['EXTPAR'][1]','blocks['EXTPAR'][2]','decays[1000024].totalwidth'])    
    :param parsRanges: dictionary with parameters and their ranges 
                       (e.g. {'EXTPAR' : { 1 : [100.,1000.], 2: [300.,1000.], 23: [500,1000]}}) 
    :param npts: total number of points to be generated (int)
    :param outdir: output folder. If None, the generated files will not be stored
    :param inputTemplate: Path to the template input file
    
    :return: 2-D array with each point, its corresponding y-value and a 1-D array with the corresponding file names
    
    """
    
    points = []
    slhaFiles = []
    for slhafile in glob.glob(slhaFolder+'/*.slha'):
        data = pyslha.readSLHAFile(slhafile)
        x = np.array([eval(expr,data.__dict__) for expr in parsExpr])
        points.append(x)
        slhaFiles.append(os.path.basename(slhafile))
    return np.array(points),np.array(slhaFiles)


def writeSummary(points,header,outfile,slhaFiles=None):
    """
    Writes a simple multi-column text summary of the points.
    
    :param points: 2-D array with the points to be written
    :param header: List of headers. Should match the dimensions of a single point
    :param outfile: Output file name
    :slhaFiles: 1-D array with the corresponding list of file names (optional)
    
    """
    
    
    summary = open(outfile,'w')
    h = header[:]    
    if not slhaFiles is None:
        h.append('slhafile')
    col_width = max(15,max([len(hname) for hname in h])) + 3  # padding            
    summary.write('#'+"".join(hname.ljust(col_width) for hname in h)+'\n')
    for i,pt in enumerate(points):
        if not slhaFiles is None:
            summary.write(' '+"".join(("%.4e" %(v)).ljust(col_width) for v in pt)+slhaFiles[i]+' \n')
        else:
            summary.write(' '+"".join(("%.4e" %(v)).ljust(col_width) for v in pt)+' \n')

    summary.close()

def plotScan(scanPoints):
    
    pars = ['mu (GeV)','M1 (GeV)','M2 (GeV)']
    ndim = len(pars)
    plt.figure(figsize=(15,15))
    nplot = 401+10*ndim
    Y = np.log10(scanPoints[:,-1])
    cm = plt.cm.get_cmap('RdYlBu')
    for var1,var2 in itertools.product(pars,pars):
        ix = pars.index(var1)
        iy = pars.index(var2)
        if ix >= iy:
            continue
        plt.subplot(nplot)                    
        plt.scatter(scanPoints[:,ix],scanPoints[:,iy],c=Y,s=50,vmin=min(Y),vmax=max(Y),cmap=cm)
        plt.colorbar()
        plt.xlabel(var1)
        plt.ylabel(var2)
        nplot += 1  
    
    plt.show()


# 
# def plotScan3D(scanPoints):
#     
#     pars = ['mu (GeV)','M1 (GeV)','M2 (GeV)']
#     cm = plt.cm.get_cmap('RdYlBu')
#     fig = plt.figure(figsize=(15,15))
#     Y = np.log10(scanPoints[:,-1])
#     ax = Axes3D(fig)
#     ax.scatter(scanPoints[:,0],scanPoints[:,1],scanPoints[:,2],c=Y,s=50,vmin=min(Y),vmax=max(Y),cmap=cm)
#     ax.set_xlabel(pars[0])
#     ax.set_ylabel(pars[1])
#     ax.set_zlabel(pars[2])
#     plt.show()
