#!/usr/bin/python


import argparse
import os,time,copy
import pyslha


#Widths to compute (always use positive PDGs)
getWidths = {'gl_W': 1000021, 'C1_W' : 1000024, 'T1_W' : 1000006}
getWidths = {'H0_W' : 35, 'A0_W' : 36, 'Hp_W' : 37}

#BRs to compute (always use positive PDGs, charges are always summed over)
getBRs = {
'gl_N1qq': {1000021 : [[1000022,1,1],[1000022,2,2],[1000022,3,3],[1000022,4,4]]},    
'gl_N2tt': {1000021 : [[1000023,6,6]]},
'gl_N2bb': {1000021 : [[1000023,5,5]]},
'gl_C1tb': {1000021 : [[1000024,6,5]]},
'gl_sbb': {1000021 : [[1000005,5]]},
'gl_stt': {1000021 : [[1000006,6]]},
'gl_N1tt': {1000021 : [[1000022,6,6]]},
'gl_N1bb': {1000021 : [[1000022,5,5]]},
'gl_N1x': {1000021 : [[1000022]]},
'gl_N1g': {1000021 : [[1000022,21]]},
'gl_NIg': {1000021 : [[1000023,21],[1000025,21],[1000035,21]]},
'N2_N1h': {1000023 : [[1000022,25]]},
'N2_N1Z': {1000023 : [[1000022,23]]},
'C1_N1W': {1000024 : [[1000022,24]]},
'C1_N1lnu': {1000024 : [[1000022,11,12],[1000022,13,14],[1000022,15,16]]},
'C1_N1qq': {1000024 : [[1000022,1,2],[1000022,3,4]]},
'SQ_N1x': {1000001 : [[1000022]],2000001 : [[1000022]],1000002 : [[1000022]],2000002 : [[1000022]],1000003 : [[1000022]],2000003 : [[1000022]],1000004 : [[1000022]],2000004 : [[1000022]]},
'SQ_C1x': {1000001 : [[1000024]],2000001 : [[1000024]],1000002 : [[1000024]],2000002 : [[1000024]],1000003 : [[1000024]],2000003 : [[1000024]],1000004 : [[1000024]],2000004 : [[1000024]]},
'SQ_N2x': {1000001 : [[1000023]],2000001 : [[1000023]],1000002 : [[1000023]],2000002 : [[1000023]],1000003 : [[1000023]],2000003 : [[1000023]],1000004 : [[1000023]],2000004 : [[1000023]]},
'SQ_N3x': {1000001 : [[1000025]],2000001 : [[1000025]],1000002 : [[1000025]],2000002 : [[1000025]],1000003 : [[1000025]],2000003 : [[1000025]],1000004 : [[1000025]],2000004 : [[1000025]]},
'SQ_C2x': {1000001 : [[1000037]],2000001 : [[1000037]],1000002 : [[1000037]],2000002 : [[1000037]],1000003 : [[1000037]],2000003 : [[1000037]],1000004 : [[1000037]],2000004 : [[1000037]]},
'T1_N1t': {1000006 : [[1000022,6]]},
'T1_N2t': {1000006 : [[1000023,6]]},
'T1_C1b' : {1000006 : [[1000024,5]]},
'B1_N1b': {1000005 : [[1000022,5]]},
'B1_N2b': {1000005 : [[1000023,5]]},
'B1_C1t' : {1000005 : [[1000024,6]]}
}

getBRs = {
'Hp_H0ff' : {37 : [[35,1,2], [35,11,12], [35,13,14], [35,3,2]]},
'Hp_H0W' : {37 : [[35,24]]}
}    

#Masses to print
printMasses = {
 'So4_mass': 1000035,
 'Mur': 2000002,
 'Mt2': 2000006,
 'Hp_mass': 37,
 'Mt1': 1000006,
 'Msr': 2000003,
 'So1_mass': 1000022,
 'Snmu_mass': 1000014,
 'Msl': 1000003,
 'Mul': 1000002,
 'So2_mass': 1000023,
 'SmR_mass': 2000011,
 'SGl_mass': 1000021,
 'Mcl': 1000004,
 'h_mass': 25,
 'W_mass': 24,
 'H3_mass': 36,
 'Mcr': 2000004,
 'Mb2': 2000005,
 'SmL_mass': 1000011,
 'b_mass': 5,
 'H_mass': 35,
 'Stau1_mass': 1000015,
 'Snm_mass': 1000012,
 'SmuR_mass': 2000013,
 'Mdl': 1000001,
 'Stau2_mass': 2000015,
 'C2p_mass': 1000037,
 'So3_mass': 1000025,
 'Mb1': 1000005,
 'C1p_mass': 1000024,
 'Mdr': 2000001,
 'SmuL_mass': 1000013,
 'Sntau_mass': 1000016}

