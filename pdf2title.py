#!/usr/bin/python3

# Extracts title from all pdf files in current directory to a txt file
# Author: Cibin Joseph
# Use with python3

import glob, subprocess
from pdfrw import PdfReader
import os 

# Get all filenames to a list
filelist=sorted(glob.glob('*.pdf')+glob.glob('*.PDF'))

outfile=open('Title_Map.txt','w')
outfile.write('*** This title map was generated using a Python code by Cibin ***\n')
outfile.write('***  Update as neccessary ***\n\n')

indx=0
proc_createdummy=subprocess.Popen(['touch','dummyfile.txt'])
for filename in filelist:
    indx=indx+1
    reader=PdfReader(filename)

    # Extract title from file
    title=reader.Info.Title
    title=str(title)

    # Replace unnecessary () in title
    title=title.replace('(',' ')
    title=title.replace(')',' ')

    flag_pdf2txt=0
    if (title[0:4]=='None'):
        flag_pdf2txt=1
    elif ('untitled' in title):
        flag_pdf2txt=1
    elif ('Replace with your title' in title):
        flag_pdf2txt=1

    if (flag_pdf2txt==1):
        # convert pdf to txt and provide first line as title
        proc_convert=subprocess.Popen(['pdftotext','-f','1','-l','1',filename,'dummyfile.txt'])
        title=subprocess.check_output(['head','-n','1','dummyfile.txt']).decode('utf-8').rstrip()
        flag_pdf2txt=0

    outfile.write(filename+'  '+title+'\n')

outfile.close()

try:
    os.remove('dummyfile.txt')
except OSError:
    pass

print(str(indx)+' files parsed')
