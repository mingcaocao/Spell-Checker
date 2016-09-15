from spellChecker_co import *
import unittest

class TestSpellChecker(unittest.TestCase):

    def test_ignoreCaseAndPunc(self):
        self.assertEqual('actually', ignoreCaseAndPunc('Actually,'))
        self.assertEqual('actually', ignoreCaseAndPunc('Actually?'))
        self.assertEqual('actually', ignoreCaseAndPunc('Actually!'))
        self.assertEqual('actually', ignoreCaseAndPunc('Actually:'))
        self.assertEqual('actually', ignoreCaseAndPunc('Actually;'))
        self.assertEqual('variables', ignoreCaseAndPunc('variables.'))
        self.assertNotEqual('coexit', ignoreCaseAndPunc('co-exit'))
    
    def test_findWordInDictionary(self):
        self.assertTrue(findWordInDictionary("atm's",'engDictionary.txt'))
        self.assertFalse(findWordInDictionary('abandom','engDictionary.txt'))
        self.assertTrue(findWordInDictionary('Jet','engDictionary.txt'))

    def test_getWordsOfSimLength(self):
        self.assertEqual(4, len(getWordsOfSimLength('ging','oed.txt',1)))
        self.assertEqual(set(['ban','bang','gang','mange']),
                         set(getWordsOfSimLength('ging','oed.txt',1)))
        self.assertFalse('aa' in getWordsOfSimLength('ging','oed.txt',1))

    def test_getWordsWithSameStart(self):
        wordlist = ['Ban','bang','gang','ba','mange']
        self.assertEqual(['gang'],getWordsWithSameStart('ging',wordlist,1))
        self.assertEqual(2,len(getWordsWithSameStart('band',wordlist,3)))
        self.assertTrue('Ban' in getWordsWithSameStart('band',wordlist,2))
        self.assertTrue('bang' in getWordsWithSameStart('band',wordlist,2))
        self.assertFalse('ba' in getWordsWithSameStart('band',wordlist,3))

    def test_getWordsWithCommonLetters(self):
        wordlist = ['ban','Bang','gang','aa','mange']
        self.assertEqual(['mange'],getWordsWithCommonLetters('immediate',wordlist,3))
        self.assertTrue('Bang' in getWordsWithCommonLetters('clang',wordlist,3))
        self.assertTrue('gang' in getWordsWithCommonLetters('clang',wordlist,3))
        self.assertTrue('mange' in getWordsWithCommonLetters('clang',wordlist,3))
        self.assertFalse('aa' in getWordsWithCommonLetters('alang',wordlist,2))

    def test_getSimilarityMetric(self):
        self.assertEqual(2.5, getSimilarityMetric('oblige', 'oblivion'))
        self.assertEqual(1.5, getSimilarityMetric('aghast', 'gross'))

    def test_getSimilarityDict(self):
        wordlist = ['ban','bang','gang','aa','mange']
        self.assertEqual(5, len(getSimilarityDict('band',wordlist)))
        self.assertEqual(1.5, getSimilarityDict('band',wordlist)['ban'])
        self.assertEqual(3.0, getSimilarityDict('band',wordlist)['bang'])
        self.assertEqual(2.0, getSimilarityDict('band',wordlist)['gang'])
        self.assertEqual(0.5, getSimilarityDict('band',wordlist)['aa'])
        self.assertEqual(1.0, getSimilarityDict('band',wordlist)['mange'])


    def test_sortIn2D(self):
        tup1 = (1.0,3.0)
        tup2 = (2.5,3.0)
        tup3 = (1,2)
        tup4 = (5,4.2)
        self.assertEqual(0, sortIn2D(tup1, tup2))
        self.assertTrue(sortIn2D(tup1, tup3) == 1)
        self.assertFalse(sortIn2D(tup3,tup1) == 1)
        self.assertEqual(-1, sortIn2D(tup1, tup4))

    def test_getListOfFirstComponents(self):
        tupleList = [(1,5),(4,3),(20,7)]
        self.assertTrue(1 in getListOfFirstComponents(tupleList))
        self.assertTrue(4 in getListOfFirstComponents(tupleList))
        self.assertTrue(20 in getListOfFirstComponents(tupleList))
        self.assertFalse(5 in getListOfFirstComponents(tupleList))
        self.assertFalse(3 in getListOfFirstComponents(tupleList))
        self.assertFalse(7 in getListOfFirstComponents(tupleList))
        self.assertEqual(3, len(getListOfFirstComponents(tupleList)))

    def test_getBestWords(self):
        wordList = ['ban','bang','gang','aa','mange']
        similarityDict = getSimilarityDict('band', wordList)
        self.assertEqual(['bang'], getBestWords(similarityDict, 1))
        self.assertTrue('gang' in getBestWords(similarityDict, 2))
        self.assertFalse('aa' in getBestWords(similarityDict, 2))

    def test_getWordsOfCommonPercent(self):
        wordList = ['a','ab','abc','abcd','abcde','abcdef']
        self.assertEqual(3, len(getWordsOfCommonPercent('abcdefgh',wordList,50)))
        self.assertTrue('abcd' in getWordsOfCommonPercent('abcdefgh',wordList,50))
        self.assertTrue('abcde' in getWordsOfCommonPercent('abcdefgh',wordList,50))
        self.assertTrue('abcdef' in getWordsOfCommonPercent('abcdefgh',wordList,50))
        self.assertFalse('abc' in getWordsOfCommonPercent('abcdefgh',wordList,50))
        self.assertFalse('abcd' in getWordsOfCommonPercent('abcdefgh',wordList,60))

    def test_getWordSuggestionsV1(self):
        self.assertTrue('bang' in getWordSuggestionsV1('cang','oed.txt',1,55,2))
        self.assertTrue('gang' in getWordSuggestionsV1('cang','oed.txt',1,55,2))
        self.assertFalse('mange' in getWordSuggestionsV1('cang','oed.txt',1,55,2))

    def test_getWordsWithSameEnd(self):
        word = 'sheep'
        wordList = ['sleep','feet','sharp','sheer']
        self.assertTrue('sleep' in getWordsWithSameEnd(word, wordList, 3))
        self.assertFalse('sleep' in getWordsWithSameEnd(word, wordList, 4))
        self.assertFalse('sheer' in getWordsWithSameEnd(word, wordList, 1))

    def test_getWordSuggestionsV2(self):
        self.assertFalse('bigger' in getWordSuggestionsV2('biger','engDictionary.txt',2,2))
        self.assertTrue('biker' in getWordSuggestionsV2('biker','engDictionary.txt',2,2))
        self.assertTrue('bider' in getWordSuggestionsV2('biker','engDictionary.txt',2,2))        

    def test_getCombinedWordSuggestions(self):
        self.assertFalse('hall' in getCombinedWordSuggestions('paul','engDictionary.txt'))
        self.assertTrue('haul' in getCombinedWordSuggestions('paul','engDictionary.txt'))
        self.assertTrue('pail' in getCombinedWordSuggestions('paul','engDictionary.txt'))
        self.assertFalse('alum' in getCombinedWordSuggestions('paul','engDictionary.txt'))
        self.assertFalse('plate' in getCombinedWordSuggestions('paul','engDictionary.txt'))
        self.assertTrue('palm' in getCombinedWordSuggestions('paul','engDictionary.txt'))


        
unittest.main()
