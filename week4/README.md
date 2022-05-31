# Google STEP Class 4 Homework

## 課題内容

#### 1. Wikipediaのグラフを使ってなにか面白いことをしてみよう
- 必須："Google"から"渋谷"までをたどる方法をDFSとBFSで探す
- その他なんでも
  - 例：孤立している隠されたページを探す
  - 例：ページランクの高いものを探す

#### 2. 他の人の書いたコードを自分の環境で実行してレビューする

## 使用するグラフデータ

`data/` に含まれる以下の2つのファイル

- pages.txt：各ページのidとタイトルのリスト
  - 形式:(ID)\t(ページ名)
- links.txt：各リンクのリンク元とリンク先のリスト
  - 形式：(ID)\t(ID)

## 実行方法

DFS: wikipedia_dfs.py

BFS: wikipedia_bfs.py

(テスト環境: Python 3.9.12)

```shell
python3 wikipedia_dfs.py
```
その後、
```shell
START : 
```
と出てきたらスタートページ(`Google`)、
```shell
GOAL : 
```
と出てきたら目標ページ(`渋谷`)を入力してください。
(結果出力から、プログラムの実行終了まで少し時間がかかることがあります。)
