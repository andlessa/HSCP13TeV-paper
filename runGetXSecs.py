#!/usr/bin/env python

#Uses an input SLHA file to compute cross-sections using MadGraph and the UFO model files
#The calculation goes through the following steps
# 1) Run MadGraph using the options set in the input file 
# (the proc_card.dat, parameter_card.dat and run_card.dat...).
# Madgraph is used to compute the widths and cross-sections
# 2) Run slhaCreator to extract the information of the MadGraph output
# and generate a SLHA file containing the cross-sections

#First tell the system where to find the modules:
import sys,os,glob
from configParserWrapper import ConfigParserExt
import logging,shutil
import subprocess
import tempfile
import time,datetime
import itertools
import multiprocessing
import gzip

FORMAT = '%(levelname)s in %(module)s.%(funcName)s() in %(lineno)s: %(message)s at %(asctime)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

    

def Run_MG5(parser):
    """
    Runs MadGraph5 using the parameters given in parser
   
    :param parser: ConfigParser object with all the parameters needed
    """
    
    ncpu = max(1,parser.getint("MadGraphPars","ncores"))
    pars = parser.toDict(raw=False)["MadGraphPars"]
 
    #Expand relative paths:    
    pars['mg5out'] = os.path.abspath(os.path.expanduser(pars['mg5out']))
    pars['mg5path'] = os.path.abspath(os.path.expanduser(pars['MG5path']))
    if not os.path.isdir(pars['MG5path']):
        logger.error("MadGraph folder not found in %s" %pars['MG5path'])
        return False
    
    #Replace MG5 models folder if it already exists:
    if pars['modelFolder'] and pars['modelFolder'] != 'None':
        pars['modelFolder'] = os.path.abspath(os.path.expanduser(pars['modelFolder']))
        mg5model = os.path.join(pars['MG5path'],'models')
        mg5model = os.path.join(mg5model,os.path.basename(pars['modelFolder']))
        if os.path.isdir(mg5model):
            logger.info("Model folder %s already exists" %mg5model)
        else:            
            shutil.copytree(pars['modelFolder'],mg5model)
 
    processDir = pars['mg5out']    
    if os.path.isdir(processDir):
        logger.info("Process folder %s already exists. It will be replaced" %os.path.basename(processDir))
        shutil.rmtree(processDir)
    os.makedirs(processDir)
         
    #Create temp file:
    processCard = tempfile.mkstemp(suffix='.dat', prefix='processCard_', 
                                   dir=pars['MG5path'])
     
    #Get process card:      
    if not os.path.isfile(pars['proccard']):
        logger.error("Process card %s not found" %pars['proccard'])
        return False
    else:
        pFile = open(pars['proccard'],'r')
        for l in pFile.readlines():
            if l.strip()[:6] == 'output':
                continue
            if ('import model' in l) and not ('import model sm' in l):
                l = 'import model %s\n' %pars['model']
            os.write(processCard[0],l)
             
        l = 'output %s\n' %processDir
        os.write(processCard[0],l)
        os.write(processCard[0],'y\n')
        os.write(processCard[0],'quit\n')
        pFile.close()
        os.close(processCard[0])
        processCard = processCard[1]
 
    #Checks        
    if not os.path.isfile(pars['paramcard']):
        logger.error("Parameter card %s not found" %pars['paramcard'])
        return False
    if not os.path.isfile(pars['runcard']):
        logger.error("Run card %s not found" %pars['runcard'])
        return False
    if not os.path.isdir(pars['MG5path']):
        logger.error("MadGraph folder %s not found" %pars['MG5path'])
        return False
    elif not os.path.isfile(os.path.join(pars['MG5path'],'bin/mg5_aMC')):
        logger.error("MadGraph binary not found in %s/bin" %pars['mg5path'])
        return False
         
    #Generate process
    logger.info('Generating process using %s' %os.path.basename(processCard))
    run = subprocess.Popen('./bin/mg5_aMC -f %s' %processCard,shell=True,
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                cwd=pars['MG5path'])
         
    output,errorMsg = run.communicate()
    logger.debug('MG5 process error:\n %s \n' %errorMsg)
    logger.debug('MG5 process output:\n %s \n' %output)
    logger.info("Finished process generation")
    shutil.move(processCard,processDir)
      
    #First copy card files:
    shutil.copyfile(pars['runcard'],os.path.join(processDir,'Cards/run_card.dat'))
    shutil.copyfile(pars['paramcard'],os.path.join(processDir,'Cards/param_card.dat'))
    #Generate commands file:       
    commandsFile = tempfile.mkstemp(suffix='.txt', prefix='MG5_commands_', dir=processDir)
    comms = parser.toDict(raw=False)["MadGraphOptions"]
    for key,val in comms.items():
        os.write(commandsFile[0],'%s=%s\n' %(key,val))
    os.write(commandsFile[0],'done\n')
    comms = parser.toDict(raw=False)["MadGraphSet"]
    for key,val in comms.items():
        os.write(commandsFile[0],'set %s %s\n' %(key,val))        
    os.write(commandsFile[0],'done\n')
    os.close(commandsFile[0])
    commandsFile = commandsFile[1] 
     
    
    logger.info("Generating MG5 events with command file %s" %commandsFile)
    logger.info("Generating MG5 events")
    run = subprocess.Popen('./bin/generate_events --multicore --nb_core=%s < %s' %(ncpu,commandsFile),
                           shell=True,stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,cwd=processDir)
      
    output,errorMsg= run.communicate()
    logger.debug('MG5 event error:\n %s \n' %errorMsg)
    logger.debug('MG5 event output:\n %s \n' %output)
      
    logger.info("Finished event generation")
    
    return True
   

