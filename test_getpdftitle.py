#!/usr/bin/python3

import unittest
import subprocess
import getpdftitle as gpdft
import glob


class TestCode(unittest.TestCase):

    def setUp(self):
        self.samplefile1 = 'sample1.pdf'
        self.samplefile2 = 'sample2.pdf'

    def test_get_raw_title(self):
        # Empty metadata
        title = gpdft.get_raw_title(self.samplefile1)
        self.assertEqual(title, 'None')

        # Non-empty metadata
        title = gpdft.get_raw_title(self.samplefile2)
        self.assertEqual(title, 'A Random Document')

    def test_get_clean_title(self):
        # Empty metadata
        [title, from_txt] = gpdft.get_clean_title(self.samplefile1)
        self.assertEqual(title, 'A Simple PDF File')
        self.assertEqual(from_txt, True)

    def test_script(self):
        # Single sample file
        p = subprocess.Popen(['python3', 'getpdftitle.py', 'sample1.pdf'],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.stdout.read().decode('utf-8'),
                         'A Simple PDF File\n')
        p.stdout.close()

        # Multiple sample files
        p = subprocess.Popen(['python3', 'getpdftitle.py',
                             'sample1.pdf', 'sample2.pdf'],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.stdout.read().decode('utf-8'),
                         'A Simple PDF File\nA Random Document\n')
        p.stdout.close()

        # Whole directory
        p = subprocess.Popen(['python3', 'getpdftitle.py'],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        len_output = len(p.stdout.read().decode('utf-8').split('\n')) - 1 
        num_pdf_files = len(glob.glob('*.pdf')+glob.glob('*.PDF'))
        self.assertTrue(len_output == num_pdf_files)
        p.stdout.close()

        # Non-existent file
        p = subprocess.Popen(['python3', 'getpdftitle.py', 'NOPENOPE.pdf'],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertRaises(FileNotFoundError)
        p.stdout.close()



# So that unittest maybe run using python test_getpdftitle.py
# without invoking python -m unittest test_getpdftitle.py
if __name__ == '__main__':
    unittest.main()
