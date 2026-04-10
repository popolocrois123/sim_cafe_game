# [sim_cafe] mainの設計書

2026/04/09

------

## 1, クラスの目的（概要）

#### 中間地点としての役割

Main クラスがコントローラーとなり各マネージャーを制御する

#### 初期化の依存関係

各インスタンスの受け取りを行います

#### 描写と更新

バッチを作成してon_drawで描写します。各マネージャーのupdate関数を順番にupdate関数で実行します。



## 2. プロパティ（保持するデータ）

- マネージャー関連： customer_manager, seat_manager, time_manager, map
- Pyglet基盤：window, game_screen_batch

## 3. 処理フロー（シーケンス）

- 初期化(`__init__`)

  各マネージャーのインスタンスを受け取り自信のプロパティに保持する

  描写用のBatchインスタンスの生成

- 更新(update)

  dtにの経過時間によって、customer_manager, seat_managerの更新処理

- 描写(on_draw)

  画面をリセットし、main_batchを用いて全要素をスクリーンに描写

## 4. 実行

pyglet.app.run()を呼び出し実行