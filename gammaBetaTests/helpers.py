#!/usr/bin/env python

""".. module:: helpers.
        :synopsis: Functions for plotting a scan using matplotlib

.. moduleauthor:: Andre Lessa
"""

import numpy as np
import matplotlib.pyplot as plt
import pyslha,os
import copy        
from scipy.interpolate import interp1d
import unum
unum.Unum.reset()
unum.Unum.VALUE_FORMAT = "%0.2E"
unum.Unum.UNIT_HIDE_EMPTY = True

m = unum.Unum.unit('m')
cm = unum.Unum.unit('cm', 0.01 * m )
mm = unum.Unum.unit('mm', 0.001 * m )
fm = unum.Unum.unit('fm', 1e-15 * m )

fb = unum.Unum.unit('fb')
pb = unum.Unum.unit('pb', 1000 * fb)
mb = unum.Unum.unit('mb', 10**12 * fb )

eV = unum.Unum.unit('eV')
keV = unum.Unum.unit('keV', 10 ** 3 * eV)
MeV = unum.Unum.unit('MeV', 10 ** 6 * eV)
GeV = unum.Unum.unit('GeV', 10 ** 9 * eV)
TeV = unum.Unum.unit('TeV', 10 ** 12 * eV)



def getUpperLimitFrom(ulDataFile,xcol=0,ycol=1,unit=pb,doLog=True):
    """
    Reads the mass vs upper limit datapoints for the ulDataFile and
    creates a function which interpolates linearly the points. If doLog = True
    the linear interpolation will applied in the UL-axis log scale.
    
    Returns a function which gives the UL for a given mass value.
    OBS: The UL values are given in the SAME units as the input file.
         For mass values outside the range in the file, the function returns None.
    
    :param ulDataFile: Path to the UL data file (str). The file must be a text file with columns
                       for the mass and upper limit values.
    :param xcol: Index of the mass column (int)
    :param ycol: Index of the UL column (int)
    :param unit: A Unum object defining the UL unit (Unum) 
    :param doLog: If True, will interpolate linearly for log(UL).
    
    :return: A function which returns the upper limits for a given mass value.
                    
    """
    
    exclusionCurve = np.loadtxt(ulDataFile,usecols=(xcol,ycol))
    if doLog:
        interp = interp1d(exclusionCurve[:,0],np.log10(exclusionCurve[:,1]),
                     kind='linear',bounds_error=False,fill_value=None)
        if interp is None:
            return None
        
        upperLimit = lambda m: np.power(10.0, interp(m))*unit
    else:
        interp = interp1d(exclusionCurve[:,0],exclusionCurve[:,1],
                     kind='linear',bounds_error=False,fill_value=None)
        if interp is None:
            return None
        
        upperLimit = lambda m: interp(m)*unit
    
    return upperLimit


def getData(slhaFiles,massPDG,widthPDG,xsecSqrts,xsecPDGs,upperLimitFunction):
    """
    Reads the SLHA files listed in slhaFiles and returns a dictionary containing
    information about the mass, cross-section, upper limit and r=xsec/UL for each file.
    
    :param slhaFiles: List of SLHA files (list of strings)
    :param massPDG: PDG number to extract the mass from the file (int)
    :param widthPDG: PDG number to extract the total width from the file (int)
    :param xsecSqrts: Value (including units) for the cross-section sqrts (Unum object) 
    :param xsecPDGS: Tuple with the PDGs for the cross-section process (e.g. (22122,22122,11,-11))
    :param upperLimitFunction: Function to be used to compute the UL for the respective mass.
     
    :return: A nested dictionary with the format: 
                {slhafile1 : {'xsec (fb)' : xsec,  'UL (fb)' : ul, 'r' : xsec/ul,  'mass (GeV)' : mass, 'width (GeV)' : width},
                 slhafile2 : {'xsec (fb)' : xsec,  'UL (fb)' : ul, 'r' : xsec/ul,  'mass (GeV)' : mass, 'width (GeV)' : width},...}
    """

    data = {}
    for slhafile in slhaFiles:
        slhaData = pyslha.readSLHAFile(slhafile)
        proc = slhaData.xsections[xsecPDGs]
        mass = slhaData.blocks['MASS'][massPDG]
        if widthPDG in slhaData.decays:
            width = slhaData.decays[widthPDG].totalwidth
        else:
            width = 0.
        xsec = max([x.value for x in proc.get_xsecs(sqrts=xsecSqrts.asNumber(GeV))])
        xsec *= pb
        slhafile = os.path.basename(slhafile)        
        data[slhafile] = {'xsec (fb)' : xsec.asNumber(fb), 'mass (GeV)' : mass, 'width (GeV)' : width}
        ul = upperLimitFunction(mass)
        if not (ul is None):
            data[slhafile].update({'UL (fb)' : ul.asNumber(fb), 'r' : xsec.asNumber(fb)/ul.asNumber(fb)})
        else:
            data[slhafile].update({'UL (fb)' : ul, 'r' : 0.})

        
    return data

