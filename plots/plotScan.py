#!/usr/bin/env python

""".. module:: plotScan.
        :synopsis: Functions for plotting a scan using matplotlib

.. moduleauthor:: Andre Lessa
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib as mpl
import pyslha,glob,os,imp
import argparse,copy
import logging as logger
        


def getSLHAPoints(parsExpr,slhaFolder,nmax=-1):
    """
    Reads all SLHA files in the slhaFolder and returns list of points
    with the values for the parameters defined in pars.
    
    :param parsExpr: list of string expressions for computing the desired parameters
                      (e.g. ['blocks['EXTPAR'][23],'blocks['EXTPAR'][1]','blocks['EXTPAR'][2]','decays[1000024].totalwidth'])
    :param slhaFolder: Path to the folder containing slha files  or a list of SLHA files  
    :param nmax: Option to set the maximum number of points. If nmax > 0, only the first nmax points will be read.    
    
    :return: 2-D array with each point, its corresponding y-value and a 1-D array with the corresponding file names
    
    """
    
    if isinstance(slhaFolder,str) and os.path.isdir(slhaFolder):
        slhaF = glob.glob(slhaFolder+'/*.slha')
    else:
        slhaF = slhaFolder
    
    points = []
    slhaFiles = []
    for slhafile in slhaF:
        if nmax > 0 and len(points) > nmax:
            break
        if not os.path.isfile(slhafile):
            logger.error("File %s not found" %slhafile)
            break
        
        data = pyslha.readSLHAFile(slhafile)
        if isinstance(parsExpr,list):
            x = np.array([eval(expr,globals(),data.__dict__) for expr in parsExpr])
        else:
            x = eval(parsExpr,data.__dict__)
        points.append(x)
        slhaFiles.append(os.path.basename(slhafile))
    return np.array(points),np.array(slhaFiles)

def getPointsFrom(pyFolder,objName,parsExpr,nmax=-1):
    """
    Reads python files containing the object objName and returns
    a list of points with the values for the parameters defined in pars.
    
    :param pyFolder: Path to the folder containing python files (*.py)  or a list of files
    :param objName: Name of object to be retrieved from each file (e.g. "smodelsOutput")
    :param parsExpr: list of string expressions for computing the desired parameters
                      (e.g. ["ExptRes", "OutputStatus['input file']"),...])
        
    :param nmax: Option to set the maximum number of points. If nmax > 0, only the first nmax points will be read.    
    
    :return: 2-D array with each point, its corresponding y-value and a 1-D array with the corresponding file names
    
    """

    points = []
    pyFiles = []
    filesRead = []
    
    if isinstance(pyFolder,str) and os.path.isdir(pyFolder):
        pyFiles = glob.glob(pyFolder+'/*.py')
    else:
        pyFiles = pyFolder
    
    for f in pyFiles:
        if nmax > 0 and len(points) > nmax:
            break
        if not os.path.isfile(f):
            logger.error("File %s not found" %f)
            break
        mod = imp.load_source(os.path.basename(f).replace('.py',''),f)        
        dataDict = getattr(mod,objName)
        try:
            if isinstance(parsExpr,list):
                x = np.array([eval(expr,globals(),dataDict) for expr in parsExpr])
            else:
                x = eval(parsExpr,globals(),dataDict)
            points.append(x)
        except:
            points.append(None)
        filesRead.append(os.path.basename(f))

    try:
        points = np.array(points)
    except:
        pass

    return points,np.array(filesRead)



def getSModelSPoints(parsExpr,smodelsFolder,nmax=-1):
    """
    Reads all SModelS files in the smodelsFolder and returns list of points
    with the values for the parameters defined in pars.
    
    :param parsExpr: list of string expressions for computing the desired parameters
                      (e.g. ["max([x['theory prediction (fb)']/x['upper limit (fb)'] for x in ExptRes])",
                             "sorted(ExptRes, key = lambda x: x['theory prediction (fb)']/x['upper limit (fb)'])[-1]"] )
    :param smodelsFolder: Path to the folder containing smodels files (*.py)  or a list of smodels files    
    :param nmax: Option to set the maximum number of points. If nmax > 0, only the first nmax points will be read.    
    
    :return: 2-D array with each point, its corresponding y-value and a 1-D array with the corresponding file names
    
    """
    
   
    return getPointsFrom(smodelsFolder, objName='smodelsOutput', parsExpr=parsExpr, nmax=nmax)


def getContour(xpts,ypts,zpts,levels):
    """
    Uses pyplot tricontour method to obtain contour
    curves in a 2D plane.

    :return: A dictionary with a list of contours for each level
    """
    
    fig = plt.figure()
    x = copy.deepcopy(xpts)
    y = copy.deepcopy(ypts)
    z = copy.deepcopy(zpts)
    CS = plt.tricontour(x,y,z,levels=levels)
    levelPts = {}
    for il,level in enumerate(CS.levels):
        levelPts[level] = []
        c = CS.collections[il]        
        paths = c.get_paths()
        for path in paths:
            levelPts[level].append(path.vertices)
    plt.close(fig)
    
    return levelPts



def plotScan(points,axes,coloraxis=None,doLog=True,doLines=False):
    """
    Makes 2D scatter plots with the points using all the axes combinations in the dictionary axes.
    If defined, the coloraxis variable will be plotted as a colorbar.
    
    :param points: 2-D numpy array with list of points
    :param axes: Dictionary with the axes labels and their corresponding index in a point
                 (e.g. {'mu' : 0, 'M2' : 2, 'M1' : 1})
    :param coloraxis: Dictionary with axis label and its index to be plotted in the color bar
                  (e.g. {'Width' : -1})
                  norm=LogNorm(vmin=Z.min(), vmax=Z.max())
    :param doLog: If True will plot the colorbar in log scale
    
    :param doLines: If True will add lines to the points.
    
    :return: pyplot fig object
    
    """
    
    nplots = ((len(axes)*(len(axes)-1))/2)
    if coloraxis:
        nplots *= len(coloraxis)
    nrows = int(np.floor(nplots**0.5).astype(int))
    ncolumns = int(np.ceil(1.*nplots/nrows).astype(int))
    fig = plt.figure()
    cm = plt.cm.get_cmap('RdYlBu')
    iplot = 1
    for var1,var2,cvar in itertools.product(axes.keys(),axes.keys(),coloraxis.keys()):
        ix = axes[var1]
        iy = axes[var2]
        if ix >= iy:
            continue
        ax = fig.add_subplot(nrows,ncolumns,iplot)        
        if coloraxis:
            Z = points[:,coloraxis[cvar]]
            if doLog:
                ax.scatter(points[:,ix],points[:,iy],c=Z,norm=LogNorm(vmin=Z.min(), vmax=Z.max()),
                            vmin=Z.min(),vmax=Z.max(),cmap=cm)
            else:
                ax.scatter(points[:,ix],points[:,iy],c=Z,
                            vmin=Z.min(),vmax=Z.max(),cmap=cm)            
        else:
            ax.scatter(points[:,ix],points[:,iy])       
        if doLines:
            ax.plot(points[:,ix],points[:,iy],'--')        
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        if coloraxis:
            PCM = fig.axes[-1].collections[0]
            if len(coloraxis) == 1 and iplot == 1:                
                cax = plt.axes([1.05, 0.1, 0.05, 0.8])
                cbar = fig.colorbar(PCM,cax=cax)                
            else:
                cbar = fig.colorbar(PCM)
            cbar.set_label(cvar)

        iplot += 1        
        
    if len(fig.axes) > 1:
        fig.tight_layout()
        
    return fig


if __name__ == "__main__":
    
    ap = argparse.ArgumentParser( description=
            "Reads points from a slhaFolder and makes a 2D scatter plot with the results" )
    ap.add_argument('-f', '--slhafolder', help='path to the slha folder')
    ap.add_argument('-m', '--smodelsfolder', help='path to the smodels output folder')
    ap.add_argument('-o', '--outfile', help='Name of output file. If not defined, the plot will not be saved',
                    default = None)


    args = ap.parse_args()
    

    
    #Define the variables to be read here:
    parsExpr = ["blocks['MASS'][5000011]",
                "decays[5000011].totalwidth","1.9e-16/(decays[5000011].totalwidth)"]
    points,slhaFiles = getSLHAPoints(parsExpr,args.slhaFolder)

    parsExpr = ["ExptRes"]
    smodelsPoints,slhaFiles = getSLHAPoints(parsExpr,args.smodelsFolder)

    r8Tracker = []
    r8TOF = []
    r13Tracker = []
    r13TOF = []
    for expList in smodelsPoints:
        for exp in expList:
            if exp['AnalysisSqrts (TeV)'] == 8:
                if 'tracker' in exp['AnalysisID'].lower():
                    r8Tracker.append(exp['theory prediction (fb)']/exp['upper limit (fb)'])
                elif 'tof' in exp['AnalysisID'].lower():
                    r8TOF.append(exp['theory prediction (fb)']/exp['upper limit (fb)'])
            elif exp['AnalysisSqrts (TeV)'] == 8:
                if 'tracker' in exp['AnalysisID'].lower():
                    r13Tracker.append(exp['theory prediction (fb)']/exp['upper limit (fb)'])
                elif 'tof' in exp['AnalysisID'].lower():
                    r13TOF.append(exp['theory prediction (fb)']/exp['upper limit (fb)'])
                    
    rMax = np.array([max(r8Tracker[i],r13Tracker[i],r8TOF[i],r13TOF[i]) for i in range(len(smodelsPoints))])

    
    points = np.concatenate((points,rMax.T),axis=1)
    #Define the axes labels and their index in points (for plotting)
    pars = {r'$m_{E}$ (GeV)' : 0 , r'$c \tau$ (m)' : 2}
    coloraxis = {'r' : -1}
    subset = points[points[:,-1]>0.]
    
    #Define global plot settings:
    params = {'xtick.labelsize' : 15,
            'ytick.labelsize' : 15, 
            'axes.labelsize' : 20, 
            'figure.figsize' : (15,10)}
    mpl.rcParams.update(params)    
    
    fig = plotScan(subset,pars,coloraxis,doLog=True,doLines=False)    
    if args.outfile:
        plt.savefig(args.outfile,bbox_inches='tight')
    plt.show()
    
    
    
