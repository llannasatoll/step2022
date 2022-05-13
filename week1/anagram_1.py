"""
step2022 -week1-
1. 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
"""

import test2
import time

def make_sortedDict(words): # -> [sorted word, original word] list
    myDic = [["".join(sorted(i)), i] for i in words]
    return sorted(myDic)

def binary_search(lst, word):
    left = 0
    right = len(lst) - 1
    anagrams = []

    while left <= right:
        middle = (left + right) // 2
        x = lst[middle][0]
        if word < x: right = middle - 1 
        elif word > x: left = middle + 1
        else:
            tmp = middle
            while x == lst[tmp][0]:
                anagrams.append(lst[tmp][1])
                if tmp == len(lst)-1: break
                tmp += 1
            tmp = middle-1
            while x == lst[tmp][0]: 
                anagrams.append(lst[tmp][1])
                if tmp == 0: break
                tmp -= 1
            return anagrams
    return anagrams

def find_anagram(random_word, sorted_dictionary): # -> anagrams list
    sorted_random_word = "".join(sorted(random_word))
    anagrams = binary_search(sorted_dictionary, sorted_random_word)
    return anagrams

def main():
    WORDS_FILE = "words.txt"
    words = []
    with open(WORDS_FILE) as f:
        for line in f:
            line = line.rstrip('\n')
            words.append(line)

    while(1):
        #x = input("Please enter letters(a-z, A-Z) : ").lower().replace(" ", "")

        x = "run"
        if not x.isalpha():
            print("Enter only letters.")
        else:
            break
            
    t1 = time.time() 
    for i in range(50):
        myDict = make_sortedDict(words)
    t2 = time.time()

    print("myDic", (t2-t1)/50)

    t1 = time.time() 
    for i in range(50):
        res = find_anagram(x, myDict)
    t2 = time.time()

    print("res", (t2-t1)/50)

    t1 = time.time() 
    for i in range(50):
        myDict = test2.make_sortedDict(words)
    t2 = time.time()

    print("test2.myDic", (t2-t1)/50)

    t1 = time.time()
    for i in range(50):
        res = test2.find_anagram(x, myDict)
    t2 = time.time()

    print("test2.res", (t2-t1)/50)

    if res == []:
        print("There are no words using the letters in \"% s\"." %x)
    else:
        print("Anagram :",", ".join(res))

if __name__ == "__main__":
    main()