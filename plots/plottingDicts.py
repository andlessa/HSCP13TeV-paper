"""
Some definitions of variables and labels useful for plotting
"""

#Some SLHA parameters
EXTPAR_dic = {'1' : 'MG1','2' : 'MG2','3' : 'MG3','11' : 'At',
              '12' : 'Ab','13' : 'Al','23' : 'mu','26' : 'MH3',
              '31' : 'Ml1','32' : 'Ml2','33' : 'Ml3','34' : 'Mr1',
              '35' : 'Mr2','36' : 'Mr3','41' : 'Mq1','42' : 'Mq2',
              '43' : 'Mq3', '44' : 'Mu1','45' : 'Mu2','46' : 'Mu3',
              '47' : 'Md1','48' : 'Md2','49' : 'Md3'}

MINPAR_dic = {'3' : 'tanb'}

#Mass variables and the corresponding PDGs
MassPDG_dic = {'24' : 'W_mass','25' : 'h_mass','35' : 'H_mass','36' : 'H3_mass','37' : 'Hp_mass',
               '5' : 'b_mass','1000001' : 'Mdl','2000001' : 'Mdr','1000002' : 'Mul',
               '2000002' : 'Mur','1000003' : 'Msl','2000003' : 'Msr','1000004' : 'Mcl',
               '2000004' : 'Mcr','1000005' : 'Mb1','2000005' : 'Mb2','1000006' : 'Mt1',
               '2000006' : 'Mt2','1000011' : 'SmL_mass','2000011' : 'SmR_mass',
               '1000012' : 'Snm_mass','1000013' : 'SmuL_mass','2000013' : 'SmuR_mass',
               '1000014' : 'Snmu_mass','1000015' : 'Stau1_mass','2000015' : 'Stau2_mass',
               '1000016' : 'Sntau_mass','1000021' : 'SGl_mass','1000022' : 'So1_mass',
               '1000023' : 'So2_mass','1000025' : 'So3_mass','1000035' : 'So4_mass',
               '1000024' : 'C1p_mass','1000037' : 'C2p_mass'}

#Some observables
Observables_dic = {'relicdensity' : 'Omega','g-2' : 'gmuon','BSG' : 'Bsgm',
                   'protonSIxsec' : 'pSI','protonSDxsec' : 'pSD','Bsmumu' : 'Bsmumu'}

