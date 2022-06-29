# Google STEP Class 2 Homework

## 課題内容

#### 1. matrix.cpp
以下のような行列積を求めるループ順序としては6種類の組合せがある。この6種類を実行速度が速いと思う方から順に並べてください。実際に実験してその予想が正しいかどうか確かめてください。

- i-j-k, i-k-j, j-i-k, j-k-i, k-i-j, k-j-i

```C++
for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
        for (k = 0; k < n; k++)
            c[i][j] += a[i][k] * b[k][j];
```

#### 3. solver_ga.cpp
これまでの7回の授業で学んできたことを総合して、TSP Challengeのプログラムを最適化して、Challenge 6（都市数＝2048）のベストスコア更新とChallenge 7（都市数＝8192）のベストスコアを目指す！！

## 結果

% ./matrix 3000
j-k-i time: 127 sec
j-k-i time: 64 sec
j-k-i time: 162 sec
j-k-i time: 257 sec
j-k-i time: 67 sec
j-k-i time: 255 sec
sum: 3280499392500009457942528.00000

3opt
0 3289
1 3775
2 4486
3 8243
4 10601
5 20323
6
7

challenge 7
78021.000000

ga
0 3289
1 3775
2 4656
3 21958
4 50285
5 300964
6