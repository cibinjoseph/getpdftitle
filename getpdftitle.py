#!/usr/bin/python3

# Extracts title from pdf
# Author: Cibin Joseph

import os
import sys
import subprocess
import glob
try:
    import argparse
except ImportError:
    print('ERROR: Ensure python module argparse is installed')
    exit(-1)
try:
    from pdfrw import PdfReader
except ImportError:
    print('ERROR: Ensure python module pdfrw is installed')
    exit(-1)


def get_raw_title(filename):
    'Extracts title from a given pdf file'
    try:
        reader = PdfReader(filename)

        # Extract title from file
        title = reader.Info.Title
        title = str(title)

        # replace unnecessary () in title
        title = title.replace('(', ' ')
        title = title.replace(')', ' ')
    except FileNotFoundError:
        print('ERROR: File does not exist or is not readable')
        title = ''

    return title


def get_first_line(filename):
    'Extracts first line from pdf converted to txt file'

    try:
        # Create dummyfile.txt
        dummyfile = open('dummyfile.txt', 'w+')
        dummyfile.close()
        # Convert pdf to text using linux command pdftotext
        proc_convert = subprocess.Popen(
                ['pdftotext', '-f', '1', '-l', '1', filename, 'dummyfile.txt'])
        # Wait for conversion process to complete
        while proc_convert.poll() is None:
            pass
        # Get first non-empty line from txt file
        first_line = ''
        with open('dummyfile.txt') as dummyfile:
            for i, line in enumerate(dummyfile):
                if (line.strip() != ''):
                    first_line = line.strip('\n').strip()
                    break
    except OSError:
        print('WARNING: Unix command pdftotext not found. pdf not converted to txt')
        first_line = ''

    try:
        os.remove('dummyfile.txt')
    except OSError:
        pass
    return first_line


def init_parser():
    'Initializes the argument parser'
    parser = argparse.ArgumentParser(
            description=('Extracts title from pdf file'),
            epilog='Author: Cibin Joseph')
    parser.add_argument(
            'filename', nargs='*', default='.',
            help='Extracts title from file.pdf.\
            Extracts from all pdf files in current directory\
            if a filename is not specified')
    parser.add_argument(
            '-n', '--name', action='store_true',
            help='Include filename in output')
    parser.add_argument(
            '-s', '--stat', action='store_true',
            help='Show statistics of files parsed')
    return parser


def get_clean_title(filename):
    title = get_raw_title(filename)
    wordlist_replace = ['none', 'None', 'untitled',
                        'replace with your title', 'pdf', 'PDF']
    from_txt = False
    for word in wordlist_replace:
        if (word in title):
            from_txt = True

    if (from_txt is True):
        # Better way - Convert to txt once,  check each line for valid title
        title = get_first_line(filename)

    return [title, from_txt]


# main
parser = init_parser()
args = parser.parse_args()

if (args.filename == '.'):
    # Get all filenames of current directory to a list
    filelist = sorted(glob.glob('*.pdf')+glob.glob('*.PDF'))
    num_pdf = 0
    num_txt = 0
    for filename in filelist:
        num_pdf = num_pdf+1
        [title, from_txt] = get_clean_title(filename)
        if (from_txt is True):
            num_txt = num_txt+1
        if (args.name is True):
            print(filename+'  '+title)
        else:
            print(title)
else:
    num_pdf = 1
    num_txt = 0
    [title, from_txt] = get_clean_title(str(args.filename[0]))
    if (args.name is True):
        print(filename+'  '+title)
    else:
        print(title)
    if (from_txt is True):
        num_txt = 1

if (args.stat is True):
    print('\n'+str(num_pdf)+' pdf files parsed')
    print(str(num_txt)+' titles extracted from pdf converted to txt')
