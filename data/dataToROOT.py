#!/usr/bin/env python



""".. module:: dataToROOT.
        :synopsis: Converts a data in python dictionary format to a ROOT file

.. moduleauthor:: Andre Lessa
"""

import argparse
import time,copy,os
import imp

remove_keys = ['0','sr','analysis','db','ds', 'obs', 'Mass (GeV)', 
               'expected upper limit (fb)', 'chi2', 'likelihood', 'dataType']


def getnulldataFrom(indata):
    
    
    if isinstance(indata,bool):
        return False
    elif indata is None:
        return None
    elif isinstance(indata,str):
        return 'empty'
    elif isinstance(indata,int):
        return 0
    elif isinstance(indata,float):
        return -1.
    elif isinstance(indata,list):
        if not indata:
            return []
        return [getnulldataFrom(indata[0])]
    elif isinstance(indata,dict):
        return dict([[key,getnulldataFrom(val)] for key,val in indata.items()])
    
    
def getUncoveredXsecs(indata):
    
    coverage = {'Asymmetric Branches' : 0., 'Outside Grid' : 0., 
                'Missed Topologies' : 0., 'Long Cascades' : 0.}
    
    for key in coverage:
        if not key in indata:
            continue
        for entry in indata[key]:
            coverage[key] += entry['weight (fb)']
            
    return coverage


def main(dataFolders,rootFile,dictName,fileExtension,treename):
    
    import Aux
    

    #Get list of files
    datafiles = []
    for dataFolder in dataFolders:
        for dirName, _, fileList in os.walk(dataFolder):
            for f in fileList:
                if f[-len(fileExtension):] == fileExtension:                
                    fdata = imp.load_source(dictName,os.path.join(dirName,f))
                    data = getattr(fdata,dictName)
                    #Skip files with long-lived particles or errors
                    if data['OutputStatus']['file status'] < 0:
                        continue
                    datafiles.append(os.path.join(dirName,f))
      
    if not datafiles:
        print 'No files with extension %s found' %fileExtension
        print 'Check if the data has been converted to suitable output.'
        return

    nfiles = len(datafiles)
    entries = 0
    iproc = 0
    nprint = 0
    alldata = None
    nulldataALL = {}
    for datafile in sorted(datafiles):
        try:
            f = imp.load_source(dictName,datafile)
            data = getattr(f,dictName)
        except Exception as e:
            print 'Error reading %s \n Error msg: %s' %(datafile,str(e))
            return False
        
        if not isinstance(data,dict):
            print 'Data in %s is not a dictionary' %datafile
            return False
        
        nulldataALL.update(getnulldataFrom(data))

    for datafile in sorted(datafiles):
        
        f = imp.load_source(dictName,datafile)
        data = getattr(f,dictName)

#     #Collect data to save (make sure string values are at the top level)
        if not 'ExptRes' in data:
            data['ExptRes'] = copy.deepcopy(nulldataALL['ExptRes'])



        expList8 = [exp for exp in data['ExptRes'] if exp['AnalysisSqrts (TeV)'] in [8.,0.,-1.]]
        expList13 = [exp for exp in data['ExptRes'] if exp['AnalysisSqrts (TeV)'] in [13.]]
        
        
        bestExpUL8 = sorted([exp for exp in expList8 if exp['dataType'] == 'upperLimit'], 
                           key = lambda exp: exp['theory prediction (fb)']/exp['upper limit (fb)'], reverse = True)
        bestExpEM8 = sorted([exp for exp in expList8 if exp['dataType'] == 'efficiencyMap'], 
                           key = lambda exp: exp['theory prediction (fb)']/exp['upper limit (fb)'], reverse = True)

        bestExpUL13 = sorted([exp for exp in expList13 if exp['dataType'] == 'upperLimit'], 
                           key = lambda exp: exp['theory prediction (fb)']/exp['upper limit (fb)'], reverse = True)
        bestExpEM13 = sorted([exp for exp in expList13 if exp['dataType'] == 'efficiencyMap'], 
                           key = lambda exp: exp['theory prediction (fb)']/exp['upper limit (fb)'], reverse = True)


        exps8 = {'UL' : bestExpUL8, 'EM' : bestExpEM8}
        exps13 = {'UL' : bestExpUL13, 'EM' : bestExpEM13}
        
        for exps in [exps8,exps13]:
            for expType,exp in exps.items():            
                if not exp:
                    exp = copy.deepcopy(nulldataALL['ExptRes'])[0]    
                else:
                    exp = exp[0] #Select the best result        
                if not 'robs' in exp:
                    if exp['theory prediction (fb)'] == exp['upper limit (fb)'] == -1.:
                        exp['robs'] = 0.
                    else:
                        exp['robs'] = exp['theory prediction (fb)']/exp['upper limit (fb)']            
                exp['lumi'] = exp.pop('lumi (fb-1)')
                if isinstance(exp['TxNames'],list):
                    if len(exp['TxNames']) > 1:
                        exp['TxNames'] = exp['TxNames'][0]+'+'
                    else:
                        exp['TxNames'] = exp['TxNames'][0]
                elif not isinstance(exp['TxNames'],str):
                    exp['TxNames'] = None
                for key in exp.keys():
                    if key in remove_keys:
                        exp.pop(key)