def CreateSLHAFileFrom(inputFile,parser):
    """
    Uses the corresponding banner generated by MadGraph
    to generate an SLHA file corresponding to the parton LHE
    file, including the XSECTION block.
    
    :param inputFile: path to a LHE file generated by MG5 or a template SLHA file. If an slha file is given,
                      the parameters defined in parser[slhaCreator-replace] will be used to replace the values
                      in the template SLHA file.
    :param parser: ConfigParser object with all the parameters needed    
    
    :return: True if successful. Otherwise False.
    """
    
    pars = parser.toDict(raw=False)["slhaCreator"]
    pdgDict = parser.toDict(raw=True)["pdgDict"]
    
    slhaFile = pars['slhaout']
    #Create output dirs, if do not exist:
    try:
        os.makedirs(os.path.dirname(pars['slhaout']))
    except:
        pass    
    
    if not os.path.isfile(inputFile):
        logger.error("File %s not found" %inputFile)
        return False
    
    if inputFile[-3:] == '.gz':
        f = gzip.open(inputFile, 'r')
    else: 
        f = open(inputFile,'r')
    fData = f.read()
    f.close()
    #Check if input file is MG5 banner or SLHA file
    if not '<MGGenerationInfo>' in fData:
        logger.error("Input file %s does not contain required data " %inputFile)
        return False
       
    #Collect necessary info:
    bannerData = fData
    slhaData = bannerData[bannerData.find('<slha>'):bannerData.find('</slha>')]
    slhaData = slhaData.replace('<slha>','')
    slhaData = slhaData.replace('</slha>','')    
    xsecData = (bannerData[bannerData.find('<MGGenerationInfo>'):bannerData.find('</MGGenerationInfo>')]).split('\n')
    processXsecData = (bannerData[bannerData.find('<init>'):bannerData.find('</init>')]).split('\n')
    processData = (bannerData[bannerData.find('<MG5ProcCard>'):bannerData.find('</MG5ProcCard>')]).split('\n')
    
    #Get generated processes:
    processes = []
    for l in processData:
        if not l or l[0] == '#':
            continue
        l = l.strip()
        if l[:8] == 'generate':
            processes = []
            l = l[l.find('generate')+8:]
        elif l[:11] == 'add process':
            l = l[l.find('add process')+11:]
        else:
            continue
        l = l.strip()
        inptc,outptc = l.split('>')
        inptc = inptc.strip().split()
        outptc = outptc.split(',')[0]
        outptc = outptc.strip().split()
        #Convert madgraph particle names to pdgs
        allptc = [pdgDict[ptc] if ptc in pdgDict else ptc for ptc in inptc+outptc]
        processes.append(allptc)

    #Get total cross-section,number of events
    xsecTotal = [l.split(':')[1].strip() for l in xsecData if 'Integrated weight (pb)' in l][0]
    xsecTotal = eval(xsecTotal)
    nevents = [l.split(':')[1].strip() for l in xsecData if 'Number of Events' in l][0]
    nevents = int(eval(nevents))
    if xsecTotal <= 0.:
        logger.error("Total cross-section is zero?")
        return False
    
    #Get sqrts and cross-section for each process:
    for l in processXsecData:
        if not l or l[0] == '#' or l[0] == '<':
            continue
        vals = [eval(x) for x in l.split()]
        if len(vals) == 4:
            processes[vals[-1]-1].append(vals[0])
        else:
            sqrts = vals[2]+vals[3]


    #Check:
    if abs(xsecTotal - sum([x[-1] for x in processes]))/xsecTotal > 0.001:
        logger.error("Error obtaining process cross-sections")
        return False 
    
    #Write SLHA file:
    slhaF = open(slhaFile,'w')
    slhaF.write(slhaData)
    for process in processes:
        if len(process) != 5:
            logger.error("Found process which is not 2 -> 2.")
            return False
        comment = "# Nevts: %i xsec unit: pb" %nevents
        slhaF.write(("\n\nXSECTION %1.3e"+" %s"*5+" %s\n") %(sqrts,process[0],process[1],
                                                       len(process)-3,process[2],
                                                       process[3],comment))        
        slhaF.write("  0  0  0  0  0  0  %1.4e slhaFromLHE 1.0\n" %process[-1])    
    slhaF.close()
    
    logger.info("Finished SLHA creation")
    
    return True


