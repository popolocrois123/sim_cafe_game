import random

CELL_SIZE = 32
MAX_LOGS = 100

# 顧客の飲食時間
## 宿題！
STAY_DURATION = 2

# 顧客生成の上限
MAX_CUSTOMERS = 50

# 新規顧客の生成間隔
## 顧客生成の間隔のずれを作る
second_random = random.random()
SPAWN_TIME = (3 / MAX_CUSTOMERS) + second_random

# 時計ラベルの位置
TIMER_GRID = (3, 3)


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