#                 exps[expType] = expextension
    
        filename = os.path.basename(data['OutputStatus']['input file'])
        decompStatus = float(data['OutputStatus']['decomposition status'])
        savedata = {'filename' : filename, 'decompStatus' : decompStatus}
        savedata.update({'coverage' : getUncoveredXsecs(data)})


        best = {'bestResult8' : {}, 'bestResult13' : {}}
        for bestDict in best:
            if bestDict == 'bestResult8':
                exps, sqrts = exps8, '_8'
            elif bestDict == 'bestResult13':
                exps, sqrts = exps13, '_13'
            for expType,exp in exps.items():
                for key,val in exp.items():
                    if isinstance(val,bool) or val is None:  #Convert boolean to string
                        val = str(val)
                    if not isinstance(val,(float,int)):
                        savedata[key+'_'+expType+sqrts] = str(exp.pop(key))
                    else:
                        exp[key] = float(val) #Make sure there are no ints
                        best[bestDict][key+'_'+expType+sqrts] = exp[key]            

        savedata.update(best)
#     #If first call, generate empty data dictionary  (nulldata) 
        if not alldata:
            nulldata = {}
            for key in savedata:
                if type(savedata[key]) == type({}):
                    nulldata[key] = {}
                    for key2 in savedata[key]:
                        nulldata[key][key2] = []
                else: nulldata[key] = []
            alldata = copy.deepcopy(nulldata)
           
        for key in alldata:
            if type(savedata[key]) == type({}):
                for key2 in alldata[key]:  
                    alldata[key][key2].append(savedata[key][key2])
            else:
                alldata[key].append(savedata[key])
                

        iproc += 1
        entries += 1
         
        #Save data to root file    
        if entries >= 1000:
            Aux.ToFile(alldata,rootFile,new=False,treename=treename)
            alldata = copy.deepcopy(nulldata)
            entries = 0
#         
        #Print progress
        if (10*iproc/nfiles) > nprint:
            nprint = 10*iproc/nfiles
            print str(10*nprint)+"% events processed at "+time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
#     
#     
#         

    print nfiles
    if entries > 0:
        Aux.ToFile(alldata,rootFile,new=False,treename=treename)  
    return


if __name__ == "__main__":
    
    
    """ Get the name of input folder to be converted """
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--dataFolder', nargs='+', action='append',
            help='name of data folder(s) path (required argument). ', required=True,
             type = str, default=[])
    ap.add_argument('-o', '--output', 
            help='name of ROOT output file (default = data folder.root', type = str, default = None)
    ap.add_argument('-e', '--extension', 
            help='File name extension (e.g. .slha, .py, ...)', type = str, default = '.py')
    ap.add_argument('-d', '--dictName', 
            help='Name of dictionary in the data file', type = str, default = 'smodelsOutput')
    ap.add_argument('-T', '--treename', 
            help='Label of main Tree in root file', type = str, default = 'tree')
    ap.add_argument('-U', '--update', 
            help='If set will update the root file. Otherwise it will be overwritten', action='store_true')
    

    args = ap.parse_args()
    
    args.dataFolder = args.dataFolder[0]
    for i,dF in enumerate(args.dataFolder):    
        args.dataFolder[i] = os.path.abspath(dF)

    if not args.extension[0] == '.':
        args.extension = '.'+args.extension
    if not args.output:
        args.output = os.path.basename(args.dataFolder)+'.root'
    args.output = os.path.abspath(args.output)
    
    if not args.update and os.path.isfile(args.output):
        os.remove(args.output)
    

    main(args.dataFolder,args.output,args.dictName,
        args.extension,args.treename)
    
    
    