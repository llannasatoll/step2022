# Google STEP Class 6 Homework

## 課題内容

#### Malloc Challenge!

1. 複数の空き領域が使えるときに、十分な大きさの空き領域のうち最も小さいものを選ぶ、Best-fitを実装。

2. 空き領域を格納するfree listをサイズの範囲ごとに複数用意して、実行時間の短縮をする、Freelist-binを実装。

<br>

## 実装方法

### 1. Best-fit

空き領域リストを全て見て、以下のようにして最も適切な領域を見つける。

```C
while (metadata) { //空き領域リストを最後まで見る

  //best空き容量よりも小さい、かつ、mallocしたいsizeよりも大きかったら、bestを更新
  if(best_metadata_size > metadata->size && metadata->size >= size){
    best_prev = prev;
    best_metadata = metadata;
    best_metadata_size = metadata->size;
  }
}
```

### 2. Freelist-bin

以下のように、領域のサイズに合わせた、4つの空き領域リストを作る。

<img src="https://github.com/llannasatoll/step2022/blob/main/week6/freelist_bin.png" heigh="200">

0番目のリストには、小さすぎてこれ以上割り当てられない領域を格納する。
最も適切な領域が入っていそうなリストから探して、十分な領域が見つからなかったら次のリスト、と探していく。

一つのリストから、割り当てる領域を探すときはBest-fitを用いる。


## 実行結果
|Challenge #1    |   simple_malloc |       best-fit | freelist-bin |
|--------------- | --------------- | ---------------| ---------------|
|       Time [ms]|              16 |          1008  |            804|
|Utilization [%] |              70 |              70|              70|

|Challenge #2    |   simple_malloc |       best-fit|freelist-bin |
|--------------- | --------------- | ---------------| ---------------|
|       Time [ms]|               7 |              650|             282|
|Utilization [%] |              40 |              40|              40|

|Challenge #3    |   simple_malloc |      best-fit|freelist-bin |
|--------------- | --------------- | ---------------| ---------------|
|       Time [ms]|              78 |             763|             295|
|Utilization [%] |               8 |              50|              50|

|Challenge #4    |   simple_malloc |       best-fit|freelist-bin |
|--------------- | --------------- | ---------------| ---------------|
|       Time [ms]|           18481 |             7111|             386|
|Utilization [%] |              15 |              71|              71|

|Challenge #5    |   simple_malloc |       best-fit|freelist-bin |
|--------------- | --------------- | ---------------| ---------------|
|       Time [ms]|           11774 |            4015|            1127|
|Utilization [%] |              15 |              74|              74|
