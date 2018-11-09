#!/usr/bin/python3

import unittest
import getpdftitle as gpdft

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


# So that unittest maybe run using python test_getpdftitle.py
# without invoking python -m unittest test_getpdftitle.py
if __name__=='__main__':
    unittest.main()
