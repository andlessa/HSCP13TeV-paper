#!/usr/bin/env python
import os,sys,copy
from ROOT import TTree,TColor,TCanvas,TF1,TGraph,Double,TFile,gDirectory,TNamed,gROOT
from plottingDicts import Var_dic,Exp_dic,EXTPAR_dic,Observables_dic,MINPAR_dic,MassPDG_dic
from array import array
from math import sqrt,log,log10

def infiles(fileList):
    filename = fileList[0]
    friends = fileList[1:]
    
    goodfriends = []
    for friend in friends:
        if os.path.isfile(friend):
            goodfriends.append(friend)
        elif os.path.isdir(friend):
            dirfiles = os.listdir(friend)
            for f in dirfiles:                
                fname = friend+f
                if not os.path.isfile(fname): continue
                if fname[-5:] == '.root' and fname != filename: goodfriends.append(fname)

    return filename,goodfriends

def getTree(gDirectory,friends=[],verbose=False):
        
#Get Trees:
    objs = gDirectory.GetListOfKeys()
    trees = []
    if not objs:
        print 'No objects found'
        sys.exit()
    for ob in objs:
        Tob = ob.ReadObj()
        if type(Tob) == type(TTree()):
            trees.append(Tob)

    if len(trees) <= 0:
        print "No trees found in file"
        sys.exit()
    elif len(trees) > 1:
        pstr = "More than one tree found, specify which one to use ("
        for tree in trees:
            pstr += tree.GetName()+","
        pstr += ")"
        usetree = raw_input(pstr)
        tree = gDirectory.Get(usetree)
    else:
        tree = trees[0]
    
    for ifriend,friend in enumerate(friends):
        ffriend = TFile(friend)
        objs = ffriend.GetListOfKeys()        
        for ob in objs:
            Tob = ob.ReadObj()
            if type(Tob) == type(TTree()):
                print "Adding friend",friend
                tree.AddFriend("friend"+str(ifriend)+" = "+str(Tob.GetName()),friend)
        ffriend.Close()
#Get Branches and Leaves (variables):
    branches = tree.GetListOfBranches()
    leaves = tree.GetListOfLeaves()
    lnames = [leaf.GetName() for leaf in leaves]
    
#Get Input parameters:
    inputpars = {}
    for br in branches:    
        if br.GetName().lower() != "input": continue
        for leaf in br.GetListOfLeaves():
            lname = leaf.GetName()
            inputpars.update({lname : [tree.GetMinimum(lname),tree.GetMaximum(lname)]})
            
    if verbose:            
        print "Nevts = ",tree.GetEntries()
        if inputpars:
            print "Input parameters and range:"
            for key in inputpars.keys():
                print key,inputpars[key]            

    return tree,lnames,inputpars

#Use Var_dic to create latex-compliant names for the leaves.
#If Var_dic does not contain the leaf name, use the own name:
def GetVarNames(allvars):
    varnames = {}
    for vname in allvars:
        if Var_dic.has_key(vname):
            varnames.update({vname : Var_dic[vname]})
        else:
            varnames.update({vname : vname})
        
    return varnames

#Check if variables in AllowedRange.keys() have their values in the allowed range
def GetExcluded(AllowedRange,tree):

    excluded = {}

    for exc in AllowedRange.keys():        
        try:
            if getattr(tree,exc) <= AllowedRange[exc][1] and getattr(tree,exc) >= AllowedRange[exc][0]:
                excluded[exc] = False
            else:
                excluded[exc] = True
        except:
            pass
    
    return excluded    
        
        
def GetValue(tree,x):

    if hasattr(tree,x):
        return getattr(tree,x)
    if x in Exp_dic.keys():
        exp = Exp_dic[x]
        exp = exp.replace("TREENAME","tree")
        return eval(exp)
    else:
        print "[GetValue]: Unknown variable",x
        sys.exit()
    
    
        
