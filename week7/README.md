# Google STEP Class 7 Homework

## 課題1
以下のような行列積を求めるループ順序としては6種類の組合せがある。この6種類を実行速度が速いと思う方から順に並べてください。実際に実験してその予想が正しいかどうか確かめてください。

- i-j-k, i-k-j, j-i-k, j-k-i, k-i-j, k-j-i

```C++
for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
        for (k = 0; k < n; k++)
            c[i][j] += a[i][k] * b[k][j];
```

### 実行方法

ファイル:matrix/matrix.cpp

```
% g++ -o martix matrix.cpp -std=c++11
```

```
% ./matrix N
```

(Nは行列サイズ)
<br>
<br>

## 課題3
これまでの7回の授業で学んできたことを総合して、TSP Challengeのプログラムを最適化して、Challenge 6（都市数＝2048）のベストスコア更新とChallenge 7（都市数＝8192）のベストスコアを目指す！！

<br>


<br>

## 1. Genetic Algotrithm

詳しい実装方法は[week5](https://github.com/llannasatoll/step2022/tree/main/week5)。

今回は、初期個体群はランダムに生成を行う。

### 実行方法
ファイル：solver_ga.cpp
```
% g++ -o solver_ga solver_ga.cpp common.cpp genetic_algorithm.cpp
```
```
% ./solver_ga [inputfile]
```
出力：ga_(都市数).csv



## 2. 3-opt

<img src="https://github.com/llannasatoll/step2022/blob/main/week7/img/3-opt.png" width="800">

これは[week5](https://github.com/llannasatoll/step2022/tree/main/week5)での(1)2-optを包含している。

貪欲法（greedy）で初期経路を求め、3-optで最適化を行う。

今回は10回繰り返し、最も距離が短かった経路をファイルに出力する。(Challenge 7は1回)
ここで、貪欲法を始める点は、直前に求めた経路の中で最も長い辺を構成する点とする。


### 実行方法

ファイル：solver_3opt.cpp
```
% g++ -o solver_3opt solver_3opt.cpp common.cpp
```
```
% ./solver_3opt [inputfile]
```
出力：3opt_(都市数).csv


### 実行結果

| Challenge 0 | Challenge 1 | Challenge 2 | Challenge 3 | Challenge 4 | Challenge 5 | Challenge 6 | Challenge 7 | 
|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
|3291.62|3778.72|4494.42|8274.17|10664.9|20575.8|40819.9| 82115.9|