printMasses = {
'H0_mass' : 35,
'Hp_mass' : 37,
'A0_mass' : 36    
}

#Xsecs to print:
printXSecs = {'C1pN2_fb' : ['8 TeV',(1000023,1000024)],'C1mN2_fb' : ['8 TeV',(-1000024,1000023)],
              'T1T1_fb' : ['8 TeV',(-1000006,1000006)],'B1B1_fb' : ['8 TeV',(-1000005,1000005)],
              'glgl_fb' : ['8 TeV',(1000021,1000021)], 'totalxsec_fb' : ['8 TeV','all']}

printXSecs = {'HpHm_fb' : ['8 TeV',(-37,37)], 'totalxsec13_fb' : ['13 TeV','all'],'totalxsec8_fb' : ['8 TeV','all']}

#K-factors to print
printKfactors = {'k_glgl' : ['8 TeV',(1000021,1000021)], 
                 'k_sdsd' : ['8 TeV',(1000001,1000001)],
                 'k_sdgl' : ['8 TeV',(1000001,1000021)], 'k_max' : ['8 TeV','all']}
printKfactors = {}

def getFilesFrom(select):
    """
    Get the list of filenames in file select.
    """
    
    import ROOT

    f = ROOT.TFile(select,'read')
    objs = f.GetListOfKeys()
    trees = []
    for ob in objs:
        Tob = ob.ReadObj()
        if type(Tob) == type(ROOT.TTree()):
            trees.append(Tob)

    fnames = []
    for tree in trees:
        tree.GetEntry(0)
        if not hasattr(tree,'filename'):
            continue
        for iev in range(tree.GetEntries()):
            tree.GetEntry(iev)
            fname = str(tree.filename)
            if not fname in fnames:
                fnames.append(fname)

    f.Close()

    return fnames   


