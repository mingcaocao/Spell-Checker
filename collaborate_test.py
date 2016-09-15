from spellChecker import *
import unittest

class Testcollaborate(unittest.TestCase):


    def test_ignoreCaseAndPunc(self):
        self.assertEqual('actually', ignoreCaseAndPunc('Actually,'))
        self.assertEqual('variables', ignoreCaseAndPunc('variables.'))
        self.assertNotEqual('coexit', ignoreCaseAndPunc('co-exit'))
    
    def test_findWordInDictionary(self):
        self.assertTrue(findWordInDictionary("atm's",'engDictionary.txt'))
        self.assertFalse(findWordInDictionary('abandom','engDictionary.txt'))
        self.assertTrue(findWordInDictionary('jet','engDictionary.txt'))

    def test_getWordsOfSimLength(self):
        self.assertEqual(4, len(getWordsOfSimLength('ging','oed.txt',1)))
        self.assertEqual(set(['ban','bang','gang','mange']),
                         set(getWordsOfSimLength('ging','oed.txt',1)))

    def test_getWordsWithSameStart(self):
        wordlist = ['ban','bang','gang','aa','mange']
        self.assertEqual(['gang'],getWordsWithSameStart('ging',wordlist,1))
        self.assertEqual(2,len(getWordsWithSameStart('band',wordlist,2)))
        self.assertTrue('ban' in getWordsWithSameStart('band',wordlist,2))
        self.assertTrue('bang' in getWordsWithSameStart('band',wordlist,2))

    def test_getWordsWithCommonLetters(self):
        wordlist = ['ban','bang','gang','aa','mange']
        self.assertEqual(['mange'],getWordsWithCommonLetters('immediate',wordlist,3))
        self.assertTrue('bang' in getWordsWithCommonLetters('clang',wordlist,3))
        self.assertTrue('gang' in getWordsWithCommonLetters('clang',wordlist,3))
        self.assertTrue('mange' in getWordsWithCommonLetters('clang',wordlist,3))
        self.assertFalse('aa' in getWordsWithCommonLetters('clang',wordlist,3))

    def test_getSimilarityMetric(self):
        self.assertEqual(2.5, getSimilarityMetric('oblige', 'oblivion'))
        self.assertEqual(1.5, getSimilarityMetric('aghast', 'gross'))

    def test_getSimilarityDict(self):
        wordlist = ['ban','bang','gang','aa','mange']
        self.assertEqual(1.5, getSimilarityDict('band',wordlist)['ban'])
        self.assertEqual(3.0, getSimilarityDict('band',wordlist)['bang'])
        self.assertEqual(2.0, getSimilarityDict('band',wordlist)['gang'])
        self.assertEqual(0.5, getSimilarityDict('band',wordlist)['aa'])
        self.assertEqual(1.0, getSimilarityDict('band',wordlist)['mange'])

unittest.main()
