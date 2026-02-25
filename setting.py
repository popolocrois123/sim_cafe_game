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
TIMER_GRID = (3, 3)

# 混み具合のラベルの位置
CROWD_GRID = (10, 3)


# lofファイルの読み込み
LOG_PATH = "customer_lifecycle.log"
MAP_DATA = [
    'BBBBBBBBBBBBBBBBBBB',
    'NGGGGGGGGGGGGGGGGGN',
    'NGGGGGGGGGGGGGGGGGN',
    'BBBBBBBBBBBBBBBBOEB',
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