def getLLPFractionData(fractionFiles,xcol=0,ycol=1):
    """
    Reads the LLPfraction files listed in fractionFiles and returns a dictionary containing
    information about LLP fractions for each file.
    The names of the fractionFiles are supposed to correspond to the SLHA files (except for .slha <-> .txt).
    Each fraction file must contain a table with the values for L/ctau and LLP_fraction.
    
    :param fractionFiles: List of LLP fraction files (list of strings)
    :param xcol: Index of the L/ctau column (int)
    :param ycol: Index of the LLP_fraction column (int)
     
    :return: A dictionary with the format: 
                {slhafile1 : np.array([[x1,fraction1],[x2,fraction2],...]),...}
    """
    
    
    fractionLLP = {}
    for f in fractionFiles:
        slhafile = os.path.basename(f).replace('.txt','.slha')
        fractionLLP[slhafile] = np.loadtxt(f,usecols=(xcol,ycol))
                
    return fractionLLP

def rescaleData(data,fractionLLP,Ldetector):
    """
    Uses the total cross-section and mass information from data and the LLP fractions
    from fractionLLP to produce a set of points with the cross-section (r-values)
    rescaled by the LLP fractions.
    Since the fractions are given for a specific x = L/ctau value, the relevant
    size of the detector must be defined by Ldetector in order to convert from x to ctau.
    
    
    :param data: A data dictionary generated by getData
    :param fractionLLP: A data dictionary generated by getLLPFractionData
    :param Ldetector: The relevant size of the detector including units (Unum object)
    
    :return: A list of floats in the format:
             [ [mass1,ctau1,r1_rescaled], [mass2,ctau2,r2_rescaled],...]
     
    """
    
    points = []
    for slhafile in data:
        res = data[slhafile]
        fLLP = fractionLLP[slhafile]
        ctau = Ldetector.asNumber(m)/fLLP[:,0]
        if not res['r']:
            continue #skip points without limits or xsecs        
        r = res['r']*fLLP[:,1] 
        mList = [res['mass (GeV)']]*len(ctau)
        points += zip(mList,ctau,r)

    points = np.array(points)
    return points    


def getExclusionCurve(ulDataFile,slhaFiles,fractionFiles,
                      massPDG,widthPDG,xsecPDGs,xsecSqrts,Ldetector,
                      curveFile,borderValue):

    """
    Get an exclusion curve using the upper limits defined in the ulDataFile
    and the total cross-sections from the SLHA files in slhaFiles.
    The cross-sections are rescaled by the effective pre-computer LLP fractions
    stored in fractionFiles.
    
    
    
    :param ulDataFile: Path to the UL data file (str). The file must be a text file with columns
                       for the mass and upper limit values.
    :param slhaFiles: List of SLHA files (list of strings)
    :param fractionFiles: List of LLP fraction files (list of strings)    
    :param massPDG: PDG number to extract the mass from the file (int)
    :param widthPDG: PDG number to extract the total width from the file (int)    
    :param xsecSqrts: Value (including units) for the cross-section sqrts (Unum object) 
    :param xsecPDGS: Tuple with the PDGs for the cross-section process (e.g. (22122,22122,11,-11))
    :param Ldetector: The relevant size of the detector including units (Unum object)
    :param curveFile: Name of the curve file to save the output.
    :param borderValue: r-value to be used to define the exclusion border (float)
    
    :return: Name of the data file generated    
    
    """


    cmsUL = getUpperLimitFrom(ulDataFile)
    data = getData(slhaFiles=slhaFiles,massPDG=massPDG,widthPDG=widthPDG,
                   xsecPDGs=xsecPDGs,xsecSqrts=xsecSqrts,
                  upperLimitFunction=cmsUL)
    fractionLLP = getLLPFractionData(fractionFiles)
    points = rescaleData(data,fractionLLP,Ldetector)
    
    #Compute exclusion curve in the log plane
    excCurve = getContour(points[:,0],np.log10(points[:,1]),points[:,2],levels=[borderValue])[borderValue][0]
    #Convert to ctau:
    excCurve[:,1] = np.power(10.,excCurve[:,1])
    #Removed points without limits:
    cleanCurve = []
    for pt in excCurve:
        if any(np.isnan(pt)):
            continue
        cleanCurve.append(pt)
    cleanCurve = np.array(cleanCurve)
    #Save exclusion curve:
    np.savetxt(curveFile,cleanCurve,delimiter='  ',header = "mass(GeV)        ctau(m)",fmt='%.6e')
    
    return curveFile


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

