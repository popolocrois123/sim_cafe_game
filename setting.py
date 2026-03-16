import random

CELL_SIZE = 32
MAX_LOGS = 100

# 顧客の飲食時間
STAY_DURATION = 2

# 顧客生成の上限
MAX_CUSTOMERS = 50

# 新規顧客の生成間隔
## 顧客生成の間隔のずれを作る
second_random = random.random()
SPAWN_TIME = (3 / MAX_CUSTOMERS) + second_random

# 生成数の時間ごとの変動の辞書
EMPTY_GENERATE = 3
CROWD_GENERATE = 0.5

CUSTOMER_CROWD = {0: "c", 1: "e", 2: "e", 3: "e", 4: "e", 5: "c",
                  6: "c", 7: "c", 8: "c", 9: "e", 10:"e", 11: "e",
                  12: "c", 13: "c", 14: "e", 15: "e", 16: "e", 
                  17: "c", 18: "c", 19: "c", 20: "e", 21: "c", 22: "c",
                  23: "c"}

# [宿題]
# 店内が空いているか普通か混んでいるかの目安の客数
# 混んでいる
AVAILABLE = 5
LIMITED_SEATING = 10
FULL_CUSTOMER = 20


# 時計ラベルの位置
TIMER_GRID_X, TIMER_GRID_Y = (3, 3)

# 混み具合のラベルの位置
CROWD_GRID = (10, 3)


# lofファイルの読み込み
LOG_PATH = "customer_lifecycle.log"

# ------------------------------------------------
# --- シュミレーション画面の要素 ---
# B: 壁（キャラが通れない）
# .: 何もない場所（移動可能）
# G: キャラ生成場所
# N: 生成場所の端
# E: 入り口
# O: 出口
# W: キャラの待機場所
# T: テーブル
# S: 席

# --- 統計情報の要素 ---
# I: 統計画面の何もない場所
# H: 時間
# C: 席の混み具合
# A: 店の客数
# D: 店の待機場所と席の占有率
# -------------------------------------------------
MAP_DATA = [
    'HBBBBBBABBBBBBBBBBB',
    'NGGGGGGGGGGGGGGGGGN',
    'NGGGGGGGGGGGGGGGGGN',
    'CBBBBBBBDBBBBBBBOEB',
    'B................WB',
    'B................WB',
    'B.STS.STS........WB',
    'B................WB',
    'B.STS.STS........WB',
    'B................WB',
    'B.STS.STS........WB',
    'B................WB',
    'B.STS.STS........WB',
    'B................WB',
    'BBBBBBBBBBBBBBBBBBB'
]