def Default(obj,Type):
    
    if Type == "TCanvas":
        obj.SetLeftMargin(0.1097891)
        obj.SetRightMargin(0.02700422)
        obj.SetTopMargin(0.02796053)
        obj.SetBottomMargin(0.14796053)
        obj.SetFillColor(0)
        obj.SetBorderSize(0)
        obj.SetFrameBorderMode(0)
    elif "TGraph" in Type or "TH" in Type:
        obj.GetYaxis().SetTitleFont(132)
        obj.GetYaxis().SetTitleSize(0.065)
        obj.GetYaxis().CenterTitle(True)
        obj.GetYaxis().SetTitleOffset(0.9)
        obj.GetXaxis().SetTitleFont(52)
        obj.GetXaxis().SetTitleSize(0.065)
        obj.GetXaxis().CenterTitle(True)
        obj.GetXaxis().SetTitleOffset(1.0)
        obj.GetYaxis().SetLabelFont(132)
        obj.GetXaxis().SetLabelFont(132)
        obj.GetYaxis().SetLabelSize(0.05)
        obj.GetXaxis().SetLabelSize(0.05)
        if "TGraph2D" in Type or "TH2" in Type:
            obj.GetZaxis().SetTitleFont(132)
            obj.GetZaxis().SetTitleSize(0.06)
            obj.GetZaxis().CenterTitle(True)
            obj.GetZaxis().SetTitleOffset(0.7)
            obj.GetZaxis().SetLabelFont(132)
            obj.GetZaxis().SetLabelSize(0.05)
    elif "Leg" in Type:
        obj.SetBorderSize(1)
        obj.SetTextFont(132)
        obj.SetTextSize(0.05)
        obj.SetLineColor(1)
        obj.SetLineStyle(1)
        obj.SetLineWidth(1)
        obj.SetFillColor(0)
        obj.SetFillStyle(1001)


def Print(canvas,prefix,hasSMS):
    filename = prefix
    if hasSMS:
        addname = hasSMS.rstrip(".root")
        while addname.count("_") > 0:
            addname = addname[addname.index("_")+1:]
        filename += "_"+addname
    filename += ".eps"
    canvas.Print(filename)

def printInput(tree,inputpars):
    
    for key in inputpars.keys():
        print key,getattr(tree,key)        
        
        
def set_palette(gStyle,name="none", ncontours=999):
        """Set a color palette from a given RGB list
        stops, red, green and blue should all be lists of the same length
        see set_decent_colors for an example"""
        
        from array import array

        if name == "gray" or name == "grayscale":
                stops = [0.00, 0.34, 0.61, 0.84, 1.00]
                red     = [1.00, 0.84, 0.61, 0.34, 0.00]
                green = [1.00, 0.84, 0.61, 0.34, 0.00]
                blue    = [1.00, 0.84, 0.61, 0.34, 0.00]
        else:
                # default palette, looks cool
                stops = [0.00, 0.34, 0.61, 0.84, 1.00]
                red     = [0.00, 0.00, 0.87, 1.00, 0.51]
                green = [0.00, 0.81, 1.00, 0.20, 0.00]
                blue    = [0.51, 1.00, 0.12, 0.00, 0.00]

        s = array('d', stops)
        r = array('d', red)
        g = array('d', green)
        b = array('d', blue)

        npoints = len(s)
        TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
        gStyle.SetNumberContours(ncontours)

def getContours(gROOT,vals,hist,fit=None):
        """Get contour graphs from a histogram with contour values vals"""
        from array import array

        res = {}
        canv = TCanvas("getContour_canvas","getContour_canvas",0,0,500,500)
        canv.cd()
        h2 = hist.Clone()
        contours = array('d',vals)
        h2.SetContour(len(vals),contours)
        h2.Draw("CONT Z LIST")
        canv.Update()
        conts = gROOT.GetListOfSpecials().FindObject("contours")
        for ival,val in enumerate(vals):
                contLevel = conts.At(ival)
                res[val] = contLevel.First()
                for cont in contLevel:
                        if cont.GetN() > res[val].GetN(): res[val] = cont     #Get the contour wiht highest number of points 

        if fit:
                f1 = TF1("f1",fit,0.,1000.)
                for val in vals:
                        curv = res[val].Clone()
                        curv.Sort()
                        xmin = curv.GetX()[0]
                        xmax = curv.GetX()[curv.GetN()-1]
                        f1.SetMinimum(xmin)
                        f1.SetMaximum(xmax)
                        curv.Fit(f1)
                        fit = TGraph(curv.FindObject("f1"))
                        res[val] = fit.Clone()

        canv.Clear()

        return res

def getData(fname,Rmax=1.,condmax=0.001):
    infile = open(fname,'r')
    data = infile.read()
    pts = data[:data.find('#END')-1].split('\n')
    not_tested = TGraph()
    exc = TGraph()
    allow = TGraph()
    not_cond = TGraph()
    
    xv = []
    yv = []
    limv = []
    condv = []
    resv = []
    for pt in pts:
        x,y,res,lim,cond,tot = pt.split()        
        R = float(eval(res))/float(eval(lim))
        if eval(res) < 0.: continue
        if cond == 'None': cond = '0.'
        x = eval(x)
        y = eval(y)
        lim = eval(lim)
        cond = eval(cond)
        res = eval(res)
        xv.append(x)
        yv.append(y)
        limv.append(lim)
        condv.append(cond)
        resv.append(res)
        if cond > condmax: not_cond.SetPoint(not_cond.GetN(),x,y)
        if R < 0.:
            not_tested.SetPoint(not_tested.GetN(),x,y)
        elif R >= Rmax:
            exc.SetPoint(exc.GetN(),x,y)
        elif R < Rmax:
            allow.SetPoint(allow.GetN(),x,y)
        else:
            print 'Unknown R value',R
            sys.exit()
            
    infile.close()            
    return {'exc' : exc, 'not_tested' : not_tested, 'not_cond' : not_cond, 'allow' : allow, 'xv' : xv, 'yv' : yv, 'resv' : resv, 'limv' : limv, 'condv' : condv}

