#!/usr/bin/python3

# Extracts title from all pdf files in current directory to a txt file
# Author: Cibin Joseph
# Use with python3

import os
import subprocess
import glob
from pdfrw import PdfReader
from warnings import warn
import argparse

def extract_raw_title(filename):
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
    except OSError:
        warnings.warn('Linux specific command not found. pdf to txt conversion not performed')
        first_line=''
    finally:
        try:
            os.remove('dummyfile.txt')
        except OSError:
            pass
    return first_line

def create_parser():
    parser=argparse.ArgumentParser(
            description=('Extracts title from pdf file'),
            epilog='Author: Cibin Joseph')
    parser.add_argument('filename',nargs='*',type=argparse.FileType('r'),default='.',help='Extracts title from file.pdf. Extracts from all pdf files in the current directory if a filename is not specified')
    parser.add_argument('-n','--name',help='Include filename in output',action='store_true')
    parser.add_argument('-s','--stat',help='Show statistics of files parsed',action='store_true')
    return parser

def extract_clean_title(filename):
    title=extract_raw_title(filename)
    from_txt=0
    if (title[0:4]=='none'):
        from_txt=1
    elif ('untitled' in title):
        from_txt=1
    elif ('replace with your title' in title):
        from_txt=1

    if (from_txt==1):
        # Better way - Convert to txt once, check each line for valid title
        title=extract_first_line(filename)

    return [title,from_txt]


# main
parser=create_parser()
args=parser.parse_args()

if (args.filename == '.'):
    # Get all filenames of current directory to a list
    filelist=sorted(glob.glob('*.pdf')+glob.glob('*.PDF'))
    num_pdf=0
    num_txt=0
    for filename in filelist:
        num_pdf=num_pdf+1
        [title,from_txt]=extract_clean_title(filename)
        if (from_txt==1):
            num_txt=num_txt+1
    if (args.name=='True'):
        print(filename+'  '+title+'\n')
    else:
        print(title+'\n')
else:
    num_pdf=1
    [title,from_txt]=extract_clean_title(args.filename)
    if (args.name=='True'):
        print(filename+'  '+title+'\n')
    else:
        print(title+'\n')
    if (from_txt==1):
        num_txt=1

if (args.stat=='True'):
    print(str(num_pdf)+' pdf files parsed')
    print(str(num_txt)+' titles extracted from pdf converted to txt')
