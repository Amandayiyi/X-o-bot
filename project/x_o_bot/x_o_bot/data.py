
import sys, os, re
from collections import defaultdict

import json

# function read dictionary from Dialogflow data
def readDict():

    dictionary = defaultdict(list)

    for root, dirs, files in os.walk('.'): # os.walk('./dataset/entities'):

        for file in files:
            if re.match(r'.*_entries_en\.json', file):
                # print(os.path.join(root, file))
                with open(os.path.join(root, file), 'r') as f:
                    readdict = json.load(f)
                    for i in range(len(readdict)):
                        readdict_temp = readdict[i]
                        dictionary[readdict_temp['value']].extend(readdict_temp['synonyms'])
    return dictionary


def readQuestions():

    questions = []

    for root, dirs, files in os.walk('.'): # os.walk('./dataset/intents'):

        for file in files:
            if re.match(r'.*_usersays_en\.json', file):
                # print(os.path.join(root, file))
                with open(os.path.join(root, file), 'r') as f:
                    readdict = json.load(f)
                    for i in range(len(readdict)):
                        question = ''
                        for text in readdict[i]['data']:
                            # print(text)
                            if text['userDefined']:
                                question += text['alias']
                            else:
                                question += text['text']
                        # print(end = '-------------\n')
                        # print(question)
                        questions.append(question)

    return list(set(questions))

'''
    Base on Levenshtein Distance count two strings similarity:
    Apply:
        Two strings: S1 and S2
        Create a table: (len(S1) + 1) * (len(S2) + 1)
        When i = 0, j = range(0, len(S1))
        When j = 0, i = range(0, len(S2))

        S1[i] == S2[j] temp = 0, otherwise temp = 1

        for each cell in tale except mentioned above: i, j
        table[i, j] = min(table[i - 1, j] + 1, table[i, j - 1] + 1, table[i - 1, j - 1] + temp)
        
        As a reasult: table[len(S1), len(S2)] is the Levenshtein Distance
        Similarity: 1 - 1 / max(len(S1), len(S2)) 

'''
def levenshtein_distance(string1, string2):

    length_s1 = len(string1)
    length_s2 = len(string2)
    if length_s1 == 0:
        return length_s2
    if length_s2 == 0:
        return length_s1

    matrix = [[0 for _ in range(length_s2 + 1)] for _ in range(length_s1 + 1)]
    
    for i in range(length_s1 + 1):
        matrix[i][0] = i
    for j in range(length_s2 + 1):
        matrix[0][j] = j

    for i in range(1, length_s1 + 1):
        for j in range(1, length_s2 + 1):
            if string1[i - 1] == string2[j - 1]:
                temp = 0
            else:
                temp = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + temp)

    return matrix[length_s1][length_s2]

def similarity_ld(string, list_of_string):

    similarity_ = []
    for s in list_of_string:
        ld = levenshtein_distance(string, s)
        similarity_.append(1 - ld / max(len(string), len(s)))
    

    re_list_of_string = []
    while len(re_list_of_string) < 3:
        max_similarity = max(similarity_)
        for i in range(len(similarity_)):
            if similarity_[i] == max_similarity:
                re_list_of_string.append(list_of_string[i])
                similarity_[i] = 0.0
    return re_list_of_string

def similarity(string, debug = 0):
    dictionary = readDict()
    questions = readQuestions()
    if debug:
        print('data.py Debug Checking: ')
        num = 0
        for question in questions:
            num += 1
            print(question)
        print(num)
    re = similarity_ld(string, questions)
    return re

if __name__ == '__main__':
    print(similarity('UNSW', debug = 1))