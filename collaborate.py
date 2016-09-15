
def ignoreCaseAndPunc(word):
    '''modify a word to be in lower case and all punctuation removed'''
    if '.' in word:
        word = word.strip('.')
    if ',' in word:
        word = word.strip(',')
    if ';' in word:
        word = word.strip(';')
    if ':' in word:
        word = word.strip(':')
    if '?' in word:
        word = word.strip('?')
        print word
    if '!' in word:
        word = word.strip('!')
    return word.lower()

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
        if len(dic_word) >= len(word)-n and len(dic_word) <= len(word)+n:
            word_list.append(dic_word.lower())
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
            ## ??? if word length < n, it was not counted
            if len(candidate) < n or word[i] != candidate.lower()[i]:
                sameChar = False
                break
        if sameChar == True:
            selected_word.append(candidate.lower())
    return selected_word

def getWordsWithCommonLetters(word, wordList, n):
    '''obtain a list of words that have at least n distinct letters in common'''
    charList1 = [] # store distinct characters in word
    selected_word = []
    word = ignoreCaseAndPunc(word) # pure word, no capitals
    for char in word:
        if char not in charList1:
            charList1.append(char)
    for candidate in wordList:
        candidate = candidate.lower() # all lower case
        if len(candidate) >= n:
            charList2 = [] # store distinct characters in candidate word
            for char in candidate:
                if char not in charList2:
                    charList2.append(char)
            sameChar = 0
            for char in charList1:
                if char in charList2:
                    sameChar += 1
            if sameChar >= n:
                selected_word.append(candidate)
    return selected_word

def getSimilarityMetric(word1, word2):
    '''compute left and right similarity of two words, and return the average.'''
    word1 = ignoreCaseAndPunc(word1)
    word2 = ignoreCaseAndPunc(word2)
    leftSimilarity = 0
    rightSimilarity = 0
    limit = min(len(word1), len(word2))
    for count in range(0, limit):
        if word1[count] == word2[count]:
            leftSimilarity += 1
    count = -1
    while count >= -limit:
        if word1[count] == word2[count]:
            rightSimilarity += 1
        count -= 1
    average = ( leftSimilarity + rightSimilarity ) / 2.0
    return average

def getSimilarityDict(word, wordList):
    '''create a dictionary for a list of words and their similarity metrics with a certain word'''
    dictionary = {}
    for element in wordList:
        dictionary[element] = getSimilarityMetric(word, element)
    return dictionary
