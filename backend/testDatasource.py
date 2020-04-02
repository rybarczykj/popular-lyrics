import unittest
from datasource import *

class DataSourceTester(unittest.TestCase):

    def test_yearInvalidType(self):
        DS = DataSource()
        with self.assertRaises(TypeError):
            DS.getWordInstancesInYear("hello", "two hundred B.C.")

    def test_wordInvalidType(self):
        DS = DataSource()
        with self.assertRaises(TypeError):
            DS.getWordInstancesInYear(911, 1980)

    def test_wordContainsInvalidChars(self):
        DS = DataSource()
        with self.assertRaises(ValueError):
            DS.getWordInstancesInYear("can't", 1980)

    def test_yearAboveRange(self):
        DS = DataSource()
        with self.assertRaises(ValueError):
            DS.getWordInstancesInYear("hello", 2090)

    def test_yearBelowRange(self):
        DS = DataSource()
        with self.assertRaises(ValueError):
            DS.getWordInstancesInYear("hello", 1890)

    def test_wordIsNeverUsed(self):
        DS = DataSource()
        output = DS.getWordInstancesInYear("akjsdaksjd", 1980)
        self.assertEqual(output, 0)

    def test_validInputs(self):
            DS = DataSource()
            for i in DS.getWordInstancesInYear("wooly", 1965):
                output = int(i)
            self.assertEqual(output, 18)

if __name__ =='__main__':
    unittest.main()