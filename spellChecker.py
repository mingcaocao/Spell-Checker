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
            word_list.append(dic_word.lower())
        dic_word = f.readline().strip()
    f.close()
    return word_list
    
def getWordsWithSameStart(word, wordList, n):
    '''select the word(s) with at least the first n characters in same'''
    same_start = []
    for voc in wordList:
        same = True
        for i in range(0, n):
            if word[i] != voc[i]:
                same = False
        if same:
            same_start.append(voc)
    return same_start
    
def getWordsWithCommonLetters(word, wordList, n):
    '''obtain a list of words that have at least n distinct letters in common'''
    common_letter = []
    word_letter = []
    for letter in word:
        word_letter.append(letter)
    word_letter = set(word_letter)
    for voc in wordList:
        voc_letter = []
        for letter in voc:
            voc_letter.append(letter)
        voc_letter = set(voc_letter)
        same_letter = voc_letter.intersection(word_letter)
        if len(same_letter) >= n:
            common_letter.append(voc)
    return common_letter
    
def getSimilarityMetric(word1, word2):
    '''Calculate the similarity between the two words'''
    leftSimilarity = 0
    rightSimilarity = 0
    len1 = len(word1)
    len2 = len(word2)
    if len1 >= len2:
        length = len2
    else:
        length = len1
    for i in range(0, length):
        if word1[i] == word2[i]:
            leftSimilarity += 1
    reverse_word1 = word1[::-1]
    reverse_word2 = word2[::-1]
    for i in range(0, length):
        if reverse_word1[i] == reverse_word2[i]:
            rightSimilarity += 1
    return (leftSimilarity + rightSimilarity) / 2.0
    
def getSimilarityDict(word, wordList):
    '''give a dictionary of both word v.s. similarity '''
    sim_dic = {}
    for voc in wordList:
        sim_dic[voc] = getSimilarityMetric(word, voc)
    return sim_dic

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
    for voc in wordList:
        reverse_voc = voc[::-1]
        same = True
        for i in range(0, n):
            if reverse_word[i] != reverse_voc[i]:
                same = False
        if same:
            same_end.append(voc)
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
    '''Add index before each word'''
    i = 1
    for word in lst:
        print str(i) + '. ' + word
        i += 1

def main():
    f = open(fileName)
    g = open("correct.txt", "w")
    file_line = f.readline()
    while file_line:
        correct_word = ''
        line_word = file_line.split()
        for word in line_word:
            if findWordInDictionary(word, 'engDictionary.txt'):
                correct_word += word + ' '
            else:
                print "The word" + word + "is misspelled."
                suggestion_list = getCombinedWordSuggestions(word, 'engDictionary.txt')
                if suggestion_list != []:
                    print "Following suggestions are available:"                    
                    prettyPrint(suggestion_list)
                    user_choice = raw_input("Press 'r' for replace, 'a' for accept as is, 't' for type in manually.")
                    choice_right = False
                    while not choice_right:
                        if user_choice == 'r':
                            print "Your word will now be replaced with one of the suggestions."
                            print "Enter the number corresponding to the word that you want to use for replacement."
                            second_choice = input()
                            word = suggestion_list[second_choice - 1]
                            correct_word += word + ' '
                            choice_right = True
                        elif user_choice == 'a':
                            correct_word += word + ' ' 
                            choice_right = True
                        elif user_choice == 't':
                            print "Please type the word will be used as the replacement in the output file:"
                            word = raw_input()
                            correct_word += word + ' '
                            choice_right = True
                        else:
                            print "Please input right choice. Try again!"
                else:
                    print "There are 0 suggestions in our dictionary for this word."
                    user_choice = raw_input("Press 'a' for accept as is, 't' for type in manually.")                    
                    choice_right = False
                    while not choice_right:
                        if user_choice == 'a':
                            correct_word += word + ' '
                            choice_right = True
                        elif user_choice == 't':
                            print "Please type the word will be used as the replacement in the output file:"
                            word = raw_input()
                            correct_word += word + ' '
                            choice_right = True
                        else:
                            print "Please input right choice. Try again!"
        g.write(correct_word)
        g.write('\n')
                
                
                                    




            