def getEnvelope(excluded,consecutive_bins=3):

    exc_curve = TGraph()
    exc = copy.deepcopy(excluded)
    exc.Sort()
    x1,y1 = Double(), Double()
    exc.GetPoint(0,x1,y1)
    yline = []
    for ipt in range(exc.GetN()+1): 
        x,y = Double(), Double()
        dmin = 0.
        if ipt < exc.GetN(): exc.GetPoint(ipt,x,y)
        if ipt != exc.GetN() and x == x1: yline.append(y)
        else:
            yline = sorted(yline,reverse=True)
            dy = [abs(yline[i]-yline[i+1]) for i in range(len(yline)-1)]
            if len(yline) <= 3 or exc_curve.GetN() == 0:
                newy = max(yline)
                if len(dy) > 2: dmin = min([abs(yline[i]-yline[i+1]) for i in range(len(yline)-1)])
            else:
                newy = max(yline)         
#                dmin = min(dy)
                dmin = sum(dy)/float(len(dy))
                for iD in range(len(dy)-1):
                    if dy[iD] <= dmin and dy[iD+1] <= dmin:
                        newy = yline[iD]
                        break
            exc_curve.SetPoint(exc_curve.GetN(),x1,newy+dmin/2.)
            x1 = x
            yline = [y]

    x2,y2 = Double(), Double()
    exc_curve.GetPoint(exc_curve.GetN()-1,x2,y2)
    exc_curve.SetPoint(exc_curve.GetN(),x2,0.)    #Close exclusion curve at zero
    return exc_curve


def getMetadata(filename,tags):
    infile = open(filename,'r')
    data = infile.read()
    info = data[data.find('#END'):].split('\n')
    metadata = {}
    for tag in tags: metadata[tag] = None
    if len(info) > 0:
        for line in info:
            for tag in tags:
                if tag in line:
                    if not metadata[tag]: metadata[tag] = []
                    entry = line.lstrip(tag+' :').rstrip()
                    if ':' in entry: entry = entry.split(':')
                    metadata[tag].append(entry)

    infile.close()
    return metadata


def getRootPlots(metadata):    
    plots = {}
    if metadata['Root file'] and os.path.isfile(metadata['Root file'][0]):
        rootfile = TFile(metadata['Root file'][0],"read")
        objs = gDirectory.GetListOfKeys()
        for ob in objs:
            add = False
            Tob = ob.ReadObj()
            if type(Tob) != type(TGraph()): continue
            if metadata['Root tag']:
                for rootTag in metadata['Root tag']:
                    Tag = rootTag
                    if type(Tag) == type([]) and len(Tag) > 1: Tag = Tag[0]
                    if Tag == ob.GetName():    add = rootTag
            else:
                add = 'Official Exclusion'
            if add:
                if type(add) == type([]): add = add[1]
                plots[add] = copy.deepcopy(Tob)
                
    return plots

def convertLabels(indic,use_dic=None,exclusive=False):
    
    outdic = {}
    if use_dic:
        myLabels = globals()[use_dic]
    else:
        myLabels = EXTPAR_dic
        myLabels.update(MINPAR_dic)
        myLabels.update(MassPDG_dic)
        myLabels.update(Observables_dic)
    for key in indic.keys():
        if str(key) in myLabels: outdic[myLabels[str(key)]] = indic[key]
        elif not exclusive: outdic[str(key)] = indic[key]
        
    return outdic

def getBestAnalysis(ana_list,sqrts=8.):
    
    R_best_Good = 0.
    Th_best_Good = 0.
    Cond_best_Good = 0.
    Ana_best_Good = "NONE"
    R_best_Bad = 0.
    Th_best_Bad = 0.
    Cond_best_Bad = 0.
    Ana_best_Bad = "NONE"
    for ana in ana_list:
        if ana['AnalysisSqrts'] != sqrts: continue
        if ana['exptlimit'] <= 0.: continue
        if ana['maxcond'] < 0.2:
            if not R_best_Good or R_best_Good < ana['tval']/ana['exptlimit']:
                R_best_Good = ana['tval']/ana['exptlimit']
                Th_best_Good = ana['tval']
                Cond_best_Good = ana['maxcond']
                Ana_best_Good = ana['AnalysisName']+':'+ana['AnalysisTopo']
        else:
            if not R_best_Bad or R_best_Bad < ana['tval']/ana['exptlimit']:
                R_best_Bad = ana['tval']/ana['exptlimit']
                Th_best_Bad = ana['tval']
                Cond_best_Bad = ana['maxcond']
                Ana_best_Bad = ana['AnalysisName']+':'+ana['AnalysisTopo']
            
    best_dic = {"R_best_Good" : R_best_Good, "Th_best_Good" : Th_best_Good, "Cond_best_Good" : Cond_best_Good, "Ana_best_Good" : Ana_best_Good, "R_best_Bad" : R_best_Bad, "Th_best_Bad" : Th_best_Bad, "Cond_best_Bad" : Cond_best_Bad, "Ana_best_Bad" : Ana_best_Bad}
        
    return best_dic

