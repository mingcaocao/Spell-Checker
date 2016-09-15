
def ignoreCaseAndPunc(word):
    '''modify a word to be in lower case and all punctuation removed'''
    word = word.lower()
    word = word.strip(",.;:?!")
    return word
    
def findWordInDictionary(word, fileName):
    '''check if the provided word is in the dictionary file'''
    f = open(fileName)
    dic_word = f.readline().strip()
    word = ignoreCaseAndPunc(word)
    while dic_word:
        if word == dic_word.lower():
            return True
        else:
            dic_word = f.readline().strip()
    f.close()
    return False
        
def getWordsOfSimLength(word, fileName, n):
    '''select alternate words that have required length from dictionary'''
    f = open(fileName)
    dic_word = f.readline().strip()
    word = ignoreCaseAndPunc(word)
    word_list = []
    while dic_word:
        if len(dic_word) >= len(word) - n and len(dic_word) <= len(word) + n:
            word_list.append(dic_word)
        dic_word = f.readline().strip()
    f.close()
    return word_list
    
def getWordsWithSameStart(word, wordList, n):
    '''select the word(s) with at least the first n characters in same'''
    selected_word = []
    word = ignoreCaseAndPunc(word)
    for candidate in wordList:
        sameChar = True
        for i in range(0,n):
            # if word length < n, it is not considered to be a qualified one
            if len(candidate) < n or word[i] != candidate.lower()[i]:
                sameChar = False
                break
        if sameChar:
            selected_word.append(candidate)
    return selected_word
    
def getWordsWithCommonLetters(word, wordList, n):
    '''obtain a list of words that have at least n distinct letters in common'''
    common_letter = []
    word_letter = []
    word = ignoreCaseAndPunc(word) # all lower letters
    for letter in word:
        word_letter.append(letter)
    word_letter = set(word_letter) # number of distinct letters in word
    for candidate in wordList:
        candidate_letter = []
        for letter in candidate:
            candidate_letter.append(letter.lower()) # all lower letters
        candidate_letter = set(candidate_letter) # number of distinct letters in candidate
        same_letter = candidate_letter.intersection(word_letter)
        if len(same_letter) >= n:
            common_letter.append(candidate)
    return common_letter
    
def getSimilarityMetric(word1, word2):
    '''Calculate the similarity between the two words'''
    word1 = ignoreCaseAndPunc(word1)
    word2 = ignoreCaseAndPunc(word2)
    leftSimilarity = 0
    rightSimilarity = 0
    length = min(len(word1), len(word2))
    for count in range(0, length):
        if word1[count] == word2[count]:
            leftSimilarity += 1
    reverse_word1 = word1[::-1]
    reverse_word2 = word2[::-1]
    for count in range(0, length):
        if reverse_word1[count] == reverse_word2[count]:
            rightSimilarity += 1
    return (leftSimilarity + rightSimilarity) / 2.0
    
def getSimilarityDict(word, wordList):
    '''give a dictionary of both word v.s. similarity '''
    similarity_dic = {}
    for element in wordList:
        similarity_dic[element] = getSimilarityMetric(word, element)
    return similarity_dic

def sortIn2D(tup1, tup2):
    '''sorting help function'''
    if tup1[-1] < tup2[-1]:
        return -1
    elif tup1[-1] == tup2[-1]:
        return 0
    return 1

def getListOfFirstComponents(tupleList):
    '''Give a list containing first component from each tuple'''
    new_list = []
    for tup in tupleList:
        new_list.append(tup[0])
    return new_list

def getBestWords(similarityDictionary, n):
    '''Sort the dictionary by similarity'''
    listOfTuples = similarityDictionary.items()
    listOfTuples.sort(sortIn2D, reverse=True)
    return getListOfFirstComponents(listOfTuples)[0:n]

def getWordsOfCommonPercent(word, wordList, commonPercent):
    '''Give a list of words with common letters above the commonPercent'''
    word_letter = []
    for letter in word:
        word_letter.append(letter)
    word_letter = set(word_letter)
    letter_number = len(word_letter)
    n = letter_number * commonPercent / 100.0
    if n % 1 != 0:
        n = int(n) + 1
    n = int(n)
    return getWordsWithCommonLetters(word, wordList, n)
        
def getWordSuggestionsV1(word, fileName, n, commonPercent, topN):
    '''Give a list where word has fixable length range and similarity'''
    word_list = getWordsOfSimLength(word, fileName, n)
    word_list = getWordsOfCommonPercent(word, word_list, commonPercent)
    similarityDictionary = getSimilarityDict(word, word_list)
    return getBestWords(similarityDictionary, topN)

