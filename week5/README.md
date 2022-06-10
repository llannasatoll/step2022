# Google STEP Class 5 Homework

## 課題内容

#### Traveling Salesman Problemに挑戦！

<br>

## 使用するデータ

https://github.com/hayatoito/google-step-tsp

[このリポジトリ](https://github.com/llannasatoll/step2022/new/main/week5)にはオリジナルのものだけを入れています。
<br><br>

## 実装

### (1) 2-opt(solver_2opt.py)

交差している2本の辺があったら、解くように経路を更新していく。

![./img/2opt.png](https://github.com/llannasatoll/step2022/blob/main/week5/img/2opt.png)

```Python
#以下を交差がなくなるまで繰り返す。

for i in range (N-2):
    for j in range(i+2, N):
      l1 = dist[solution[i]][solution[i+1]]
      l2 = dist[solution[j]][solution[(j+1) % N]]
      l3 = dist[solution[i]][solution[j]]
      l4 = dist[solution[i+1]][solution[(j+1) % N]]
      if l1+l2 > l3+l4: #入れ替えた方が短かったら
          new_solution = solution[i+1:j+1]
          solution[i+1:j+1] = new_solution[::-1]
```

ここで、初期値として与える経路は、greedy法を採用する。

<br><br>

### (2) 遺伝的アルゴリズム(genetic_algorithm.py)
以下のように処理をしていく。
1. 初期集団生成(solver_ga.py)
2. 評価(以下はgenetic_algorithm.py)
3. 選択
4. 交叉
5. 突然変異

#### 1. 初期集団(initial_population)生成
- 方法1 : 全てランダムな経路

- 方法2 : ランダムに選んだ点を始点として貪欲法で生成した経路

- 方法3 : 貪欲法のあとに2-optを行った経路

（このとき、直前に作った経路で、最も長かった辺を構成する点を始点として、次の経路を生成する。）


<br>

#### 2.　評価(GeneticAlgorithm._to_next_generation())
今回は閾値は設けず、指定した世代数までの遺伝が終わったら終了とする。

<br>

#### 3. 選択(GeneticAlgorithm.selection())
今回は、エリート選択方式とルーレット選択方式を同時に用いる。

- エリート選択方式 : 適応度が高い個体を次世代に引き継ぐ方法<br>
- ルーレット選択方式 : 各個体の適応度に合わせて選択確率を変え、この確率に沿って次世代となる個体を残していく方法

<br>

#### 4. 交叉（GeneticAlgorithm.crossover()）
選択によって決定された個体群から、交叉確率に基づいて親を選び、交叉対象の親の集団を作る。そこからランダムに親のペアを作り、交叉させて子個体と入れ替える。

<br>

今回は **循環交叉(Chromosome.cyclic_crossover())** を採用する。

2つの親から、点の組と位置の組が等しいグループを探し、グループ同士を交換する。
1. 親1からランダムな都市$a_1$を選択（$a_i = a_1$）。
2. 親1から都市$a_i$を探し、その位置をj番目として、親2の$j$番目の都市を$a_{i+1}$とする。
3. $a_{i+1} = a_1$なら終了。そうでなければ2を繰り返す。

![./img/cyclic_crossover.png](https://github.com/llannasatoll/step2022/blob/main/week5/img/cyclic_crossover.png)

<br>

#### 5. 突然変異(GeneticAlgorithm.matate())

変異確率に基づいて、突然変異を行う。

今回は **経路の交換（GeneticAlgorithm.swap_mutation（))** を採用する。

![./img/swap_mutation.png](https://github.com/llannasatoll/step2022/blob/main/week5/img/swap_mutation.png)


## 結果(myresult/)
GAの各パラメータ
- 世代数　　　: 10000
- 個体数　　　: 10
- 交叉率　　　: 0.9
- 突然変異率　: 0.2
- 選択方式　　： エリート選択方式(30%)、ルーレット選択方式(70%)


|              | N                          | 2opt         | ga(random) | ga(greedy)| ga(greedy+2opt) |  
|------------- | -------------------------: | -------------------   | ----------    | ----------               | ----------  |
|Challenge 0   |                          5 |  3418.10              | 3291.62       | 3291.62                  | 3291.62 |
|Challenge 1   |                          8 | 3832.29               | 3778.72       | 3778.72                  | 3778.72 |
|Challenge 2   |                         16 |  4994.89              | 4944.16       | 4873.83                  | 4494.42 |
|Challenge 3   |                         64 | 8970.05               | 16909.75      | 9339.95                  | 8374.08 |
|Challenge 4   |                        128 |11489.79               | 38009.72      | 12084.38                 | 11182.28 |
|Challenge 5   |                        512 | 21363.60              | 206831.98     | 24673.01                 |  21169.58 |
|Challenge 6   |                       2048 | 42712.37              | 1157232.45    | 48405.39                 | 42045.51 |


## 参考結果(sample/)

|              | N                          | sa          | random |greedy      |
|------------- | -------------------------: | -------------------| ----------    | ----------  |
|Challenge 0   |                          5 | 3291.62            | 3862.20       | 3418.10   |
|Challenge 1   |                          8 | 3778.72            | 6101.57       | 3832.29   |
|Challenge 2   |                         16 | 4494.42            | 13479.25      | 5449.44   |
|Challenge 3   |                         64 | 8150.91            | 47521.08      | 10519.16  | 
|Challenge 4   |                        128 | 10675.29           | 92719.14      | 12684.06  | 
|Challenge 5   |                        512 | 21119.55           | 347392.97     | 25331.84  | 
|Challenge 6   |                       2048 | 44393.89           | 1374393.14    | 49892.05  | 

