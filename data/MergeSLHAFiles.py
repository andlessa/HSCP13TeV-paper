#!/usr/bin/env python


import os,sys,shutil,glob


if len(sys.argv) < 4:
    print('You must pass as arguments the 8 TeV and 13 TeV folders and the output folder')

for folder in sys.argv[1:4]:
    if not os.path.isdir(folder):
        print('Folder %s does not exist' %folder)
        sys.exit()

nmerge = 0
for f in glob.glob(sys.argv[1]+'/*.slha'):
#     if os.path.isfile(f.replace('slha_8','slha')):
#         continue
#     if not os.path.isfile(f.replace('slha_8','slha_13')):
#         continue    
    slhaF = open(f,'r')
    slhaData = slhaF.read()
    slhaF.close()
    slhaF = open(os.path.join(sys.argv[2],os.path.basename(f)),'r')
    newData = slhaF.read()
    slhaData += '\n\n'+newData[newData.find('XSECTION'):]
    slhaF.close()
    slhaF = open(os.path.join(sys.argv[3],os.path.basename(f)),'w')
    slhaF.write(slhaData+'\n')
    slhaF.close()
    nmerge += 1

print('merged %i files' %nmerge)
