import unittest
from functions import *


class MyTestCase(unittest.TestCase):
    def test_isDNA(self):
        self.assertTrue(isDNA('ATGCGTA'))
        self.assertFalse(isDNA('AUGCA'))

    def test_getRaw(self):
        test = 'A T G\n AT\tGATG'
        expected = 'ATGATGATG'
        result = getRaw(test)
        self.assertEqual(expected, result)

    def test_getComplement(self):
        test = 'ATGGTA'
        expected = 'TACCAT'
        result = getComplement(test)
        self.assertEqual(expected, result)

    def test_transcribe(self):
        test = 'ATGATG'
        expected = 'AUGAUG'
        result = transcribe(test)
        self.assertEqual(expected, result)

    def test_translate(self):
        test = 'AUGUGUUGA'
        expected = 'MC-'
        result = translate(test)
        self.assertEqual(expected, result)

    def test_getORFs(self):
        test = 'AUGGCAGGGUGAAACGCAGGUCGCCAGCGGCACCGCGCCUUUCGGCGGUGAAAUUAUCGAUGA\
GCGUGGUGGUUAUGCCGAUCGCGUCACACUACGUCUGAACGU'
        expected1 = orf()
        expected1.startPos, expected1.endPos = 0, 12
        expected2 = orf()
        expected2.startPos, expected2.endPos = 59, 101

        result = getORFs(test)
        self.assertEqual(2, len(result))
        self.assertEqual(expected1.startPos, result[0].startPos)
        self.assertEqual(expected1.endPos, result[0].endPos)
        self.assertEqual(expected2.startPos, result[1].startPos)
        self.assertEqual(expected2.endPos, result[1].endPos)

    def test_sortORFs(self):
        seq = 'AUGGCAGGGUGAAACGCAGGUCGCCAGCGGCACCGCGCCUUUCGGCGGUGAAAUUAUCGAUGA\
GCGUGGUGGUUAUGCCGAUCGCGUCACACUACGUCUGAACGU'
        test = getORFs(seq)
        test = sortORFs(test, len(test))
        firstLen = test[0].endPos - test[0].startPos
        secondLen = test[1].endPos - test[1].startPos
        self.assertTrue(firstLen > secondLen)

    def test_longestORF(self):
        test = 'ATGGCAGGGTGAAACGCAGGTCGCCAGCGGCACCGCGCCTTTCGGCGGTGAAATTATCGATGA\
GCGTGGTGGTTATGCCGATCGCGTCACACTACGTCTGAACGT'
        expected = 'MSVVVMPIASHYV-'
        result = longestORF(test)
        self.assertEqual(expected, result)

    def test_compRNA(self):
        test = 'ATGGACCAG'
        expected = 'CUGGUCCAU'
        result = compRNA(test)
        self.assertEqual(expected, result)

    def test_getProtein(self):
        seq = 'AUGGCAGGGUGAAACGCAGGUCGCCAGCGGCACCGCGCCUUUCGGCGGUGAAAUUAUCGAUGA\
GCGUGGUGGUUAUGCCGAUCGCGUCACACUACGUCUGAACGU'
        expected1 = 'MAG'
        result1 = getProtein(seq, 0, 9)
        self.assertEqual(expected1, result1)

        expected2 = 'GTV'
        result2 = getProtein(seq, 9, 0)
        self.assertEqual(expected2, result2)

    def test_getAllOrfs(self):
        seq = 'ATGGCAGGGTGAAACGCAGGTCGCCAGCGGCACCGCGCCTTTCGGCGGTGAAATTATCGATGA\
GCGTGGTGGTTATGCCGATCGCGTCACACTACGTCTGAACCCAT'
        expected1 = orf()
        expected1.startPos = 59
        expected1.endPos = 101

        expected2 = orf()
        expected2.startPos = 107
        expected2.endPos = 86

        expected3 = orf()
        expected3.startPos = 0
        expected3.endPos = 12

        result = getAllOrfs(seq)

        expectedList = [expected1, expected2, expected3]
        for x in range(len(result)):
            self.assertEqual(expectedList[x].startPos, result[x].startPos)
            self.assertEqual(expectedList[x].endPos, result[x].endPos)


if __name__ == '__main__':
    unittest.main()