#Latex syntax for variables
Var_dic = {'So4_mass': "m_{#tilde{#chi}^{0}_{4}} (GeV)", 'pSI': "#sigma(p,SI) (pb)", 
           'H3_mass': "m_{A} (GeV)", 'SmL_mass': "m_{#tilde{e}_{L}} (GeV)", 
           'Mr1': "#tilde{m}_{#tilde{e}_{R}} (GeV)", 'pSD': "#sigma(p,SD) (pb)", 
           'Mr3': "#tilde{m}_{#tilde{#tau}_{R}} (GeV)", 'Ml2': "#tilde{m}_{#tilde{#mu}_{L}} (GeV)", 
           'Ml3': "#tilde{m}_{#tilde{#tau}_{L}} (GeV)", 'MG1': "M_{1} (GeV)", 
           'Ml1': "#tilde{m}_{#tilde{e}_{L}} (GeV)", 'SmR_mass': "m_{#tilde{e}_{R} (GeV)", 
           'bsmumu': "BR(B_{s} #rightarrow #mu #mu)", 'Bsmumu': "BR(B_{s} #rightarrow #mu #mu)", 
           'gmuon': "a_{#mu}",'Gmuon': "#Deltaa_{#mu}", 'h_mass': "m_{h} (GeV)",
           'Mq1': "#tilde{m}_{#tilde{Q}}(1)} (GeV)", 'Mq3':    "#tilde{m}_{#tilde{Q}}(3)} (GeV)", 
           'Mq2': "#tilde{m}_{#tilde{Q}}(2)} (GeV)", 'Am': 'A_{#tilde{#mu}} (GeV)', 
           'Md2': "#tilde{m}_{#tilde{d}}(2)} (GeV)", 'Md3': "#tilde{m}_{#tilde{d}}(3)} (GeV)", 
           'Md1': "#tilde{m}_{#tilde{d}}(1)} (GeV)", 'Omega': "#Omega_{#tilde{#chi}_{1}^{0}} h^{2}", 
           'MH3': "M_{A} (GeV)", 'So2_mass': "m_{#tilde{#chi}^{0}_{2}} (GeV)", 
           'Mu1': "#tilde{m}_{#tilde{u}}(1)} (GeV)", 'Mu3': "#tilde{m}_{#tilde{u}}(3)} (GeV)", 
           'Mu2': "#tilde{m}_{#tilde{u}}(2)} (GeV)", 'Mtp': "m_{top} (GeV)", 'Ab': 'A_{b} (GeV)', 
           'So1_mass': "m_{#tilde{#chi}^{0}_{1}} (GeV)", 'MG3': "M_{3} (GeV)", 
           'Snm_mass': "m_{#tilde{#nu}_{#mu}} (GeV)", 'MG2': "M_{2} (GeV)", 'tb': "tan#beta", 
           'So3_mass': "m_{#tilde{#chi}^{0}_{3}} (GeV)", 'Al': 'A_{l} (GeV)', 'mu': '#mu (GeV)', 
           'C1p_mass': "m_{#tilde{#chi}^{#pm}_{1}} (GeV)", 'At': 'A_{t} (GeV)', 
           'Mr2': "#tilde{m}_{#tilde{#mu}_{R}} (GeV)", 'Bsgm': "BR(b #rightarrow s #gamma)", 
           'bsgmm': "BR(b #rightarrow s #gamma)", 'C2p_mass': "m_{#tilde{#chi}^{#pm}_{2}} (GeV)",
           "epRat" : "#epsilon^{MSSM}/#epsilon^{SM}", "epMSSM" : "#epsilon^{MSSM}", 
           "epSM" : "#epsilon^{SM}", "Smu1_mass": "m_{#tilde{#mu}_{1}} (GeV)", 
           "pSI_eff" : "#sigma(p,SI)^{eff} (pb)", 
           "mC1-mN1" : "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} (GeV)",
           "mSmu1-mN1" : "m_{#tilde{#mu}_{1}}-m_{#tilde{#chi}^{0}_{1}} (GeV)",
           "mSlep-mN1" : "m_{#tilde{l}}-m_{#tilde{#chi}^{0}_{1}} (GeV)", 
           "mSl1-mN1" : "m_{#tilde{#tau}_{1}}-m_{#tilde{#chi}^{0}_{1}} (GeV)",
           'SGl_mass' : 'm_{#tilde{g}} (GeV)','gl_C1tb' : 'BR(#tilde{g} #rightarrow #tilde{#chi}_{1}^{#pm} + tb)', 
           'gl_sbb' : 'BR(#tilde{g} #rightarrow #tilde{b}_1 + b)',
           'gl_N2QQ' : 'BR(#tilde{g} #rightarrow #tilde{#chi}_{2}^{0} + tt,bb)',
           'gl_N1tt' : 'BR(#tilde{g} #rightarrow #tilde{#chi}_{1}^{0} + tt)',
           'gl_N1bb' : 'BR(#tilde{g} #rightarrow #tilde{#chi}_{1}^{0} + bb)',
           'N2_N1h' : 'BR(#tilde{#chi}_{2}^{0} #rightarrow #tilde{#chi}_{1}^{0} + h)',
           'gl_N1x' : '#mathcal{B}(#tilde{g} #rightarrow #tilde{#chi}_{1}^{0} + t#bar{t},b#bar{b},qq)',
           'SQ_N1x' : 'BR(#tilde{q} #rightarrow #tilde{#chi}_{1}^{0} + X)',
           'gl_N1g' : 'BR(#tilde{g} #rightarrow #tilde{#chi}_{1}^{0} + g)',
           'gl_NIg' : 'BR(#tilde{g} #rightarrow #tilde{#chi}_{2,3,4}^{0} + g)',
           "XsecTot" : "#sigma_{Total} (fb)","Long_Frac" : "#sigma(long topologies)/#sigma_{total}",
           "Miss_Frac" : "#sigma(missing topologies)/#sigma_{total}",
           "Asym_Frac" : "#sigma(asymmetric topologies)/#sigma_{total}",
           "Long_Frac" : "#sigma(long topologies)/#sigma_{total}",           
           "Outside_Frac" : "#sigma(outside grid)/#sigma_{total}",           
           "totalxsec_fb" : "#sigma_{total} (fb)",
           "mN2-mN1" : "m_{#tilde{#chi}^{0}_{2}}-m_{#tilde{#chi}^{0}_{1}} (GeV)", 
           "SQ_mass" : "m_{#tilde{q}} (GeV)","St1_mass" : "m_{#tilde{t}_{1}} (GeV)", 
           "Sb2_mass" : "m_{#tilde{b}_{1}} (GeV)","Sb1_mass" : "m_{#tilde{b}_{1}} (GeV)", 
           "St2_mass" : "m_{#tilde{t}_{2}} (GeV)",'C1pN2_xsec' : "#sigma(#tilde{#chi}_{1}^{+} #tilde{#chi}_2^{0}) (fb)",
           'C1mN2_xsec' : "#sigma(#tilde{#chi}_{1}^{-} #tilde{#chi}_2^{0}) (fb)",
           'C1N2_xsec' : "#sigma(#tilde{#chi}_{1}^{#pm} #tilde{#chi}_{2}^{0}) (fb)",
           'C1_W' : "#Gamma_{#tilde{#chi}_{1}^{#pm}} (GeV)",
           'gl_W' : "#Gamma_{#tilde{g}} (GeV)", 'T1_W' : "#Gamma_{#tilde{t}_{1}} (GeV)",
           'C1_ct' : "c #tau_{#tilde{#chi}_{1}^{#pm}} (m)"}





