# [sim_cafe] main設計書

2026/04/09

------

## クラスの目的（概要）

#### プログラムの目的

pygletを利用してsim_cafeというカフェのシュミレーションプログラムを作ろうとしている

#### 中間地点としての役割

Main クラスがコントローラーとなり各マネージャーを制御する

#### 初期化の依存関係

Mainクラスが各インスタンスの受け取りを行います

#### 描写と更新

バッチを作成してon_drawで描写します。各マネージャーのupdate関数を順番に実行します。



## 利用モジュール一覧

```
import pyglet
from map import Map
from setting import *
from customer_manager import CustomerManager
from seat_manager import SeatManager
from loguru import logger
```

#### pyglet

window, app, graphics.Batch, clockなどを利用

ウィンドウの設定やアプリの実行、バッチやクロックの設定などを行う

#### map

シュミレーションゲームのUIの配置を決めている

#### setting

ゲーム内の各種設定のパラメーターを書いている

#### customer_manager

入り口から待機場所の動線、顧客を削除する

#### seat_manager

座席の割り当て

#### loguru

ログのremoveを行い、ログファイルの作成とログレベルを設定（初期はINFO）

ログの設定についてはログのページで詳細を記載



## プロパティ（保持するデータ）

マネージャー関連：

| **変数名**           | **クラス名**      | **内容・役割**                       |
| -------------------- | ----------------- | ------------------------------------ |
| **map**              | `Map`             | Mapクラスの呼び出し                  |
| **customer_manager** | `CustomerManager` | 顧客の生成・削除・リスト管理         |
| **seat_manager**     | `SeatManager`     | 座席の空き状況管理、顧客の席への移動 |

Pyglet基盤：

| **変数名**            | **クラス名**            | **内容・役割**                                               |
| --------------------- | ----------------------- | ------------------------------------------------------------ |
| **window**            | `pyglet.window.Window`  | メインウィンドウ本体                                         |
| **game_screen_batch** | `pyglet.graphics.Batch` | 画面上の全エンティティを一括描写するためのバッチオブジェクト |
| **width**             | `WINDOW_WIDTH`          | スクリーンの幅                                               |
| **height**            | `WINDOW_HEIGHT`         | スクリーンの高さ                                             |



## 処理フロー（シーケンス）

- 初期化(`__init__`)

  - ログの設定

    以前追加したハンドラーを削除、初期化する（remove()を実行）

    ログファイルの設定（add()の実行）

    ログレベルは初期でINFOにする

  - ウィンドウの設定

    詳しいウィンドウの幅と高さはsetting.pyの詳細設計、**定数定義**に記述

    ウィンドウの幅や高さを取得、setting.pyからタイトルを取得しウィンドウの設定を行う

    ウィンドウサイズが変更できるように設定する(pyglet.window.Window()の使用)

  - バッチの作成

    ゲームスクリーン用のバッチを作成(graphics.Batch()の使用)

    各マネージャークラスを生成する際、各エンティティをバッチに登録

    - バッチに登録するエンティティの種類

      - キャラクター（Simple_moverクラスで生成）

      - 店員（後に追加予定）

      - テーブル（Mapクラス）

      - 椅子（Mapクラス）

      - 統計ラベル（Mapクラス）

  - 各マネージャーの受け取り

    各マネージャーのインスタンスを受け取りプロパティに保持する

    - 背景Map呼び出し

    - CustomerManagerの呼び出し

    - SeatManagerの呼び出し

  - 自動ループの作成

    アプリケーションを動かすために更新頻度を一定に保ち、実行速度を制御し自動ループを作成する

    時間の設定は外部定義（setting.py）からFPSを参照

    参照した値を秒単位の実行時間`1/ FPS`に変更

    pyglet.clock.schedule_intervalを用いて周期的な更新メソッド(self.update)を登録





- 描写(on_draw)

  前のフレームをまっさらな状態にして書き直す（window.clear()の使用）

  描写用のBatchインスタンスの生成

  全要素をスクリーンに描写

- 更新(update)

  マネージャーのupdate関数の呼び出し

  dtを引数にすることで経過時間を更新処理

  - customer_manager
  - seat_manager



## 実行

pyglet.app.run()を呼び出し実行