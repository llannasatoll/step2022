"""
step2022 -week1-
2. 与えられた文字列の全ての文字を使わなくても良いように関数をアップグレードする

入力：small.txt , medium.txt, large.txt
出力：各単語について「最大のスコアを持つアナグラム」を列挙したファイル
"""

import sys
import itertools
import anagram_1
import test2

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]


# Count the number of letters in the alphabet for each word
def make_table(dic):
    count_list = []
    for word in dic:
        data_table = [0] * 26
        for char in word[0]:
            data_table[ord(char) - ord('a')] += 1
        count_list.append(data_table)
    return count_list

# (Method1) Find anagrams for all combinations
def binary_search_solution(random_word, dictionary):
    lst = []
    anagram = []
    for i in range(1, len(random_word)+1):
        lst += set(itertools.combinations(random_word, i))
    
    for i in lst:
        anagram += anagram_1.find_anagram("".join(i), dictionary)
    return anagram

# (Method2) Find anagrams based on the table
def better_solution(random_word, dictionary, table):
    word_table = [0] * 26
    for char in random_word: 
        word_table[ord(char) - ord('a')] += 1

    anagram = []
    for i in range(len(dictionary)):
        for j in range(26):
            if table[i][j] > word_table[j]:
                break
            if j == 25:
                anagram.append(dictionary[i][1])
    return anagram

# Calculate each score and find the best anagram
def calc_bestanagram(anagramlist):
    max = 0
    best_anagram = ""
    for i in anagramlist:
        score = 0
        for char in i:
            score += SCORES[ord(char) - ord('a')]
        if max < score:
            max = score
            best_anagram = i
    return best_anagram

def main(files):
    WORDS_FILE = "words.txt"
    answer_files = ["small_answer.txt", "medium_answer.txt", "large_answer.txt"]
    answer_files = ["small_answer.txt"]
    words = []
    with open(WORDS_FILE) as f:
        for line in f:
            line = line.rstrip('\n')
            words.append(line)

    #myDict = anagram_2.make_sortedDict(words)
    #table = make_table(myDict)

    myDict = test2.make_sortedDict(words)
    table = test2.make_table(myDict)

    for i in range(len(files)):
        test = []
        with open(files[i]) as f:
            for line in f:
                line = line.rstrip('\n')
                test.append(line)

        #res = [calc_bestanagram(better_solution(i, myDict, table)) for i in test]
        res = [calc_bestanagram(test2.better_solution(i, myDict, table)) for i in test]


        #res = [calc_bestanagram(binary_search_solution(i, myDict)) for i in test]

        with open(answer_files[i], "w") as f:
            for word in res:
                f.write("%s\n" % word)
        
        print("Finished writing %s" % files[i])

if __name__ == "__main__":
    """    
    if len(sys.argv) != 4:
        print("usage: %s small.txt medium.txt large.txt" % sys.argv[0])
        exit(1)
    """
    #main([sys.argv[1], sys.argv[2], sys.argv[3]])
    main([sys.argv[1]])
