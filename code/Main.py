import string
import numpy as np
import random
import math

table = str.maketrans({key: None for key in string.punctuation})

inputHamiltonTraining = [1, 6, 7, 8, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29]
inputMadisonTraining = [10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
inputFileTestHamilton = [9, 11, 12]
inputFileTestMadison = [47, 48, 58]

uniHamilton = {}
smoothUniHamilton = {}
uniProbabilityHamilton = {}
biHamilton = {}
smoothBiHamilton = {}
biProbabilityHamilton = {}
triHamilton = {}
smoothTriHamilton = {}
triProbabilityHamilton = {}

uniMadison = {}
smoothUniMadison = {}
uniProbabilityMadison = {}
biMadison = {}
smoothBiMadison = {}
biProbabilityMadison = {}
triMadison = {}
smoothTriMadison = {}
triProbabilityMadison = {}


def readFile(fileNumber):
    fileName = str(fileNumber) + ".txt"
    return fileName

def operateTestFile(fileName):
    file = open(fileName, "r")
    lineCounter = 0
    for lineCount in file:
        lineCounter = lineCounter + 1

    file = open(fileName, "r")
    authorName = file.readline()

    for index in range(1, lineCounter):
        ### remove puctuations from data and convert to lowercase ###
        line = file.readline().lower()

        essayProbabilityHamilton = 0.0
        essayProbabilityMadison = 0.0

        essayProbabilityTrigramHamilton = 0.0
        essayProbabilityTrigramMadison = 0.0

        # essayProbabilityBigramHamiltonForPerplexity = 1.0
        # essayProbabilityBigramMadisonForPerplexity = 1.0
        # essayProbabilityTrigramHamiltonForPerplexity = 1.0
        # essayProbabilityTrigramMadisonForPerplexity = 1.0

        perplexityBiHamilton = 0
        perplexityBiMadison = 0
        perplexityTriHamilton = 0
        perplexityTriMadison = 0

        totalWordNumberInTest = 0


        sentenceSplittedForBla = line.split('.')
        for sentencesSplittedForExclamationMark in sentenceSplittedForBla:
            sentencesSplittedForExclamationMarkArray = sentencesSplittedForExclamationMark.split('!')
            for sentences in sentencesSplittedForExclamationMarkArray:
                sentencesArray = sentences.split('?')
                while sentencesArray.count(' \n') > 0:
                    sentencesArray.remove(' \n')

                for sentence in sentencesArray:
                    senteceProbabilityHamilton = 0.0
                    senteceProbabilityMadison = 0.0

                    senteceProbabilityTrigramHamilton = 0.0
                    senteceProbabilityTrigramMadison = 0.0
                    if sentence == ' ':
                        continue
                    else:
                        sentence = sentence.translate(table)
                        sentence = sentence + " </s> </s> "

                        words = sentence.split()
                        words.insert(0, '<s>')
                        words.insert(0, '<s>')

                        ### Creating bigram probability ###
                        for i in range(1, len(words) - 2):
                            totalWordNumberInTest += 1
                            ###  Hamilton  ###
                            if words[i] + ' ' + words[i + 1] in biHamilton.keys():
                                biProbabilityHamilton = (biHamilton[words[i] + ' ' + words[i + 1]] + 1) / (uniHamilton[words[i]] + len(uniHamilton.keys()))
                            else:
                                if words[i] in uniHamilton.keys():
                                    biProbabilityHamilton = 1 / (uniHamilton[words[i]] + len(uniHamilton.keys()))
                                else:
                                    biProbabilityHamilton = 1 / len(uniHamilton.keys())
                            senteceProbabilityHamilton = senteceProbabilityHamilton + math.log10(biProbabilityHamilton)
                            # essayProbabilityBigramHamiltonForPerplexity = essayProbabilityBigramHamiltonForPerplexity * biProbabilityHamilton

                            ###  Madison  ###
                            if words[i] + ' ' + words[i + 1] in biMadison.keys():
                                biProbabilityMadison = (biMadison[words[i] + ' ' + words[i + 1]] + 1) / (uniMadison[words[i]] + len(uniMadison.keys()))
                            else:
                                if words[i] in uniMadison.keys():
                                    biProbabilityMadison = 1 / (uniMadison[words[i]] + len(uniMadison.keys()))
                                else:
                                    biProbabilityMadison = 1 / len(uniMadison.keys())
                            senteceProbabilityMadison = senteceProbabilityMadison + math.log10(biProbabilityMadison)
                            # essayProbabilityBigramMadisonForPerplexity = essayProbabilityBigramMadisonForPerplexity * biProbabilityMadison

                        essayProbabilityHamilton = essayProbabilityHamilton + senteceProbabilityHamilton
                        essayProbabilityMadison = essayProbabilityMadison + senteceProbabilityMadison

        # print(essayProbabilityHamilton)
        # print(essayProbabilityMadison)

                        ### Creating bigram probability ###

                        ### Creating trigram probability ###
                        cont1 = False
                        cont2 = False
                        for i in range(2, len(words)):
                            if cont1:
                                cont1 = False
                                continue
                            if cont2:
                                cont2 = False
                                continue

                            ###  Hamilton  ###
                            if words[i - 2] + ' ' + words[i - 1] + ' ' + words[i] in triHamilton.keys():
                                if words[i - 2] + ' ' + words[i - 1] == '<s> <s>':
                                    triProbabilityHamilton = (triHamilton[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] + 1) / len(biHamilton)
                                else:
                                    triProbabilityHamilton = (triHamilton[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] + 1) / (biHamilton[words[i - 2] + ' ' + words[i - 1]] + len(biHamilton))
                            else:
                                if (words[i - 2] + ' ' + words[i - 1] in biHamilton.keys()) and (words[i - 2] + ' ' + words[i - 1] != '<s> <s>'):
                                    triProbabilityHamilton = 1 / (biHamilton[words[i - 2] + ' ' + words[i - 1]] + len(biHamilton))
                                else:
                                    triProbabilityHamilton = 1 / len(biHamilton)
                            senteceProbabilityTrigramHamilton = senteceProbabilityTrigramHamilton + math.log10(triProbabilityHamilton)
                            # essayProbabilityTrigramHamiltonForPerplexity = essayProbabilityTrigramHamiltonForPerplexity * triProbabilityHamilton


                            ###  Madison  ###
                            if words[i - 2] + ' ' + words[i - 1] + ' ' + words[i] in triMadison.keys():
                                if words[i - 2] + ' ' + words[i - 1] == '<s> <s>':
                                    triProbabilityMadison = (triMadison[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] + 1) / len(biMadison)
                                else:
                                    triProbabilityMadison = (triMadison[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] + 1) / (biMadison[words[i - 2] + ' ' + words[i - 1]] + len(biMadison))
                            else:
                                if (words[i - 2] + ' ' + words[i - 1] in biMadison.keys()) and (words[i - 2] + ' ' + words[i - 1] != '<s> <s>'):
                                    triProbabilityMadison = 1 / (biMadison[words[i - 2] + ' ' + words[i - 1]] + len(biMadison))
                                else:
                                    triProbabilityMadison = 1 / len(biMadison)
                            senteceProbabilityTrigramMadison = senteceProbabilityTrigramHamilton + math.log10(triProbabilityMadison)
                            # essayProbabilityTrigramMadisonForPerplexity = essayProbabilityTrigramMadisonForPerplexity * triProbabilityMadison

                            if (words[i].count('</s>') > 0) and i + 1 != len(words):
                                cont1 = True
                                cont2 = True

                        essayProbabilityTrigramHamilton = essayProbabilityTrigramHamilton + senteceProbabilityTrigramHamilton
                        essayProbabilityTrigramMadison = essayProbabilityTrigramMadison + senteceProbabilityTrigramMadison
        # print(str(essayProbabilityTrigramHamilton) + " " + fileName)
        # print(str(essayProbabilityTrigramMadison) + " " + fileName)

        perplexityBiHamilton = 10 ** (essayProbabilityHamilton * (-1 / totalWordNumberInTest))
        perplexityBiMadison = 10 ** (essayProbabilityMadison * (-1 / totalWordNumberInTest))

        print("perplexityBiHamilton "+str(perplexityBiHamilton))
        print("perplexityBiMadison "+str(perplexityBiMadison))

        perplexityTriHamilton = 10 ** (essayProbabilityTrigramHamilton * (-1 / totalWordNumberInTest))
        perplexityTriMadison = 10 ** (essayProbabilityTrigramMadison * (-1 / totalWordNumberInTest))

        print("perplexityTriHamilton "+str(perplexityTriHamilton))
        print("perplexityTriMadison "+ str(perplexityTriMadison))

### Creating trigram probability ###




def operateFile(fileName):

    file = open(fileName, "r")
    lineCounter = 0
    for lineCount in file:
        lineCounter = lineCounter + 1

    file = open(fileName, "r")
    authorName = file.readline()

    #print("Author Name is " + authorName)

    isAuthorHamilton = False
    if authorName.count('HAMILTON') == 1:
        isAuthorHamilton = True

    for index in range(1, lineCounter):

        ### remove puctuations from data and convert to lowercase ###
        line = file.readline().lower()
        sentenceSplittedForBla = line.split('.')
        for sentencesSplittedForExclamationMark in sentenceSplittedForBla:
            sentencesSplittedForExclamationMarkArray = sentencesSplittedForExclamationMark.split('!')
            for sentences in sentencesSplittedForExclamationMarkArray:
                sentencesArray = sentences.split('?')
                while sentencesArray.count(' \n') > 0:
                    sentencesArray.remove(' \n')

                for sentence in sentencesArray:
                    if sentence == ' ':
                        continue
                    else:
                        sentence = sentence.translate(table)
                        sentence = sentence + " </s> </s> "

                        words = sentence.split()
                        words.insert(0, '<s>')
                        words.insert(0, '<s>')


                        ### Creating unigram dictionary ###
                        for word in words:
                            if isAuthorHamilton:
                                if word in uniHamilton.keys():
                                    if (word.count('<s>') > 0) or (word.count('</s>') > 0):
                                        uniHamilton[word] = uniHamilton[word] + 0.5
                                    else:
                                        uniHamilton[word] = uniHamilton[word] + 1
                                else:
                                    if (word.count('<s>') > 0) or (word.count('</s>') > 0):
                                        uniHamilton[word] = 0.5
                                    else:
                                        uniHamilton[word] = 1
                            else:
                                if word in uniMadison.keys():
                                    if (word.count('<s>') > 0) or (word.count('</s>') > 0):
                                        uniMadison[word] = uniMadison[word] + 0.5
                                    else:
                                        uniMadison[word] = uniMadison[word] + 1
                                else:
                                    if (word.count('<s>') > 0) or (word.count('</s>') > 0):
                                        uniMadison[word] = 0.5
                                    else:
                                        uniMadison[word] = 1
                        # print(uniHamilton)
                        ### Creating unigram dictionary ###


                        ### Creating bigram dictionary ###
                        for i in range(1, len(words) - 2):
                            if isAuthorHamilton:
                                if words[i] + ' ' + words[i + 1] in biHamilton.keys():
                                    biHamilton[words[i] + ' ' + words[i + 1]] = biHamilton[words[i] + ' ' + words[i + 1]] + 1
                                else:
                                    biHamilton[words[i] + ' ' + words[i + 1]] = 1
                            else:
                                if words[i] + ' ' + words[i + 1] in biMadison.keys():
                                    biMadison[words[i] + ' ' + words[i + 1]] = biMadison[words[i] + ' ' + words[i + 1]] + 1
                                else:
                                    biMadison[words[i] + ' ' + words[i + 1]] = 1
        #print(biHamilton)
                        ### Creating bigram dictionary ###



                        ### Creating trigram dictionary ###
                        cont1 = False
                        cont2 = False
                        for i in range(2, len(words)):
                            if cont1:
                                cont1 = False
                                continue
                            if cont2:
                                cont2 = False
                                continue

                            if isAuthorHamilton:
                                if words[i - 2] + ' ' + words[i - 1] + ' ' + words[i] in triHamilton.keys():
                                    triHamilton[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] = triHamilton[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] + 1
                                else:
                                    triHamilton[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] = 1
                                if (words[i].count('</s>') > 0) and i + 1 != len(words):
                                    cont1 = True
                                    cont2 = True
                            else:
                                if words[i - 2] + ' ' + words[i - 1] + ' ' + words[i] in triMadison.keys():
                                    triMadison[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] = triMadison[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] + 1
                                else:
                                    triMadison[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] = 1
                                if (words[i].count('</s>') > 0) and i + 1 != len(words):
                                    cont1 = True
                                    cont2 = True
                        ### Creating trigram dictionary ###

    ### remove puctuations from data and convert to lowercase ###



def calculateProbability(hamiltonUniDicWordCount, madisonUniDicWordCount):
    ### Creating probability for unigram dictionary ###
    for key in uniHamilton.keys():
        uniProbabilityHamilton[key] = uniHamilton[key] / hamiltonUniDicWordCount

    for key in uniMadison.keys():
        uniProbabilityMadison[key] = uniMadison[key] / madisonUniDicWordCount
    ### Creating probability for unigram dictionary ###


    ### Creating probability for bigram dictionary ###
    for key in biHamilton.keys():
        word = key.split()
        if word[0] == '<s>':
            if word[1] == '<s>':
                continue
            else:
                biProbabilityHamilton[key] = (biHamilton[key]) / (uniHamilton[word[0]])
        else:
            biProbabilityHamilton[key] = (biHamilton[key]) / (uniHamilton[word[0]])

    for key in biMadison.keys():
        word = key.split()
        if word[0] == '<s>':
            if word[1] == '<s>':
                continue
            else:
                biProbabilityMadison[key] = (biMadison[key]) / (uniMadison[word[0]])
        else:
            biProbabilityMadison[key] = (biMadison[key]) / (uniMadison[word[0]])
    ### Creating probability for bigram dictionary ###


    ### Creating probability for trigram dictionary ###
    # for key in triHamilton.keys():
    #     word = key.split()
    #     triProbabilityHamilton[key] = (triHamilton[key] / (biHamilton[word[0] + ' ' + word[1]]))
    #
    #
    # for key in triMadison.keys():
    #     word = key.split()
    #     triProbabilityMadison[key] = (triMadison[key] / (biMadison[word[0] + ' ' + word[1]]))
    #     if key == 'parties are and':
    #         print("triMadison "+key+" "+str(triMadison[key])+" // biMadison "+word[0] + ' ' + word[1]+" "+str(biMadison[word[0] + ' ' + word[1]]))
    #
    ### Creating probability for trigram dictionary ###

def calculateAllWordNumberInFile(dictionary):
    totalWordNumber = 0
    for key in dictionary.keys():
        totalWordNumber += dictionary[key]
    return totalWordNumber

def generateEssayFromUnigram(dictionary, totalWordSize):
    word = []
    rollNumber = []
    cumArray = []
    sentence = ''

    probabilityGeneratedSentence = 1.0
    for key in dictionary:
        word.append(key)
        rollNumber.append(dictionary[key]/totalWordSize)

    cumArray = np.cumsum(rollNumber)

    sentenceFinished = False
    for i in range(0, 30):
        if sentenceFinished:
            continue
        else:
            randomNumber = random.random()
            index = 0
            while cumArray[index] <= randomNumber:
                index += 1
            if word[index] == '</s>':
                if i != 0:
                    sentence = sentence + '.'
                    sentenceFinished = True
                    continue
                else:
                    continue
            elif word[index] == '<s>':
                probabilityGeneratedSentence = probabilityGeneratedSentence * (dictionary[key]/totalWordSize)
                continue
            else:
                probabilityGeneratedSentence = probabilityGeneratedSentence * (dictionary[key]/totalWordSize)
                sentence = sentence + str(word[index]) + ' '
    return sentence, probabilityGeneratedSentence



def generateEssayFromBigram(dictionary, totalWordSize):   #startingWord will be <s>
    sentenceFinished = False
    sentence = ''
    startingWord = '<s>'

    for i in range(0, 30):
        word = []
        rollNumber = []
        cumArray = []

        probabilityGeneratedSentence = 1.0
        for key in dictionary:
            keySplitted = key.split()
            if keySplitted[0] == startingWord:
                word.append(key)
                rollNumber.append(dictionary[key] / totalWordSize)
            else:
                continue

        cumArray = np.cumsum(rollNumber)

        if sentenceFinished:
            continue
        else:
            randomNumber = random.uniform(0, cumArray[len(cumArray) - 1])
            index = 0
            while cumArray[index] <= randomNumber:
                index += 1

            foundWordPair = word[index].split()

            if foundWordPair[1] == '</s>':
                if sentence == '':
                    i -= 1
                    continue
                else:
                    sentence = sentence + '.'
                    sentenceFinished = True
                    continue

            startingWord = foundWordPair[1]

            if i == 0:
                probabilityGeneratedSentence = probabilityGeneratedSentence * (dictionary[key]/totalWordSize)
                continue
            else:
                probabilityGeneratedSentence = probabilityGeneratedSentence * (dictionary[key]/totalWordSize)
                sentence = sentence + str(foundWordPair[0]) + ' '

    return sentence, probabilityGeneratedSentence

def generateEssayFromTrigram(dictionary, totalWordSize):
    sentenceFinished = False
    sentence = ''
    firstWord = '<s>'
    secondWord = '<s>'

    probabilityGeneratedSentence = 1.0
    for i in range(0, 30):
        word = []
        rollNumber = []
        cumArray = []

        for key in dictionary:
            keySplitted = key.split()
            if (keySplitted[0] == firstWord) and (keySplitted[1] == secondWord):
                word.append(key)
                rollNumber.append(dictionary[key] / totalWordSize)
            else:
                continue

        cumArray = np.cumsum(rollNumber)

        if sentenceFinished:
            continue
        else:
            randomNumber = random.uniform(0, cumArray[len(cumArray) - 1])
            index = 0
            while cumArray[index] <= randomNumber:
                index += 1

            foundWordPair = word[index].split()

            if foundWordPair[2] == '</s>':
                if sentence == '':
                    i -= 1
                    continue
                else:
                    sentence = sentence + '.'
                    sentenceFinished = True
                    continue

            firstWord = foundWordPair[1]
            secondWord = foundWordPair[2]

            if i <= 1:
                probabilityGeneratedSentence = probabilityGeneratedSentence * (dictionary[key]/totalWordSize)
                continue
            else:
                probabilityGeneratedSentence = probabilityGeneratedSentence * (dictionary[key]/totalWordSize)
                sentence = sentence + str(foundWordPair[0]) + ' '

    return sentence, probabilityGeneratedSentence



def main():
    for i in inputHamiltonTraining:
        operateFile(readFile(i))

    for i in inputMadisonTraining:
        operateFile(readFile(i))


    hamiltonUniDicWordCount = calculateAllWordNumberInFile(uniHamilton)
    madisonUniDicWordCount = calculateAllWordNumberInFile(uniMadison)


    hamiltonBiDicWordCount = calculateAllWordNumberInFile(biHamilton)
    madisonBiDicWordCount = calculateAllWordNumberInFile(biMadison)

    hamiltonTriDicWordCount = calculateAllWordNumberInFile(triHamilton)
    madisonTriDicWordCount = calculateAllWordNumberInFile(triMadison)

    ###  Gereating Essays  ###
    generatedSentenceForHamiltonUnigram = generateEssayFromUnigram(uniHamilton, hamiltonUniDicWordCount)
    generatedSentenceForHamiltonBigram = generateEssayFromBigram(biHamilton, hamiltonBiDicWordCount)
    generatedSentenceForHamiltonTrigram = generateEssayFromTrigram(triHamilton, hamiltonTriDicWordCount)

    generatedSentenceForMadisonUnigram = generateEssayFromUnigram(uniMadison, madisonUniDicWordCount)
    generatedSentenceForMadisonBigram = generateEssayFromBigram(biMadison, madisonBiDicWordCount)
    generatedSentenceForMadisonTrigram = generateEssayFromTrigram(triMadison, madisonTriDicWordCount)
    ###  Gereating Essays  ###

    # print(generatedSentenceForHamiltonUnigram)
    # print(generatedSentenceForHamiltonBigram)
    # print(generatedSentenceForHamiltonTrigram)
    # print(generatedSentenceForMadisonUnigram)
    # print(generatedSentenceForMadisonBigram)
    # print(generatedSentenceForMadisonTrigram)

    calculateProbability(hamiltonUniDicWordCount, madisonUniDicWordCount)
    total = 0

    # operateTestFile("9.txt")
    # print()
    # operateTestFile("11.txt")
    # print()
    # operateTestFile('12.txt')
    # print()
    # operateTestFile('47.txt')
    # print()
    # operateTestFile('48.txt')
    # print()
    # operateTestFile('58.txt')
    # print()

    # for key in triProbabilityMadison:
    #     total += uniProbabilityHamilton[key]
    #     print(key + " " + str(triProbabilityMadison[key]))

    # for key in triProbabilityHamilton:
    #     total += triProbabilityHamilton[key]
    #     print(key + " " + str(triProbabilityHamilton[key]))

    # for key in biProbabilityHamilton:
    #     total += biProbabilityHamilton[key]
    #     print(key + " " + str(biHamilton[key]))

    # for key in uniProbabilityHamilton:
    #     total += uniProbabilityHamilton[key]
    #     print(key + " " + str(uniProbabilityHamilton[key]))

    print("Total "+str(total))
main()