def runAll(parserDict):
    """
    Runs Madgraph, Pythia and the SLHA creator for a given set of options.
    :param parserDict: a dictionary with the parser options.
    """
    
    t0 = time.time() 
    
    parser = ConfigParserExt()
    parser.read_dict(parserDict)    
    
    #Run MadGraph    
    if parser.getboolean("options","runMG"):  
        Run_MG5(parser)

    #Create SLHA file
    if parser.getboolean("options","runSlhaCreator"):
        inputFile = parser.getstr("slhaCreator","inputFile")
        if not os.path.isfile(inputFile):
            logger.error("Input file %s for SLHA creator not found" %inputFile)
        else:
            logger.info("Creating SLHA file from %s" %inputFile)
            slhaFile = CreateSLHAFileFrom(inputFile,parser)
            logger.debug("File %s created" %slhaFile)
                
    #Clean output:
    if parser.getboolean("options","cleanOutFolders"):
        logger.info("Cleaning output")
        if os.path.isdir(parser.getstr("MadGraphPars","mg5out")):
            shutil.rmtree(parser.getstr("MadGraphPars","mg5out"))
          
    logger.info("Done in %3.2f min" %((time.time()-t0)/60.))
    now = datetime.datetime.now()
    
    return "Finished run at %s" %(now.strftime("%Y-%m-%d %H:%M"))



if __name__ == "__main__":

    import argparse    
    ap = argparse.ArgumentParser( description=
            "Run MadGraph and Pythia in order to compute efficiencies for a given model." )
    ap.add_argument('-p', '--parfile', default='eff_parameters_default.ini',
            help='path to the parameters file. Parameters not defined in the parfile will be read from eff_parameters_default.ini')
    ap.add_argument('-l', '--loglevel', default='error',
            help='verbose level (debug, info, warning or error). Default is error')


    t0 = time.time()

    args = ap.parse_args()
    
    level = args.loglevel.lower()
    levels = { "debug": logging.DEBUG, "info": logging.INFO,
               "warn": logging.WARNING,
               "warning": logging.WARNING, "error": logging.ERROR }
    if not level in levels:
        logger.error ( "Unknown log level ``%s'' supplied!" % level )
        sys.exit()
    logger.setLevel(level = levels[level])    

    parser = ConfigParserExt( inline_comment_prefixes=( ';', ) )   
    ret = parser.read(args.parfile)
    if ret == []:
        logger.error( "No such file or directory: '%s'" % args.parfile)
        sys.exit()
        
    
    loopVars = []
    varValues = []
    for section in parser.sections():
        for option in parser.options(section):
            val = parser.get(section,option,raw=True)
            try:
                v = eval(val)
            except:
                v = val
            if not isinstance(v,list):
                v = [v]
            loopVars.append(option)
            varValues.append(v)

    ncpus = parser.getint("options","ncpu")
    if ncpus  < 0:
        ncpus =  multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=ncpus)
    children = []
    #Loop over model parameters and submit jobs
    for values in itertools.product(*varValues):
        newParser = ConfigParserExt()
        newParser.read_dict(parser.toDict())
        for i,v in enumerate(values):        
            for section in newParser.sections():
                if loopVars[i] in newParser.options(section):        
                    newParser.set(section,loopVars[i],str(v))
        parserDict = newParser.toDict(raw=False) #Must convert to dictionary for pickling
        p = pool.apply_async(runAll, args=(parserDict,))            
        children.append(p)
        if len(children) == 1:
            time.sleep(15)  #Let first job run for 15s in case it needs to create shared folders
      
    #Wait for jobs to finish:
    output = [p.get() for p in children]
    for out in output:
        print(out)

    print("\n\nDone in %3.2f min" %((time.time()-t0)/60.))
            
