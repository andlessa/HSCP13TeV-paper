#!/usr/bin/env python



import os
import argparse


 


def main(mainRoot,friends,xprint,DoPrint,outputFolder,nbins,xmin,xmax):

    import AuxPlot
    from ROOT import kAzure,kRed,kGreen,kGray,kMagenta,kOrange,kBlack,TGraph,gDirectory,gStyle,TFile,TCanvas,TH1F,TLegend,gPad,THStack,TLatex
    
    
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

    #Define histograms:
    sms8 = TH1F("Excluded by SModelS (8 TeV)","",nbins,xmin,xmax)
    sms13 = TH1F("Excluded by SModelS (13 TeV)","",nbins,xmin,xmax)
    allowed = TH1F("Allowed points","",nbins,xmin,xmax)
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
        if max([robsUL8,robsEM8,robsUL13,robsEM13]) < 1.:
            allowed.Fill(xval)
            
            if xval > 1.5 and AuxPlot.GetValue(tree,'Hp_mass') < 500.:
                print( AuxPlot.GetValue(tree,'Hp_mass'), AuxPlot.GetValue(tree,'filename'))
                        
            continue

        if max([robsUL8,robsEM8]) > 1.:
            sms8.Fill(xval)
        elif max([robsUL13,robsEM13]) > 1.:
            sms13.Fill(xval)
            
            
   
    print "8 TeV:", sms8.GetEntries()
    print "13 TeV:",sms13.GetEntries()
    nexcluded = sms8.GetEntries()+sms13.GetEntries()
    nallowed = allowed.GetEntries()
    
    print "total excluded:",nexcluded    
    print "allowed:",nallowed
    print "total:",allHisto.GetEntries()

    xtotal = allHisto.GetEntries()
    xexcluded = sms8.GetEntries()+sms13.GetEntries()    
    print "Fraction of excluded = ",xexcluded/xtotal,"Fraction of allowed = ",(xtotal-xexcluded)/xtotal
    
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
    
    tit = TLatex()
    tit.SetTextSize(0.045)
    tit.SetTextFont(12)
    tit.DrawLatexNDC(0.15,0.45,"#splitline{Excluded points = %i}{Allowed points = %i}" %(nexcluded,nallowed))
    
    
    gPad.RedrawAxis()
    gPad.Update()
    
    if DoPrint:
        plane.Print(DoPrint)
    
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
            help='Name of the output file to save the plot', type = str, default = None)
    ap.add_argument('-o', '--output', 
            help='Name of output folder to save plots', type = str, default = './')
    ap.add_argument('-n', '--nbins', 
            help='Number of bins to show', type = int, default = 20)
    ap.add_argument('-m', '--xmin', 
            help='Minimum value for x', type = float, default = 100.)
    ap.add_argument('-M', '--xmax', 
            help='Maximum value for x', type = float, default = 5000.)

    
    args = ap.parse_args()
    
    
    if args.friends:
        args.friends = args.friends[0]
    
    main(args.mainRootFile,args.friends,args.xprint,args.Print,args.output,args.nbins,args.xmin,args.xmax)
    
    
