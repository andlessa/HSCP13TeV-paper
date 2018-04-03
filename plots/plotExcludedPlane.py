#!/usr/bin/env python



import argparse
from collections import OrderedDict


xmin = 0.
xmax = 4500.

#Total number of points:
N_bino_exc = 42039
N_bino_allow = 61370  
N_higgsino_exc = 48703
N_higgsino_allow = 77981
N_wino_exc = 36553
N_wino_allow =  43680

def main(mainRoot,friends,xprint,yprint,DoPrint,outputFolder):

    import AuxPlot
    from ROOT import ( kAzure,kRed,kGreen,kGray,kMagenta,kCyan,kViolet,kPink,
                    kOrange,kBlack,TGraph,gDirectory,gStyle,TMultiGraph,
                    TFile,TCanvas,TH1F,TLegend,gPad,THStack,TLatex )
    
    cList = [kPink,kGreen,kMagenta,kRed,kAzure,kOrange,kCyan,kViolet]
    nc = len(cList)
    for c in cList[:nc]:
        cList.append(c+3)
    for c in cList[:nc]:
        cList.append(c-3)
    for c in cList[:nc]:
        cList.append(c-2)
    for c in cList[:nc]:
        cList.append(c+2)
        
    txgrs = {}
            
    #Get input file and related ones
    filename,friends = AuxPlot.infiles([mainRoot]+friends)
    print "Reading",filename,"..."
    resfile = TFile(filename,"read")
    #Get tree and additional info
    tree,lnames,_ = AuxPlot.getTree(gDirectory,friends,verbose=True)
    #Get variable dictionary (for printing)
    varnames = AuxPlot.GetVarNames(lnames+[xprint,yprint])
    
    nevts = tree.GetEntries()
    #Loop over events
    for iev in range(nevts):
        tree.GetEntry(iev)
     
        #Get plotting variables    
        xval = AuxPlot.GetValue(tree,xprint)
        yval = AuxPlot.GetValue(tree,yprint)
        robsUL8 = AuxPlot.GetValue(tree,'robs_UL_8')
        robsEM8 = AuxPlot.GetValue(tree,'robs_EM_8')
        robsUL13 = AuxPlot.GetValue(tree,'robs_UL_13')
        robsEM13 = AuxPlot.GetValue(tree,'robs_EM_13')


        minMass = min([AuxPlot.GetValue(tree,'Mur'),
                      AuxPlot.GetValue(tree,'Mcr'),
                      AuxPlot.GetValue(tree,'Mdr'),
                      AuxPlot.GetValue(tree,'Msr'),
                      AuxPlot.GetValue(tree,'Mul'),
                      AuxPlot.GetValue(tree,'Mcl'),
                      AuxPlot.GetValue(tree,'Mdl'),
                      AuxPlot.GetValue(tree,'Msl'),
                      AuxPlot.GetValue(tree,'St1_mass'),
                      AuxPlot.GetValue(tree,'SGl_mass')])
                      
                      
        yval =  minMass-AuxPlot.GetValue(tree,'So1_mass')

        if max([robsUL8,robsEM8]) > 1.: #Exclude pts excluded by 8 TeV
            continue            

        #Skip not excluded by 13 TeV:
        if not max([robsUL13,robsEM13]) > 1.:            
            continue

        if robsUL13 > robsEM13:
            txname = str(AuxPlot.GetValue(tree,'TxNames_UL_13'))
        else:
            txname = str(AuxPlot.GetValue(tree,'TxNames_EM_13'))

#         if AuxPlot.GetValue(tree,'SGl_mass') > 1000.: continue
        if not txname in ['T2','T2cc']: continue

        if not txname in txgrs:
            txgrs[txname] = TGraph()

        
        txgrs[txname].SetPoint(txgrs[txname].GetN(),xval,yval)
    
    resfile.Close()

    #Sort graphs by number of points:
    txGraphs = OrderedDict(sorted(txgrs.iteritems(), 
                                 key=lambda x: x[1].GetN(),reverse=True))

    
    plane = TCanvas("c1", "c1",0,0,800,600)
    AuxPlot.Default(plane,"TCanvas")
    plane.cd()
    plane.SetRightMargin(0.05)
    plane.SetLeftMargin(0.12)
    
    #Graph options:
    for txgr in txGraphs.values():
        txgr.SetMarkerStyle(20)
        txgr.SetMarkerSize(1.7)
        txgr.SetMarkerColor(cList.pop())        
        
    
    base = TMultiGraph()
    npts = {}
    for tx,txgr in txGraphs.items():
        print '%i pts excluded by %s'%(txgr.GetN(),tx)
        base.Add(txgr,"P")
        
    print 'Total points = %i'%sum(npts.values())
    base.Draw("AP")
    AuxPlot.Default(base,"TGraph")
    base.GetXaxis().SetTitle(varnames[xprint])
    base.GetYaxis().SetTitle(varnames[yprint])
    base.GetYaxis().SetTitleOffset(0.8)
#     base.GetXaxis().SetLimits(xmin,xmax)
#     base.GetYaxis().SetRangeUser(ymin,ymax)
    
    
    #Legend
    xleg1, yleg1 = 0.63, 0.74
    leg = TLegend(xleg1,yleg1,xleg1+0.35,yleg1+0.25)
    AuxPlot.Default(leg,'TLegend')
    for tx in txGraphs:
        leg.AddEntry(txGraphs[tx],tx,"P")
    leg.Draw()
        
    gPad.RedrawAxis()
    gPad.Update()
        
#     if DoPrint:
#         if not DoPrint[0] == '.':
#             DoPrint = '.'+DoPrint
#         label = 'excludedTx'
#         if lsptype:
#             label += '_%s' %lsptype                  
# 
#         plotname = "%s%s"%(label,DoPrint)
#         filename = os.path.join(outputFolder,plotname)
#         plane.Print(filename)
    
    raw_input("Hit any key to close\n")


if __name__ == "__main__":
    
    """ Make a 2D scatter plot the excluded points at 13 TeV"""
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--mainRootFile', 
            help='name of the main ROOT file containing plotting info. ', required=True, type = str)    
    ap.add_argument('-F', '--friends', 
            help='name or list of names of auxiliary ROOT files containing plotting info.', 
            nargs='+', action='append',type=str, default=[], required=False)
    ap.add_argument('-x', '--xprint', 
            help='Name of the variable to be printed in the x-axis', type = str, default = 'SGl_mass')
    ap.add_argument('-y', '--yprint', 
            help='Name of the variable to be printed in the y-axis', type = str, default = 'So1_mass')
    ap.add_argument('-P', '--Print', 
            help='If set will print the plot to a file with the corresponding extension', type = str, default = None)
    ap.add_argument('-o', '--output', 
            help='Name of output folder to save plots', type = str, default = './')

    
    args = ap.parse_args()
    
    
    if args.friends:
        args.friends = args.friends[0]
    
    main(args.mainRootFile,args.friends,args.xprint,args.yprint,args.Print,args.output)
    
    