def getAnalysesOptions(analyses):
 
    markers = [20,21,22,23,29]
    colorsA = ['kGreen+1','kMagenta','kMagenta+2','kAzure-6','kMagenta+3','kAzure+2', 'kMagenta-4','kAzure+10','kMagenta-9','kAzure+1','kAzure-7','kAzure-2','kAzure-5']
    colorsB = ['kRed+2','kOrange+1','kPink-2','kRed-5','kOrange-3','kRed-6','kRed-4', 'kOrange+4']
    analyses = list(set(analyses))
    analyses_opts = {}
    allopts = []
    for f in analyses:
        imarker = 0
        icolor = 0
        if 'TChi' in f or 'TSlep' in f: usecolors = colorsB
        else: usecolors = colorsA
        while [usecolors[icolor],markers[imarker]] in allopts:
            if icolor == len(usecolors)-1 and imarker == len(markers)-1:
                print 'getAnalysesOptions: Number of analyses exceeded number of possible options'
                print len(analyses),len(markers)*len(colorsA),len(markers)*len(colorsB)
                print f
                sys.exit()
                
            icolor += 1
            if icolor >= len(usecolors):
                icolor = 0
                imarker += 1
         
        Mstyle = markers[imarker]
        Mcolor = usecolors[icolor]
        analyses_opts[f] = {"MarkerStyle" : Mstyle, "MarkerColor" : Mcolor}
        allopts.append([Mcolor,Mstyle])
        
    return analyses_opts


def checkOrderBy(variable,tree,friends):
    
    if len(friends) == 0:
        return True
    varlist = []
    nevts = tree.GetEntries()
    for iev in range(nevts):
        tree.GetEntry(iev)
        var = GetValue(tree,variable)
        if 'file' in variable.lower():
            var = str(var)
            var = var[:var.rfind('.')]            
        varlist.append(var)  
    for friend in friends:
        ffriend = TFile(friend)
        objs = ffriend.GetListOfKeys()        
        friendTrees = []
        for ob in objs:
            Tob = ob.ReadObj()
            if type(Tob) == type(TTree()):
                friendTrees.append(Tob)

        for tfriend in friendTrees:
            if tfriend.GetEntries() != nevts:
                print friend,'and tree number of entries do not match'
                return False
            for iev in range(nevts):
                tfriend.GetEntry(iev)
                var = GetValue(tfriend,variable)
                if 'file' in variable.lower():
                    var = str(var)
                    var = var[:var.rfind('.')]    
                if var != varlist[iev]:
                    print friend,'and tree',variable,'do not match at event',iev
                    print 'friend value:',var,'tree value:',varlist[iev]
                    return False    
            tfriend.Delete()
        ffriend.Close()
            
    return True


def getContours(tgr,contVals):
    """
    Returns a list of TGraphs containing the curves corresponding to the
    contour values contVals from the input TGraph2D object
    :param tgr: ROOT TGraph2D object containing the x,y,r points
    :param contVals: r-values for the contour graphs
     
    :return: a dictionary, where the keys are the contour values
             and the values are a list of TGraph objects containing the curves
             for the respective contour value (e.g. {1. : [TGraph1,TGraph2],...})
    """
    
    if tgr.GetN() == 0:
        logger.info("No excluded points found for %s" %tgr.GetName())
        return None
    
    cVals = sorted(contVals)
    #Draw temp plot:
    h = tgr.GetHistogram()    
    #Get contour graphs:
    c1 = TCanvas()
    h.SetContour(len(cVals),array('d',cVals))
    h.Draw("CONT Z LIST")
    c1.Update()
    clist = gROOT.GetListOfSpecials().FindObject("contours")
    cgraphs = {}
    for i in range(clist.GetSize()):
        contLevel = clist.At(i)
        curv = contLevel.First()
        cgraphs[cVals[i]] = []
        for j in range(contLevel.GetSize()):
            cgraphs[cVals[i]].append(curv)
            curv = contLevel.After(curv)

    return cgraphs
        
