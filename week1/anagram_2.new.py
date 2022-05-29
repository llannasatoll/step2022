"""
step2022 -week1-
2. 与えられた文字列の全ての文字を使わなくても良いように関数をアップグレードする

入力：small.txt , medium.txt, large.txt
出力：各単語について「最大のスコアを持つアナグラム」を列挙したファイル
"""
import sys

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# Count the number of letters in the alphabet for a word
def make_table(word):
    data_table = [0] * 26
    for char in word:
        data_table[ord(char) - ord('a')] += 1
    return data_table

# Arrange the table by words with the highest scores.
def sort_tables(dic):
    count_list = []
    for word in dic:
        count_list.append([make_table(word), calc_score(word), word])
    return sorted(count_list, key=lambda x: x[1], reverse=True)

def better_solution(random_word, dictionary, table):
    word_table = make_table(random_word)
    for i in range(len(dictionary)):
        for j in range(26):
            if table[i][0][j] > word_table[j]:
                break
            if j == 25:
                return table[i][2]
    return ""

def calc_score(word):
  return sum([SCORES[ord(char) - ord('a')] for char in word])

def main(files):
    WORDS_FILE = "words.txt"
    answer_files = ["small_answer.txt", "medium_answer.txt", "large_answer.txt"]
    words = []
    with open(WORDS_FILE) as f:
        for line in f:
            words.append(line.rstrip('\n'))

    table = sort_tables(words)

    for i in range(len(files)):
        with open(files[i]) as f:
            with open(answer_files[i], "w") as f_answer:
                for line in f:
                    anagram = better_solution(line.rstrip('\n'), words, table)
                    f_answer.write("%s\n" % anagram)
                
        print("Finished writing %s" % answer_files[i])

if __name__ == "__main__":
    files = ["small.txt", "medium.txt", "large.txt"]
    if len(sys.argv) != 4:
        print("usage: %s %s %s %s" % (sys.argv[0], files[0], files[1], files[2]))
        exit(1)
    
    main([sys.argv[1], sys.argv[2], sys.argv[3]])