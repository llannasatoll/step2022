"""
step2022 -week1-
2. 与えられた文字列の全ての文字を使わなくても良いように関数をアップグレードする

実装方法：
アルファベットに素数を割り振り、文字列に含まれるアルファベット分の素数の積を計算し、割り算を行うことで、アナグラムかどうかを判断する。

入力：small.txt , medium.txt, large.txt
出力：各単語について「最大のスコアを持つアナグラム」を列挙したファイル
"""
import sys

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

def make_prime_list(n):
    """Make prime numbers list
    [Args]
    n : The size of list
    [Return]
    prime numbers list
    """
    x = 3
    primes = [2]
    while len(primes) < n:
        for i in range(2, x):
            if not (x % i):
                break
            if x == (i+1):
                primes.append(x)
        x += 1
    return primes

def make_num(word):
    num = 1
    for char in word:
        num *= PRIMES[ord(char) - ord('a')]
    return num

# Arrange the table by words with the highest scores.
def sort_tables(dic):
    count_list = []
    for word in dic:
        count_list.append([make_num(word), calc_score(word), word])
    return sorted(count_list, key=lambda x: x[1], reverse=True)

def better_solution(random_word, dictionary, table):
    ans_num = make_num(random_word)
    for target in table:
        if not (ans_num % target[0]):
            return target[2]
    return None

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
    PRIMES = make_prime_list(26)
    
    if len(sys.argv) != 4:
        print("usage: %s %s %s %s" % (sys.argv[0], files[0], files[1], files[2]))
        exit(1)

    main([sys.argv[1], sys.argv[2], sys.argv[3]])