def getWordsWithSameEnd(word, wordList, n):
    '''Give a list with n same characters from the end'''
    same_end = []
    reverse_word = word[::-1]
    for candidate in wordList:
        reverse_candidate = candidate[::-1]
        same_letter = True
        for i in range(0, n):
            if reverse_word.lower()[i] != reverse_candidate.lower()[i]:
                same_letter = False
        if same_letter:
            same_end.append(candidate)
    return same_end

def getWordSuggestionsV2(word, fileName, n, topN):
    '''Get a word list with fixed length range and same start and end'''
    word_list = getWordsOfSimLength(word, fileName, 1)
    word_list = getWordsWithSameStart(word, word_list, n)
    word_list = getWordsWithSameEnd(word, word_list, n)
    similarityDictionary = getSimilarityDict(word, word_list)
    return getBestWords(similarityDictionary, topN)

def getCombinedWordSuggestions(word, fileName):
    '''Combine V1 and V2 list to get the final list'''
    lst1 = set(getWordSuggestionsV1(word, fileName, 2, 75, 7))
    lst2 = set(getWordSuggestionsV2(word, fileName, 1, 7))
    word_list = lst1.union(lst2)
    similarityDictionary = getSimilarityDict(word, word_list)
    if len(similarityDictionary) <= 10:
        return getBestWords(similarityDictionary, len(similarityDictionary))
    return getBestWords(similarityDictionary, 10)

def prettyPrint(lst):
    '''Add index before each word and print them out'''
    number = 1
    for word in lst:
        print str(number) + '. ' + word
        number += 1


def replaceWordWithTopSuggestion(readFileName, writeFileName, dictionaryName):
    '''produce a new file in which each incorrect word is replaced
       by the first word in suggestion list.'''
    f = open(readFileName)
    line = f.readline()
    f_write = open(writeFileName, 'w')
    while line:
        wordList = line.strip('\n').split()
        for word in wordList:
            if (not findWordInDictionary(word, dictionaryName)
                and len(getCombinedWordSuggestions(word, dictionaryName)) >= 1):
                new_word = getCombinedWordSuggestions(word, dictionaryName)[0]
                f_write.write(new_word + ' ')
            else:
                f_write.write(word + ' ')
        f_write.write('\n')
        line = f.readline()
    f_write.close()
    f.close()

def main():
    f_read = open('Jabberwocky.txt')
    f_write = open('newJabberwocky.txt', 'w')
    file_line = f_read.readline()
    while file_line:
        line_word = file_line.strip('\n').split()
        line_to_write = ''
        for word in line_word:
            if findWordInDictionary(word, 'engDictionary.txt'):
                line_to_write += word + ' '
            else:
                print "The word " + word + " is misspelled."
                suggestion_list = getCombinedWordSuggestions(
                                    word, 'engDictionary.txt')
                if suggestion_list != []:
                    print 'The following suggestions are available'
                    prettyPrint(suggestion_list)
                    choice_right = False
                    while not choice_right:
                        user_choice = raw_input("Press 'r' for replace, 'a' for " +
                                "accept as is, 't' for type in manually.\n")
                        if user_choice == 'r':
                            print ('Your word will now be replaced with one ' +
                                   'of the suggestions')
                            second_choice = input('Enter the number corresponding ' +
                                            'to the word that you want to use for ' +
                                            'replacement.\n')
                            new_word = suggestion_list[second_choice - 1]
                            line_to_write += new_word + ' '
                            choice_right = True
                        elif user_choice == 'a':
                            line_to_write += word + ' '
                            choice_right = True
                        elif user_choice == 't':
                            new_word = raw_input('Please type the word that will ' +
                                                 'be used as the replacement in '+
                                                 'the output file\n')
                            line_to_write += new_word + ' '
                            choice_right = True
                        else:
                            print "Please input right choice. Try again!\n"
                            
                else:
                    print 'There are 0 suggestions in our dictionary for this word.'
                    choice_right = False
                    while not choice_right:
                        user_choice = raw_input("Press 'r' for replace, 'a' for " +
                                "accept as is, 't' for type in manually.\n")
                        if user_choice == 'a':
                            line_to_write += word + ' '
                            choice_right = True
                        elif user_choice == 't':
                            new_word = raw_input('Please type the word that will ' +
                                                 'be used as the replacement in '+
                                                 'the output file\n')
                            line_to_write += new_word + ' '
                            choice_right = True
                        else:
                            print "Please input right choice. Try again!\n"    
    
        line_to_write += '\n'
        f_write.write(line_to_write)
        file_line = f_read.readline()
    f_read.close()
    f_write.close()


if __name__ == '__main__':
    main()

            




            
