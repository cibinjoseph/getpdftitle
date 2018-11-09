import unittest
import getpdftitle as gpdft

class TestCode(unittest.TestCase):

    def setUp(self):


    def test_get_raw_title(self):
        title = gpdft.get_raw_title(self.samplefile1)
        self.assertEqual(title,'None')


if __name__=='__main__':
    unittest.main()
