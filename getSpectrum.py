#!/usr/bin/env python
from tempfile import mkstemp



""".. module:: getSpectrum.
        :synopsis: Simple code to run SPheno and return the slhadata
                  (pyslha object)

.. moduleauthor:: Andre Lessa
"""

import os,pyslha,subprocess
import logging as logger
import tempfile
import numpy as np

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
        os.remove(outfile)
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
    



