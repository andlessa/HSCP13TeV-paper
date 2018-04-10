#!/usr/bin/env python



import os
import argparse
import numpy as np
from array import array

xmin, xmax = 1e5,1e10


def main(mainRoot,friends,xprint,DoPrint,outputFolder,nbins):

    import AuxPlot
    from ROOT import (kAzure,kRed,kGreen,kGray,kMagenta,kOrange,kBlack,TGraph,
                      gDirectory,gStyle,TFile,TCanvas,TH1F,TLegend,gPad,THStack,TLatex)
    
    
    filename,friends = AuxPlot.infiles([mainRoot]+friends)
    print "Reading",filename,"..."
    r = TFile(filename,"read")
    #Get tree and additional info
    tree,lnames,_ = AuxPlot.getTree(gDirectory,friends,verbose=True)
    varnames = AuxPlot.GetVarNames(lnames+[xprint])
    #Make sure friends are properly ordered
#     if not AuxPlot.checkOrderBy('filename',tree,friends):
#         sys.exit()

    #Get all analyses names and create histograms for all of them
    nevts = tree.GetEntries()

    xbins = [10**y for y in np.arange(np.log10(xmin),np.log10(xmax),np.log10(xmax/xmin)/nbins)]
    xbins = array('d',xbins)
    #Define histograms:
    allowed = TH1F("Allowed","",len(xbins)-1,xbins)
    sms8 = TH1F("Excluded by 8 TeV","",len(xbins)-1,xbins)
    sms13 = TH1F("Excluded by 13 TeV","",len(xbins)-1,xbins)
    #Loop over events

    for iev in range(nevts):
        tree.GetEntry(iev)
        
        #Get plotting variables    
        xval = AuxPlot.GetValue(tree,xprint)
        robsUL8 = AuxPlot.GetValue(tree,'robs_UL_8')
        robsEM8 = AuxPlot.GetValue(tree,'robs_EM_8')
        robsUL13 = AuxPlot.GetValue(tree,'robs_UL_13')
        robsEM13 = AuxPlot.GetValue(tree,'robs_EM_13')
   
        if max([robsUL8,robsEM8,robsUL13,robsEM13]) < 1.:
            allowed.Fill(xval)            
        elif max([robsUL8,robsEM8]) > 1.:
            sms8.Fill(xval)
        elif max([robsUL13,robsEM13]) > 1.:
            sms13.Fill(xval)
            
    print "total excluded:",sms8.GetEntries() + sms13.GetEntries()
    print "allowed:",allowed.GetEntries()


    
    hs =  THStack("","")
    hs.Add(sms8)
    hs.Add(sms13)
    hs.Add(allowed)
    
    plane = TCanvas("c1", "c1",0,0,800,600)
    AuxPlot.Default(plane,"TCanvas")
    plane.cd()
    plane.SetRightMargin(0.05)
    plane.SetLeftMargin(0.13)
    plane.SetTitle("8 TeV Results")
    plane.SetLogy()
    plane.SetLogx()
    
    gStyle.SetOptStat(0)
    sms8.SetLineColor(kAzure-8)
    sms8.SetFillColor(kAzure-8)
    sms13.SetLineColor(kRed-3)
    sms13.SetFillColor(kRed-3)
    allowed.SetFillColor(kGray)
    allowed.SetLineColor(kGray)
    
    hs.Draw()
    AuxPlot.Default(hs,'TH1')
    hs.GetXaxis().SetTitle(varnames[xprint])
    hs.GetYaxis().SetTitle("Number of Points")
    hs.GetYaxis().SetTitleOffset(0.98)


    #Legend
    xleg1, yleg1 = 0.13, 0.74
    leg = TLegend(xleg1,yleg1,xleg1+0.35,yleg1+0.25)
    AuxPlot.Default(leg,'TLegend')
    leg.AddEntry(sms8,"Excluded (8 TeV)","f")
    leg.AddEntry(sms13,"Excluded (13 TeV)","f")
    leg.AddEntry(allowed,"Allowed","f")
    leg.Draw()
    
    gPad.RedrawAxis()
    gPad.Update()
    
    if DoPrint:
        if not '.' in DoPrint:
            DoPrint = '.'+DoPrint
        label = 'excludedHisto'
        froot = os.path.basename(mainRoot)  
        label += '_%s' %(froot[:froot.find('_')])
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
    
    