def main(dataFolders,rootfile,fileExtension,treename,select):


    import Aux

    #Get SLHA files
    slhafiles = []
    if select:
        if os.path.isfile(select):
            useFiles = getFilesFrom(select)
            for f in useFiles:
                slhafile = None
                for dataFolder in dataFolders:                    
                    if not os.path.isfile(os.path.join(dataFolder,f)):
                        continue
                    else:
                        slhafile = os.path.join(dataFolder,f)
                        break
                if slhafile is None:
                    print 'File %s not found' %f
                    return False
                slhafiles.append(slhafile)
        else:
            print 'File %s not found. All data will be used' %select
    else:
        useFiles = None
        for dataFolder in dataFolders:
            for dirName, _, fileList in os.walk(dataFolder):
                for f in fileList:
                    if f[-len(fileExtension):] == fileExtension:
                        slhafiles.append(os.path.join(dirName,f))
        slhafiles = sorted(slhafiles)
    
    #BRs to print
    printBRs = getBRs.keys()

    #Widths to print
    printWidths = getWidths.keys()
    

    nfiles = len(slhafiles)
    entries = 0
    iproc = 0
    nprint = 0
    nulldata = {'filename' :[], 'BRs' : {}, 'Masses' : {}, 'Xsecs' : {}, 'Kfactors' : {}, 'Widths' : {}}
    for label in printBRs:
        nulldata['BRs'][label] = []
    for label in printMasses:
        nulldata['Masses'][label] = []
    for label in printXSecs:
        nulldata['Xsecs'][label] = []
    for label in printKfactors:
        nulldata['Kfactors'][label] = []
    for label in printWidths:
        nulldata['Widths'][label] = []

        
    alldata = copy.deepcopy(nulldata)
    

    for slhafile in slhafiles:
        res = pyslha.readSLHAFile(slhafile)    
    
    #Get list of branching ratios for all particles:
        BRdic = {}
        for pid in res.decays.keys():
            BRdic[pid] = res.decays[abs(pid)].decays

    #Get mass list for all particles
        Massdic = {}
        for pid,mass in res.blocks['MASS'].items():
            if mass != None:
                Massdic[pid] = abs(mass)

        #Get BRs:
        BRdata = {}
        for key in getBRs:
            BRdata[key] = 0.
            for initial_state in getBRs[key]:             
                for final_state in getBRs[key][initial_state]:
                    for decay in BRdic[initial_state]:
                        final_states = set([abs(pdg) for pdg in decay.ids])
                        if set(final_state).issubset(final_states):
                            BRdata[key] += decay.br


        #Get Widths:
        WidthData = {}
        for key,pid in getWidths.items():
            WidthData[key] = res.decays[pid].totalwidth
        
        #Get k-factors:
        Kfactors = {}
        for key in printKfactors:
            Kfactors[key] = 1.
            pidPair = printKfactors[key][1]
            if pidPair != 'all':
                pidPair = (2212,2212) + pidPair
                if not pidPair in res.xsections:
                    continue
                else:
                    proc = res.xsections[pidPair]
                    if '8 TeV' in printKfactors[key][0]:
                        xsecs = proc.get_xsecs(sqrts=8000.)
                    elif '13 TeV' in printKfactors[key][0]:
                        xsecs = proc.get_xsecs(sqrts=13000.)
                    if not xsecs:
                        continue
                    Kfactors[key] = max([x.value for x in xsecs])/min([x.value for x in xsecs])
            else:
                kall = 1.
                for proc in res.xsections.values():
                    if '8 TeV' in printKfactors[key][0]:
                        xsecs = proc.get_xsecs(sqrts=8000.)
                    elif '13 TeV' in printKfactors[key][0]:
                        xsecs = proc.get_xsecs(sqrts=13000.)
                    if not xsecs:
                        continue
                    k =  max([x.value for x in xsecs])/min([x.value for x in xsecs])
                    kall = max(kall,k)
                Kfactors[key] = kall
        
        #Get Xsecs:
        Xsec = {}
        for key in printXSecs:
            Xsec[key] = 0.
            pidPair = printXSecs[key][1]
            if pidPair != 'all':
                pidPair = (2212,2212) + pidPair
                if not pidPair in res.xsections:
                    continue
                else:
                    proc = res.xsections[pidPair]
                    if '8 TeV' in printXSecs[key][0]:
                        xsecs = proc.get_xsecs(sqrts=8000.)
                    elif '13 TeV' in printXSecs[key][0]:
                        xsecs = proc.get_xsecs(sqrts=13000.)
                    if not xsecs:
                        continue
                    Xsec[key] = max([x.value for x in xsecs])
            else:
                xsecall = 0.
                for proc in res.xsections.values():
                    if '8 TeV' in printXSecs[key][0]:
                        xsecs = proc.get_xsecs(sqrts=8000.)
                    elif '13 TeV' in printXSecs[key][0]:
                        xsecs = proc.get_xsecs(sqrts=13000.)
                    if not xsecs:
                        continue
                    xsecall +=  max([x.value for x in xsecs])
                Xsec[key] = xsecall
            if '_fb' in key:
                Xsec[key] = Xsec[key]*1000.                     
                
        #Collect data to be printed in ROOT file:    
        data = {'BRs' : {}, 'Masses' : {}, 'Xsecs' : {}, 'Kfactors' : {}, 'Widths' : {}}
        for label in printBRs:
            data['BRs'][label] = BRdata[label]
        for label in printMasses:
            data['Masses'][label] = Massdic[printMasses[label]]
        for label in printXSecs:
            data['Xsecs'][label] = Xsec[label]
        for label in printKfactors:
            data['Kfactors'][label] = Kfactors[label]
        for label in printWidths:
            data['Widths'][label] = WidthData[label]

        for key,block in data.items():
            for key2,val in block.items():        
                alldata[key][key2].append(val)                
        filename = os.path.basename(slhafile)
        alldata['filename'].append(filename)
        
        
        iproc += 1
        entries += 1
             
        if entries >= 5000:
            Aux.ToFile(alldata,rootfile,new=False,treename=treename)
            alldata = copy.deepcopy(nulldata)
            entries = 0
         
        if (10*iproc/nfiles) > nprint:
            nprint = 10*iproc/nfiles
            print str(10*nprint)+"% events processed at "+time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
             
    if entries > 0:
        Aux.ToFile(alldata,rootfile,new=False,treename=treename)        
    

if __name__ == "__main__":
    
    """ Get the name of input folder to be converted """
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--dataFolder', nargs='+', action='append',
            help='list of data folder(s) path (required argument). ', required=True,
             type = str, default=[])
    ap.add_argument('-o', '--output', 
            help='name of output ROOT file (default = data folder_slha', type = str, default = None)
    ap.add_argument('-e', '--extension', 
            help='File name extension (e.g. .slha, .py, ...)', type = str, default = '.slha')
    ap.add_argument('-U', '--update', 
            help='If set will update the root file. Otherwise it will be overwritten', action='store_true')
    ap.add_argument('-T', '--treename', 
            help='Label of main Tree in root file', type = str, default = 'slhadata')
    ap.add_argument('-S', '--select', 
            help='Path to a ROOT file generated by dataToROOT.py. If given, it will be used to select only the files contained in the ROOT file',
            type = str,  default = '')        


    args = ap.parse_args()
    
    args.dataFolder = args.dataFolder[0]
    for i,dF in enumerate(args.dataFolder):    
        args.dataFolder[i] = os.path.abspath(dF)
    if not args.extension[0] == '.':
        args.extension = '.'+args.extension
    if not args.output:
        args.output = args.dataFolder+'_slha.root'
    args.output = os.path.abspath(args.output)
    
    if not args.update and os.path.isfile(args.output):
        os.remove(args.output)

    main(args.dataFolder,args.output,args.extension,args.treename,args.select)
    
    
