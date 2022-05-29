"""
step2022 -week1-
1. 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
"""

def make_sortedDict(words): # -> {sorted word : [original words]}
    sorted_to_originals = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in sorted_to_originals:
            sorted_to_originals[sorted_word] = []
        sorted_to_originals[sorted_word].append(word)
    return sorted_to_originals

# Returns anagrams or empty list if not found.
def find_anagrams(word, sorted_to_originals):
    sorted_word = "".join(sorted(word))
    if sorted_word in sorted_to_originals:
        return sorted_to_originals[sorted_word]
    else:
        return []

def main():
    WORDS_FILE = "words.txt"
    words = []
    with open(WORDS_FILE) as f:
        for line in f:
            words.append(line.rstrip('\n'))

    while True:
        x = input("Please enter letters(a-z, A-Z) : ").lower().replace(" ", "")
        if not x.isalpha():
            print("Enter only letters.")
        else:
            break
            
    myDict = make_sortedDict(words)
    res = find_anagrams(x, myDict)

    if res == []:
        print("There are no words using the letters in \"% s\"." %x)
    else:
        print("Anagram :",", ".join(res))

if __name__ == "__main__":
    main()