#!/usr/bin/env python



import os
import argparse
from collections import OrderedDict
from prettyDescriptions import prettyTxname


xmin = 500.
xmax = 5000.


def main(mainRoot,friends,xprint,DoPrint,outputFolder,nbins):

    import AuxPlot
    from ROOT import ( kAzure,kRed,kGreen,kGray,kMagenta,kCyan,kViolet,kPink,
                    kOrange,kBlack,TGraph,gDirectory,gStyle,
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
        

    
    filename,friends = AuxPlot.infiles([mainRoot]+friends)
    print "Reading",filename,"..."
    r = TFile(filename,"read")
    #Get tree and additional info
    tree,lnames,_ = AuxPlot.getTree(gDirectory,friends,verbose=True)
    varnames = AuxPlot.GetVarNames(lnames+[xprint])

    #Get all analyses names and create histograms for all of them
    nevts = tree.GetEntries()


    #Define histograms:
    txHists = OrderedDict()
    colors = {}
    allHisto = TH1F("All","",nbins,xmin,xmax)
    #Loop over events
    for iev in range(nevts):
        tree.GetEntry(iev)
        
        #Get plotting variables    
        xval = AuxPlot.GetValue(tree,xprint)
        robsUL8 = AuxPlot.GetValue(tree,'robs_UL_8')
        robsEM8 = AuxPlot.GetValue(tree,'robs_EM_8')
        robsUL13 = AuxPlot.GetValue(tree,'robs_UL_13')
        robsEM13 = AuxPlot.GetValue(tree,'robs_EM_13')

        allHisto.Fill(xval)
        #Skip not excluded:
        if max([robsUL8,robsEM8,robsUL13,robsEM13]) < 1.:            
            continue

        if max([robsUL8,robsEM8]) > max([robsUL13,robsEM13]):
            sqrts = '8'
            if robsUL8 > robsEM8:
                tp = 'UL'
            else:
                tp = 'EM'
        else:
            sqrts = '13'
            if robsUL13 > robsEM13:
                tp = 'UL'
            else:
                tp = 'EM'

        txname = str(AuxPlot.GetValue(tree,'TxNames_%s_%s' %(tp,sqrts)))
        if '+' in txname and 'HSCP' in txname:
            txname = 'Multiple HSCP SMS'
        
        if not txname in txHists:
            txHists[txname] = TH1F(txname,"",nbins,xmin,xmax)
            
        txHists[txname].Fill(xval)
    
    
    #Create compact summary:
    hs =  THStack("","")
    #Sort txnames by maximum contribution:
    txHists = OrderedDict(sorted(txHists.iteritems(), 
                                 key=lambda x: x[1].GetEntries(),
                                 reverse=True))
    for txname in txHists:
        if txname == 'Other':      
            colors[txname] = kGray+1
        else:
            colors[txname] = cList.pop()
        txHists[txname].SetFillColor(colors[txname])
        txHists[txname].SetLineColor(colors[txname])        
        hs.Add(txHists[txname])
    
    plane = TCanvas("c1", "c1",0,0,1000,600)
    AuxPlot.Default(plane,"TCanvas")
    plane.cd()
    plane.SetRightMargin(0.3)
    
    gStyle.SetOptStat(0)
    
    hs.Draw()
    AuxPlot.Default(hs,'TH1')
    hs.GetXaxis().SetTitle(varnames[xprint])
    hs.GetXaxis().SetLabelSize(0.04)
    hs.GetYaxis().SetTitle("Number of Points")
    hs.GetYaxis().SetTitleOffset(0.75)


    #Legend
    leg = TLegend(0.6322645,0.288225,0.987976,0.9543058)
    AuxPlot.Default(leg,'TLegend')
    leg.SetMargin(0.2)
    leg.SetTextSize(0.04)
    for txname in txHists:        
        prettyTx = prettyTxname(txname.replace('+',''))
        if not prettyTx:
            prettyTx = txname
        leg.AddEntry(txHists[txname],prettyTx,"f")
    leg.Draw()
    
    #Title:
    
    gPad.RedrawAxis()
    gPad.Update()
    
    if DoPrint:
        if not DoPrint[0] == '.':
            DoPrint = '.'+DoPrint
        label = 'excludedTx'

        plotname = "%s%s"%(label,DoPrint)
        filename = os.path.join(outputFolder,plotname)
        plane.Print(filename)
    
    raw_input("Hit any key to close\n")


if __name__ == "__main__":
    
    """ Make a 1D histogram with the most contraining analyses"""
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--mainRootFile', 
            help='name of the main ROOT file containing plotting info. ', required=True, type = str)    
    ap.add_argument('-F', '--friends', 
            help='name or list of names of auxiliary ROOT files containing plotting info.', 
            nargs='+', action='append',type=str, default=[], required=False)
    ap.add_argument('-x', '--xprint', 
            help='Name of the variable to be printed in the x-axis', type = str, default = 'SGl_mass')
    ap.add_argument('-P', '--Print', 
            help='If set will print the plot to a file with the corresponding extension', type = str, default = None)
    ap.add_argument('-o', '--output', 
            help='Name of output folder to save plots', type = str, default = './')
    ap.add_argument('-n', '--nbins', 
            help='Number of bins to show', type = int, default = 20)

    
    args = ap.parse_args()
    
    
    if args.friends:
        args.friends = args.friends[0]
    
    main(args.mainRootFile,args.friends,args.xprint,args.Print,args.output,args.nbins)
    
    
