# sim_cafe_game# 店内にいる顧客数と混み具合の情報について



## 目的

店内にいる顧客数と店内の混み具合の情報を知りたい



## 実現方法

 現状は顧客生成数があって待機場所の設定数と食べる用の椅子を利用して、

それぞれの合計を計算する。店内にいる顧客数を分子、分母は店の待機場所と椅子の数の合計が分母になる。



## 詳細

### customer_managerクラス

①、**self.wait_chair**を利用

この中に存在するTrueの数を取得



### seat_managerクラス

②、**self.seat_in_use**

Trueの数を取得

### setting.py

③、**MAP_DATA**（マップの情報をリストにした）を利用

W(待機場所)、S(座席)の数を取得



### 計算

上記の

#### ① + ②

店にいる客の数を取得





上記の

#### (① + ②) / ③ * 100

によって客が待機場所と席を占有している割合を取得



## 表示

### setting.py

MAP_DATAに**A**を追加

場所はMAP_DATA0行目、10列目

A: 店内にいる客の計算結果を表示



MAP_DATAに**D**を追加

場所はMAP_DATA0行目、13列目

B：店内にいる客が待機場所と席を占有している割合を追加



### main.py

`self.map = Map()`の引数にselfを追加



### map.py

#### init

self.parent.customer_manager よりwait_chairを取得して変数

self.wait_chair

**①true_wait_chair** に.count関数を用いてTrueの数を数える

`true_wait_chair = self.wait_chair.count(True)`





self.parent.seat_managerよりself.seat_in_useを取得して変数

self.seat_in_use

**②true_seat_in_use**変数に.count()関数を用いてTrueの数を数える

`true_seat_in_use = self.seat_in_use.count(True)`



setting.pyのMAP_DATAよりWとSの数を取得

変数self.W_count

self.S_count 

sum関数とジェネレータ式を使用

ジェネレータ式については[ここ](https://gitlab.com/ppl_crs/second-brain/-/blob/e3e3758608c4e39180cabb606a69d4e6edb09609/Concepts/python/python_core/%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AC%E3%83%BC%E3%82%BF%E5%BC%8F_%E5%80%A4%E3%82%92%E9%A0%86%E7%95%AA%E3%81%AB%E7%94%9F%E6%88%90%E3%81%99%E3%82%8B_%E3%83%AA%E3%82%B9%E3%83%88%E5%86%85%E3%81%AE%E7%89%B9%E5%AE%9A%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E6%95%B0%E3%82%92%E6%95%B0%E3%81%88%E3%82%8B)

`self.W_count = sum(w.count("W") for w in MAP_DATA)`

`self.S_count = sum(s.count("S") for s in MAP_DATA)`

この二つを加算する

`self_sum_w_s_count = self.w_count + self.s_count`



#### load_map

if文によるマップの場合分けで壁を担当するBに

`or cell == "A"` `or cell == "D"`の場合を追加

`if cell == "B" or cell == "C" or cell == "H" or cell == "A" or cell == "C":`とする

通常のBのコードが終わった後に

case文でAの場合とDの場合に分ける



#### Aの場合

#### ① + ②

店にいる客の数を取得



#### Dの場合

(① + ②) / ③ * 100

店の待機場所と席の占有率を取得
