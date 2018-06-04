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
    
    nplots = (len(axes)*(len(axes)-1))/2
    nrows = int(np.floor(nplots**0.5).astype(int))
    ncolumns = int(np.ceil(1.*nplots/nrows).astype(int))
#     fig = plt.figure(figsize=(4.*ncolumns,3.*nrows))
    fig = plt.figure()
    cm = plt.cm.get_cmap('RdYlBu')
    iplot = 1
    if coloraxis:
        Z = points[:,coloraxis.values()[0]]
    for var1,var2 in itertools.product(axes.keys(),axes.keys()):
        ix = axes[var1]
        iy = axes[var2]
        if ix >= iy:
            continue
        ax = fig.add_subplot(nrows,ncolumns,iplot)
        if coloraxis:
            if doLog:
                ax.scatter(points[:,ix],points[:,iy],c=Z,norm=LogNorm(vmin=Z.min(), vmax=Z.max()),
                            s=50,vmin=Z.min(),vmax=Z.max(),cmap=cm)
            else:
                ax.scatter(points[:,ix],points[:,iy],c=Z,
                            s=50,vmin=Z.min(),vmax=Z.max(),cmap=cm)            
        else:
            ax.scatter(points[:,ix],points[:,iy],s=50)       
        if doLines:
            ax.plot(points[:,ix],points[:,iy],'--')        
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        iplot += 1

    fig.tight_layout()
    if coloraxis:
        PCM = fig.axes[0].collections[0]
        cax = plt.axes([1.05, 0.1, 0.05, 0.8])
        cbar = fig.colorbar(PCM,cax=cax)        
        cbar.set_label(coloraxis.keys()[0])
        
    return fig


if __name__ == "__main__":
    
    import sys
    sys.path.append('../')
    from scanHelpers import getSLHAPoints
    import argparse    
    ap = argparse.ArgumentParser( description=
            "Reads points from a slhaFolder and makes a 2D scatter plot with the results" )
    ap.add_argument('-f', '--slhafolder', help='path to the slhafolder')
    ap.add_argument('-o', '--outfile', help='Name of output file. If not defined, the plot will not be saved',
                    default = None)


    args = ap.parse_args()
    

    
    #Define the variables to be read here:
    parsExpr = ["blocks['EXTPAR'][23]","blocks['EXTPAR'][1]",
                "blocks['EXTPAR'][2]","abs(blocks['MASS'][1000024]) - abs(blocks['MASS'][1000022])",
                "abs(blocks['MASS'][1000024])",
                "decays[1000024].totalwidth"]
    slhaFolder = args.slhafolder
    points,slhaFiles = getSLHAPoints(parsExpr,slhaFolder,100)
    
    #Define the axes labels and their index in points (for plotting)
    pars = {r'$\mu$ (GeV)' : 0 , r'$M_2$ (GeV)' : 2, r'$\Delta M$ (GeV)' : 3, r'$m_{\tilde{\chi}^\pm_1}$ (GeV)' : 4}
    coloraxis = {'Width' : -1}
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
    
    
    
