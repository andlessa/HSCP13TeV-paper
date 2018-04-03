import time,os,sys
import ROOT  #Keep it
from ROOT import TFile,TTree,gDirectory,TObject,gROOT,std
import copy

#Writes a dictionary to the resfile. If file does not exist, create a new one
#Uses the dictionary structure. If it is a nested dictionary, every upper level key is a branch and lower level key is a leaf.
#If it is a simple dictionary, every key is a branch
#If new=True, replace existing file, otherwise just update it
#If resfile has root in the name and pyroot is installed, write/update a root file
def ToFile(inputdic,rootfile,treename='tree',new=True,verbose=False):    
  
    indic = {}
#First replace all key names by a root complaint version:
    for key in inputdic.keys():
        indic[rootname(key)] = inputdic[key]
        if type(inputdic[key]) == type({}):
            indic[rootname(key)] = {}
            for key2 in inputdic[key].keys():
                indic[rootname(key)].update({rootname(key2) : inputdic[key][key2]})

#Promote all string variables inside a branch to its own branch:
    for key,val in indic.items():
        if isinstance(val,dict):
            for key2,val2 in val.items():
                if type(val2) == type('str'):
                    indic[key2] = indic[key][key2]
                    indic[key].pop(key2)

    if new and os.path.isfile(rootfile):
        os.remove(rootfile)
  
    rfile = TFile(rootfile, "update")

    if not treename in rfile.GetListOfKeys():
        tree = TTree(treename,"")
    else:
        tree = gDirectory.Get(treename)
        

#Get Branch names:  
    Bnames = indic.keys()    
    ListOfBranches = []
#Create Branches
    for bname in Bnames:     
        invars = indic[bname]
        branch = MyBranch()
        if not branch.Create(bname,invars):
            return False
        ListOfBranches.append(branch)
        if not tree.FindBranch(bname):
            if branch.leaf:
                tree.Branch(branch.name, branch.vars, branch.leaf)
            else:
                tree.Branch(branch.name, branch.vars)
        else:
            if branch.leaf:
                tree.GetBranch(bname).SetAddress(branch.vars)
            else:
                tree.GetBranch(bname).SetObject(branch.vars)
    
    if not indic.values():
        return False

    val = indic.values()[0]
    if type(val) == type({}):
        val = val.values()[0]
    if type(val) == type([]):    
        nevts = len(val)
    else:
        nevts = 1   
    nprint = 0
#Fill branches/leaves           
    for iev in range(nevts):

        #Select event
        eventVals = {}
        for key,vals in indic.items():
            eventVals[key] = type(vals)()
            if isinstance(vals,dict):
                for vkey in vals:
                    eventVals[key][vkey] = vals[vkey][iev]
            else:
                eventVals[key] = vals[iev]
    
        for branch in ListOfBranches:
            vals = eventVals[branch.name]

            if (10*iev/nevts) > nprint:
                nprint = 10*iev/nevts
                if verbose:
                    print str(10*nprint)+"% events processed (out of",nevts,"events) at "+time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())


            branch.Fill(vals)
       
        tree.Fill()
    
    rfile.Write("", TObject.kOverwrite)
    rfile.Close()
    return True



#Return C-type char for the type of variable. If the variable is not an integer or double, return char
def gettype(var):

    if type(var) == type(1): ktype = 'I'
    elif type(var) == type(1.): ktype = 'D'
    elif type(var) == type('str'): ktype = 'S'
    else: ktype = 'C'
    
    return ktype

#Convert string to ROOT complaint name    
def rootname(key):

    name = key.replace(" ","_")
    name = name.replace("~","S")
    name = name.replace("+","p")
    name = name.replace("-","m")
    name = name.replace(")","")
    name = name.replace("(","")
    
    return name 
    
def getroottype(var):

    if type(var) == type(1): ktype = 'Int_t'
    elif type(var) == type(1.): ktype = 'Double_t'
    elif type(var) == type('st'): ktype = 'Char_t'
    else: ktype = None
    
    return ktype


class MyBranch:
    def __init__(self):
        self.name = None
        self.classname = None
        self.leaf = None
        self.vars = None
        
    def Create(self,name,invars,verbose=True):
        
#Get list of variables and names:
        vvar = []
        if type(invars) != type({}):
            if type(invars) == type([]):            
                vvar.append([name,invars[0]])
            else:
                vvar.append([name,invars])
        else:
            for key in invars.keys():
                if type(invars[key]) == type([]):
                    vvar.append([key,invars[key][0]])
                else:
                    vvar.append([key,invars[key]])


        string = False                 
#Check for strings:
        for var in vvar:
            if type(var[1]) == type("st"):
                if len(vvar) > 1:
                    if verbose:
                        print "Create: Branch %s can not contain more than one string or mix strings and floats" %name
                    return False
                string = True                    
                
#Set global properties:
        self.name = name
        if string:
            self.classname = "std.string"
            self.leaf = None
        else:
            self.classname = name + "_t"
            self.leaf = ""
            for var in vvar:
                vtype = gettype(var[1])
                self.leaf += var[0] + "/" + vtype + ":"
            self.leaf = self.leaf[:-1]
#Now create branch specific class to hold variables:
            headline = "struct " + self.classname + " { "
            processline = ""
            for var in vvar:
                vtype = getroottype(var[1])
                processline += vtype + "        " + var[0] + "; "    
            process = headline + processline + "};"
        
        #Check if class has already been defined:
        try:
            self.vars = eval('ROOT.%s()' %self.classname)
        #If not, make ROOT generate the class
        except:
            if gROOT.ProcessLine(process) != 0:
                print 'Error processing source:\n %s' %process
                sys.exit()
            self.vars = eval('ROOT.%s()' %self.classname)

        return True
    
    
        
    def Fill(self,vals,verbose=False):
    

        if type(vals) == type('str') and not self.leaf:
            self.vars.replace(0, std.string.npos, vals)
        elif type(vals) != type({}):
            if hasattr(self.vars,self.name):
                setattr(self.vars,self.name,vals)
            elif verbose:
                print "Fill: root file does not have instance"
        else:
            for key in vals.keys():
                if hasattr(self.vars,key):
                        setattr(self.vars,key,vals[key])
                elif verbose:
                    print "Fill: root file does not have instance ",key