#Expressions for computing some variables:
Exp_dic = {"Smu1_mass" : "min(TREENAME.SmL_mass,TREENAME.SmR_mass)",
           "Smu2_mass" : "max(TREENAME.SmL_mass,TREENAME.SmR_mass)",
           "pSI_eff" : "TREENAME.pSI*TREENAME.Omega/0.11", 
           "mC1-mN1" : "abs(TREENAME.C1p_mass)-abs(TREENAME.So1_mass)",
           "mSmu1-mN1" : "min(TREENAME.SmL_mass,TREENAME.SmR_mass)-abs(TREENAME.So1_mass)",
           "mSlep-mN1" : "min(TREENAME.SmL_mass,TREENAME.SmR_mass,TREENAME.Sl1_mass)-abs(TREENAME.So1_mass)",
           "mSl1-mN1" : "TREENAME.Sl1_mass-abs(TREENAME.So1_mass)",
           "Miss_Frac" : "TREENAME.Missed_Topologies/(TREENAME.totalxsec_fb)",
           "Long_Frac" : "TREENAME.Long_Cascades/(TREENAME.totalxsec_fb)",
           "Asym_Frac" : "TREENAME.Asymmetric_Branches/(TREENAME.totalxsec_fb)",
           "Outside_Frac" : "TREENAME.Outside_Grid/(TREENAME.totalxsec_fb)",
           "mN2-mN1" : "abs(TREENAME.So2_mass)-abs(TREENAME.So1_mass)", 
           "SQ_mass" : "(TREENAME.Mur+TREENAME.Mcr+TREENAME.Mdr+TREENAME.Msr+TREENAME.Mul+TREENAME.Mcl+TREENAME.Mdl+TREENAME.Msl)/8.",
           "St1_mass" : "TREENAME.Mt1","St2_mass" : "TREENAME.Mt2","Sb1_mass" : "TREENAME.Mb1",
           "Sb2_mass" : "TREENAME.Mb2",
           "XsecTot" : "(TREENAME.Tested + TREENAME.No_Limit + TREENAME.No_Analysis + TREENAME.Bad_Conditions + TREENAME.Long_Topology + TREENAME.Asymmetric_Top)",
           'C1N2_xsec' : "TREENAME.C1mN2_xsec + TREENAME.C1pN2_xsec",
           'C1_ct' : "(6.582e-25)*(2.99e+08)/(TREENAME.C1_W)"}


