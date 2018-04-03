#!/usr/bin/python

import argparse
import os,copy,time,imp
import Aux
from multiprocessing import Pool

stringFields = ['sr','analysis','AnalysisID','DataSetID','filename']

def createRootFor(analysisID,anaLabel,datatype,datafiles,dictName,rootfile):

    nulldata = {'DataSetID': [], 'theory prediction (fb)': [], 
                'upper limit (fb)': [], 'dataType' : [], 'filename': [] , 'robs' : []}
    nfiles = len(datafiles)

    entries = 0
    iproc = 0
    nprint = 0
    if os.path.isfile(rootfile):
        os.remove(rootfile)
    alldata = copy.deepcopy(nulldata)
    for datafile in sorted(datafiles):
        dataDict = {'DataSetID' : 'None', 'theory prediction (fb)' : 0. , 'dataType' : 'None',
                    'upper limit (fb)' : 0.,'filename' : 'none', 'robs' : 0.}
        try:
            f = imp.load_source(dictName,datafile)
            data = getattr(f,dictName)
        except Exception as e:
            print 'Error reading %s \n Error msg: %s' %(datafile,str(e))
            return False

        dataDict['filename'] = os.path.basename(data['OutputStatus']['input file'])
        goodExp = None
        if 'ExptRes' in data:
            for exp in data['ExptRes']:
                if exp['AnalysisID'] != analysisID or exp['dataType'] != datatype:
                    continue
                if not 'robs' in exp:
                    exp['robs'] = exp['theory prediction (fb)']/exp['upper limit (fb)']
                if not goodExp:
                    goodExp = exp
                else:
                    if exp['robs'] > goodExp['robs']:
                        goodExp = copy.deepcopy(exp)
        
        if goodExp:
            for key,val in goodExp.items():
                if key in dataDict:
                    dataDict[key] = val

        
        for key,val in dataDict.items():
            if key in stringFields:
                val = str(val)
            alldata[key].append(val)
            
        iproc += 1
        entries += 1
        
        if entries >= 1000:
            Aux.ToFile(alldata,rootfile,treename=anaLabel,new=False)
            alldata = copy.deepcopy(nulldata)
            entries = 0
    
        if (10*iproc/nfiles) > nprint:
            nprint = 10*iproc/nfiles
            print str(10*nprint)+"% events processed at "+time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
        
    if entries > 0:
        Aux.ToFile(alldata,rootfile,treename=anaLabel,new=False)        



def main(dataFolder,outFolder,dictName,fileExtension,ncores,update):
    
    
    #Get list of files
    datafiles = []
    for dirName, subdirList, fileList in os.walk(dataFolder):
        for f in fileList:
            if f[-len(fileExtension):] == fileExtension:
                datafiles.append(os.path.join(dirName,f))
    
    #Get all analyses name:    
    allanalyses = []
    
    for datafile in datafiles:
        try:
            f = imp.load_source(dictName,datafile)
            data = getattr(f,dictName)
        except Exception as e:
            print 'Error reading %s \n Error msg: %s' %(datafile,str(e))
            return False
        
        if not isinstance(data,dict):
            print 'Data in %s is not a dictionary' %datafile
            return False
        
        if not 'ExptRes' in data:
            continue
        analysis_list = data['ExptRes']
        for ana in analysis_list:
            if ana['AnalysisSqrts (TeV)'] != 8.: continue
            anaName = ana['AnalysisID']
            if ana['dataType'] == 'efficiencyMap':
                anaName +='-eff'
            if not [ana['AnalysisID'],anaName,ana['dataType']] in allanalyses:
                allanalyses.append([ana['AnalysisID'],anaName,ana['dataType']])
    
     
    pool = Pool(processes=ncores)
    #Submit jobs
    jobs = []
    for analysisID,anaLabel,datatype in allanalyses:
        anaRootFile = os.path.join(outFolder,anaLabel+'.root')
        if not update and os.path.isfile(anaRootFile):
            os.remove(anaRootFile)
        jobs.append(pool.apply_async(createRootFor, 
                                     (analysisID,anaLabel,datatype,datafiles,dictName,anaRootFile)))
    
    for i,job in enumerate(jobs):
        try:
            r = job.get()
            print 'Job %i concluded with: %s \n' %(i,r)
        except Exception as e:
            print 'e=',e
            import sys
            sys.exit()
    


if __name__ == "__main__":
    
    
    """ Get the name of input folder to be converted """
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--dataFolder', 
            help='name of data directory path (required argument). ', required=True, type = str)
    ap.add_argument('-o', '--output', 
            help='name of output folder (default = data folder', type = str, default = None)
    ap.add_argument('-e', '--extension', 
            help='File name extension (e.g. .slha, .py, ...)', type = str, default = '.py')
    ap.add_argument('-d', '--dictName', 
            help='Name of dictionary in the data file', type = str, default = 'smodelsOutput')
    ap.add_argument('-c', '--cores', 
            help='Number of cores to run in parallel', type = int, default = 1)
    ap.add_argument('-U', '--update', 
            help='If set will update the root file. Otherwise it will be overwritten', action='store_true')


    args = ap.parse_args()
    
    args.dataFolder = os.path.abspath(args.dataFolder)
    if not args.extension[0] == '.':
        args.extension = '.'+args.extension
    if not args.output:
        args.output = args.dataFolder
    args.output = os.path.abspath(args.output)

    
    
    main(args.dataFolder,args.output,args.dictName,args.extension,args.cores,args.update)
    
    
