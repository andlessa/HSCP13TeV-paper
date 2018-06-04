#!/usr/bin/env python

""".. module:: scanHelpers.
        :synopsis: Auxiliary routines for performing a MSSM scan using SPheno

.. moduleauthor:: Andre Lessa
"""

import os,pyslha,subprocess,glob
import logging as logger
import tempfile
import numpy as np
from tempfile import mkstemp

sphenoPath = os.path.abspath('./SPheno/bin/SPheno')


def pars2x(parsDict):
    """
    Convert a parameter dictionary into a 1-D array of values.
    
    :param parsDict: parameters dictionary (e.g.  {'EXTPAR' : { 1 : 100., 2: 300., 23: 500}})
    
    :return: 1-D numpy array with values for the parameters
    """
    
    xvalues = np.array([])
    if not isinstance(parsDict,dict):
        return parsDict
    for _, v in sorted(parsDict.items()):
        xvalues = np.append(xvalues,pars2x(v))
    return xvalues

def x2pars(x,parsDict):
    """
    Replace the values in parsDict by the values in x
    
    :param parsDict: parameters dictionary (e.g.  {'EXTPAR' : { 1 : 100., 2: 300., 23: 500}})
    :param x: List with values for the parameters
    
    :return: dictionary with the new values
    """
    
    if not isinstance(parsDict,dict):
        val = x.pop(0)
        return val
    for key, v in sorted(parsDict.items()):
        parsDict[key] = x2pars(x,v)
        
    return parsDict    


def getPoints(parsExpr,slhaFolder,nmax=-1):
    """
    Reads all SLHA files in the slhaFolder and returns list of points
    with the values for the parameters defined in pars.
    
    :param parsExpr: list of string expressions for computing the desired parameters
                      (e.g. ['blocks['EXTPAR'][23],'blocks['EXTPAR'][1]','blocks['EXTPAR'][2]','decays[1000024].totalwidth'])
    :param slhaFolder: Path to the folder containing slha files    
    :param nmax: Option to set the maximum number of points. If nmax > 0, only the first nmax points will be read.    
    
    :return: 2-D array with each point, its corresponding y-value and a 1-D array with the corresponding file names
    
    """
    
    points = []
    slhaFiles = []
    for slhafile in glob.glob(slhaFolder+'/*.slha'):
        if nmax > 0 and len(points) > nmax:
            break
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



def getSpectrum(infile,outfile=None):
    """
    Runs SPheno given the input file infile.
    If outfile is defined, it will write the output to
    this file, otherwise the outputfile will be removed.
    
    :param infile: Path to the input file
    :param outfile: Path to the output file
    
    :return: pyslha Doc object. If the run was not successful, return None.    
    """
    

    #Get output filename:
    if not outfile:
        outF = tempfile.mkstemp(suffix='.slha',dir='./')
        os.close(outF[0])
        outF = outF[1]
    else:
        outF = outfile
    if os.path.isfile(outF):
        os.remove(outF)

    if not os.path.isfile(sphenoPath):
        raise Exception('Spheno not found at %s. Set the correct path.' %sphenoPath)
    
    subprocess.call([sphenoPath,infile, outF])
    
    if not os.path.isfile(outF):
        return None
    try:
        slhadata = pyslha.readSLHAFile(outF)
        if not outfile:
            os.remove(outF)
        return slhadata
    except:
        os.remove(outF)
        return None
    
    
    
def getInputFile(pars,templateFile,outfile=None):
    """
    Given a template input file (for SPheno),
    generate a new file with the values for the variables in pars
    replaced.
    
    :param pars: dictionary with the parameters to be replaced (e.g. {'EXTPAR' : {1 : 100., 2 : 500., 23 : 300.}})
    :param templateFile: path to the templateFile or pyslha Doc object.
    :param outfile: Name of the outputfile. If not defined, will create a tempfile
    
    :return: name of the outputfile. If something went wrong, return False. 
    """
    
    
    if isinstance(templateFile,str):
        if not os.path.isfile(templateFile):
            logger.error('Tempalte file %s not found' %templateFile)
            return False
        try:
            pydata = pyslha.readSLHAFile(templateFile,
                                         ignorenomass=True,ignorenobr=True)
        except:
            logger.error('Error readgin %s' %templateFile)
            return False
    elif isinstance(templateFile,pyslha.Doc):
        pydata = templateFile
    else:
        logger.error('Unknown format for templateFile: %s' %str(type(templateFile)))
        return False
    
    for key in pars:
        if not key in pydata.blocks:
            logger.info("Block %s not found in %s. It will be ignored" %(key,templateFile))
            continue
        for parameterID,parameterValue in pars[key].items():
            pydata.blocks[key][parameterID] = parameterValue
    
    #Get output file name
    if not outfile:
        outfile = mkstemp(suffix='.in',dir='./')
        os.close(outfile[0])
        outfile = outfile[1]
    if os.path.isfile(outfile):
        os.remove(outfile)
    
    #Write SLHA data to output file name
    pyslha.write(outfile,pydata)
    
    return outfile
    



