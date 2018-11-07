#!/usr/bin/python3

# Extracts title from all pdf files in current directory to a txt file
# Author: Cibin Joseph
# Use with python3

import glob, subprocess
from pdfrw import PdfReader
import os, warnings

def extract_title(filename):
    'Extracts title from a given pdf file'
    reader=PdfReader(filename)

    # Extract title from file
    title=reader.Info.Title
    title=str(title)

    # replace unnecessary () in title
    title=title.replace('(',' ')
    title=title.replace(')',' ')
    return title


def extract_first_line(filename):
    'Extracts first line from pdf converted to txt file'

    try:
        proc_createdummy=subprocess.Popen(['touch','dummyfile.txt'])
        proc_convert=subprocess.Popen(['pdftotext','-f','1','-l','1',filename,'dummyfile.txt'])
        first_line=subprocess.check_output(['head','-n','1','dummyfile.txt']).decode('utf-8').rstrip()
        try:
            os.remove('dummyfile.txt')
        except OSError:
            pass
    except OSError:
        warnings.warn('Linux specific command not found. pdf to txt conversion not performed')
        first_line=''
        pass

    return first_line

print(extract_title('sample.pdf'))

## Get all filenames to a list
#filelist=sorted(glob.glob('*.pdf')+glob.glob('*.PDF'))
#
#outfile=open('Title_Map.txt','w')
#outfile.write('*** This title map was generated using a Python code by Cibin ***\n')
#outfile.write('***  Update as neccessary ***\n\n')
#
#indx=0
#proc_createdummy=subprocess.Popen(['touch','dummyfile.txt'])
#for filename in filelist:
#    indx=indx+1
#    reader=PdfReader(filename)
#
#    # Extract title from file
#    title=reader.Info.Title
#    title=str(title)
#
#    # replace unnecessary () in title
#    title=title.replace('(',' ')
#    title=title.replace(')',' ')
#
#    flag_pdf2txt=0
#    if (title[0:4]=='none'):
#        flag_pdf2txt=1
#    elif ('untitled' in title):
#        flag_pdf2txt=1
#    elif ('replace with your title' in title):
#        flag_pdf2txt=1
#
#    if (flag_pdf2txt==1):
#        # convert pdf to txt and provide first line as title
#        proc_convert=subprocess.popen(['pdftotext','-f','1','-l','1',filename,'dummyfile.txt'])
#        title=subprocess.check_output(['head','-n','1','dummyfile.txt']).decode('utf-8').rstrip()
#        flag_pdf2txt=0
#
#    outfile.write(filename+'  '+title+'\n')
#
#outfile.close()
#
#try:
#    os.remove('dummyfile.txt')
#except OSError:
#    pass
#
#print(str(indx)+' files parsed')