#Txnames and the corresponding SUSY process 
SMS_dic = {'TChiChipmSlepL' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} #tilde{l}^{#pm}#nu,l^{#pm}#tilde{#nu})#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} #tilde{l}^{#pm}l^{#mp},#nu#tilde{#nu})',
           'TChiChipmSlepStau' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} #tilde{#tau}^{#pm}#nu)#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} #tilde{l}^{#pm}l^{#mp})',
           'TChiChipmStauStau' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} #tilde{#tau}^{#pm}#nu)#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} #tilde{#tau}^{#pm}#tau^{#mp})',
           'TChiWZ' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} W^{#pm}#tilde{#chi}_{1}^{0})#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} Z#tilde{#chi}_{1}^{0})',
           'TChiWZon' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} W^{#pm}#tilde{#chi}_{1}^{0})#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} Z#tilde{#chi}_{1}^{0})',
           'TChiWZoff' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} W^{#pm}#tilde{#chi}_{1}^{0})#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} Z#tilde{#chi}_{1}^{0})', 
           'TSlepSlep' : '#tilde{l}^{+}#tilde{l}^{-},#tilde{l} #scale[0.8]{#rightarrow} l#tilde{#chi}_{1}^{0}',
           'T1bbbb' : '#tilde{g}#tilde{g},#tilde{g} #scale[0.8]{#rightarrow} bb#tilde{#chi}_{1}^{0}',
           'T1tbtb' : '#tilde{g}#tilde{g}, #tilde{g} #scale[0.8]{#rightarrow} tb#tilde{#chi}_{1}^{#pm}',
           'T1tttt' : '#tilde{g}#tilde{g}, #tilde{g} #scale[0.8]{#rightarrow} tt#tilde{#chi}_{1}^{0}',
           'T2' : '#tilde{q}#tilde{q}, #tilde{q} #scale[0.8]{#rightarrow} q#tilde{#chi}_{1}^{0}',
           'T2bb' : '#tilde{b}#tilde{b}, #tilde{b} #scale[0.8]{#rightarrow} b#tilde{#chi}_{1}^{0}',
           'T2tt' : '#tilde{t}#tilde{t}, #tilde{t} #scale[0.8]{#rightarrow} t#tilde{#chi}_{1}^{0}',
           'T5WW' : '#tilde{g}#tilde{g}, #tilde{g} #scale[0.8]{#rightarrow} qq#tilde{#chi}_{1}^{#pm}',
           'T6WW' : '#tilde{q}#tilde{q}, #tilde{q} #scale[0.8]{#rightarrow} q#tilde{#chi}_{1}^{#pm}',
           'T6bbWW' : '#tilde{t}#tilde{t}, #tilde{t} #scale[0.8]{#rightarrow} b#tilde{#chi}_{1}^{#pm}',
           'T6bbWWoff' : '#tilde{t}#tilde{t}, #tilde{t} #scale[0.8]{#rightarrow} b#tilde{#chi}_{1}^{#pm}',
           'T5tttt' : '#tilde{g}#tilde{g}, #tilde{g} #scale[0.8]{#rightarrow} t#tilde{t}_{1}',
           'T6bbZZ' : '#tilde{b}#tilde{b}, #tilde{b} #scale[0.8]{#rightarrow} b#tilde{#chi}_{2}^{0}',
           'T6ttWW' : '#tilde{b}#tilde{b}, #tilde{b} #scale[0.8]{#rightarrow} t#tilde{#chi}_{1}^{#pm}',
           'T1' : '#tilde{g}#tilde{g}, #tilde{g} #scale[0.8]{#rightarrow} qq#tilde{#chi}_{1}^{0}', 
           'TChiChipmStauL' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} #tilde{#tau}^{#pm}#nu_{#tau},#tau^{#pm}#tilde{#nu}_{#tau})#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} #tilde{#tau}^{#pm}l^{#mp},#nu#tilde{#nu}_{#tau})',
           'TChipChimSlepSnu' : '#tilde{#chi}_{1}^{#pm} #tilde{#chi}_{1}^{#pm} #scale[0.8]{#rightarrow} l #nu l #nu',
           'TChipChimStauSnu' : '#tilde{#chi}_{1}^{#pm} #tilde{#chi}_{1}^{#pm} #scale[0.8]{#rightarrow} #tau #tau #nu_{#tau} #nu_{#tau}',
           'TChiChiSlepSlep' : '#tilde{#chi}_{2}^{0} #tilde{#chi}_{3}^{0} #scale[0.8]{#rightarrow} 4l',
           'TChiChipmHW' : '#tilde{#chi}_{1}^{#pm}(#scale[0.8]{#rightarrow} W^{#pm}#tilde{#chi}_{1}^{0})#tilde{#chi}_{2}^{0}(#scale[0.8]{#rightarrow} h#tilde{#chi}_{1}^{0})', 
           'T2bbWW' : '#tilde{t}#tilde{t}, #tilde{t} #scale[0.8]{#rightarrow} bW#tilde{#chi}_{1}^{0}'}

GluinoTops = ['T1', 'T5tttt', 'T1bbbb', 'T5WW', 'T1tttt','T1tbtb']
SquarkTops = ['T2','T6WW']
StopTops = ['T2tt','T6bbWW']
SbotTops = ['T6ttWW', 'T2bb', 'T6bbZZ']
EWinoTops = ['TChiWZ', 'TChiChipmSlepL', 'TChiChipmSlepStau']
SlepTops = ['TSlepSlep']

GrOpts_dic = {
#Gluino topologies:
'T1' : {'MarkerColor' : 'kMagenta+2', 'MarkerStyle' : 20},
'T1tttt' : {'MarkerColor' : 'kMagenta-6', 'MarkerStyle' : 21},
'T1bbbb' : {'MarkerColor' : 'kMagenta-9', 'MarkerStyle' : 22},
'T1tbtb' : {'MarkerColor' : 'kMagenta+2', 'MarkerStyle' : 23},
'T5tttt' : {'MarkerColor' : 'kMagenta+3', 'MarkerStyle' : 29},
'T5WW' : {'MarkerColor' : 'kPink-9', 'MarkerStyle' : 20},
#Squark topologies:
'T2' : {'MarkerColor' : 'kRed-2', 'MarkerStyle' : 20},
'T6WW' : {'MarkerColor' : 'kRed-6', 'MarkerStyle' : 21},
#Stop topologies:
'T2tt' : {'MarkerColor' : 'kAzure+2', 'MarkerStyle' : 20},
'T6bbWW' : {'MarkerColor' : 'kAzure-4', 'MarkerStyle' : 21},
'T6bbWWoff' : {'MarkerColor' : 'kAzure-4', 'MarkerStyle' : 21},
#Sbottom topologies
'T2bb' : {'MarkerColor' : 'kGreen+1', 'MarkerStyle' : 20},
'T2bbWW' : {'MarkerColor' : 'kGreen+2', 'MarkerStyle' : 23},
'T6ttWW' : {'MarkerColor' : 'kGreen+3', 'MarkerStyle' : 21},
'T6bbZZ' : {'MarkerColor' : 'kGreen', 'MarkerStyle' : 22},
#EW-ino topologies:
'TChiChipmHW' : {'MarkerColor' : 'kOrange-7', 'MarkerStyle' : 20},
'TChiWZ' : {'MarkerColor' : 'kOrange-9', 'MarkerStyle' : 20},
'TChiWZon' : {'MarkerColor' : 'kOrange-9', 'MarkerStyle' : 21},
'TChiWZoff' : {'MarkerColor' : 'kOrange-9', 'MarkerStyle' : 22},
'TChiChipmSlepL' : {'MarkerColor' : 'kOrange-3', 'MarkerStyle' : 23},
'TChiChipmSlepStau' : {'MarkerColor' : 'kOrange+7', 'MarkerStyle' : 29},
'TChiChipmStauL' : {'MarkerColor' : 'kOrange+5', 'MarkerStyle' : 20},
'TChipChimStauSnu' : {'MarkerColor' : 'kOrange+2', 'MarkerStyle' : 21},
'TChiChiSlepSlep' : {'MarkerColor' : 'kOrange+1', 'MarkerStyle' : 22},
'TChipChimSlepSnu' : {'MarkerColor' : 'kOrange+4', 'MarkerStyle' : 29},
'TChiChipmStauStau' : {'MarkerColor' : 'kOrange+6', 'MarkerStyle' : 20},
#Slepton topologies:
'TSlepSlep' : {'MarkerColor' : 'kAzure+7', 'MarkerStyle' : 20}
}
