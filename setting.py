import random
from enum import Enum
from types import SimpleNamespace

# =========================
# 基本設定
# =========================
CELL_SIZE = 32 # タイル1マスのピクセルサイズ
MAX_LOGS = 100 # ログの最大保存数

STAY_DURATION = 2 # 顧客が席に座っている時間の基本値（秒）
MAX_CUSTOMERS = 50 # 店内に同時に存在できる顧客の最大数（待機も含む）


# =========================
# 混雑状態
# =========================
class CrowdLevel(Enum):
    EMPTY = "empty" # 空いている
    NORMAL = "normal" # 普通
    CROWDED = "crowded" # 混雑している


AVAILABLE = 5 # 混雑レベルの閾値（この人数以下なら空いている）
LIMITED_SEATING = 10 # 混雑レベルの閾値（この人数以下なら普通、それ以上なら混雑）
FULL_CUSTOMER = 20 # 混雑レベルの閾値（この人数以上なら満席）


# =========================
# 混雑レベル判定
# =========================
# 顧客数に基づいて混雑レベルを判定する関数
def get_crowd_level(customer_count):
    if customer_count < AVAILABLE:
        return CrowdLevel.EMPTY
    elif customer_count < LIMITED_SEATING:
        return CrowdLevel.NORMAL
    else:
        return CrowdLevel.CROWDED
    
# =========================
# 客の状態についての定義
# =========================
# 顧客の状態を定義するEnum
Customer_State = SimpleNamespace(
    OUTSIDE=1, # 待機中
    MOVING_TO_ENTRANCE=2,   # 入口に向かっている
    ARRIVE=3,    # 入口に到着
    MOVING_TO_WAIT=4, # 待機エリアに向かっている
    WAITING_IN_QUEUE=5, # 待機列に並んでいる
    WAITING_TO_SIT_TO_SEAT=6, # 席に座る準備をしている
    MOVING_TO_SEAT=7, # 席に向かっている
    SEATED=8,    # 着席中
    LEAVING=9, # 席を立っている
    EXITED=10 # 店を出た
)


# =========================
# 時間帯ごとの混雑傾向
# =========================
"""
0-4時は空いている
5-8時は普通
9-10時は混雑している
11-13時は普通
14-16時は空いている
17-19時は混雑している
20時以降は空いている
"""
# 時間帯ごとの混雑傾向を定義
# 混雑しているの設定
CUSTOMER_CROWD = {
    i: CrowdLevel.CROWDED for i in range(24)
}

# 上書き、空いているの設定（必要な時間帯のみ調整）
for i in [0, 1, 2, 3, 4, 14, 15, 16, 20, 21, 22, 23]:
    CUSTOMER_CROWD[i] = CrowdLevel.EMPTY

# 上書き、普通の設定（必要な時間帯のみ調整）
for i in [5, 6, 7, 8, 11, 12, 13]:
    CUSTOMER_CROWD[i] = CrowdLevel.NORMAL

# =========================
# 顧客生成による混雑レベルによる生成数の調整
# =========================
CROWD_GENERATE = 0.5 # 混雑設定の時の生成基本間隔（秒）
EMPTY_GENERATE = 5.0 # 空いているときの生成基本間隔（秒）
NORMAL_GENERATE = 2.0 # 普通のときの生成基本間隔（秒)


# =========================
# 顧客生成
# =========================
# 顧客生成時間の初期設定
SPAWN_TIME = NORMAL_GENERATE # 初期値は普通の生成間隔

# 時間帯による生成制御
def get_spawn_time(hours):
    crowd_level = CUSTOMER_CROWD.get(hours)
    match crowd_level:
        case CrowdLevel.CROWDED:
            SPAWN_TIME =  CROWD_GENERATE
        case CrowdLevel.EMPTY:
            SPAWN_TIME =  EMPTY_GENERATE
        case CrowdLevel.NORMAL:
            SPAWN_TIME =  NORMAL_GENERATE
        case _:
            SPAWN_TIME = NORMAL_GENERATE  # デフォルト値
    return SPAWN_TIME + random.randint(0, 2) # 生成間隔にランダムなばらつきを追加



# =========================
# UI配置
# =========================
# 統計表示のグリッド位置
TIMER_GRID_X, TIMER_GRID_Y = (3, 3) # 時刻表示
CROWD_GRID = (10, 3) # 混雑率表示

LOG_PATH = "customer_lifecycle.log" # ログファイルのパス


# =========================
# タイル定義（意味ベース）
# =========================

# 役割ごとの定義
WALL = "WALL"           # 通れない
FLOOR = "FLOOR"         # 通れる

SPAWN = "SPAWN"         # 顧客出現
SPAWN_EDGE = "SPAWN_EDGE" # 顧客出現エリアの境界（出現エリアの外側に配置される）

ENTRANCE = "ENTRANCE" # 入口
EXIT = "EXIT" # 出口

WAIT = "WAIT" # 待機エリア
TABLE = "TABLE" # テーブル
SEAT = "SEAT" # 席

# INFO系ラベルを分離
TIME_LABEL = "H"
CROWD_LABEL = "C"
CUSTOMER_LABEL = "A"
WAIT_LABEL = "D"



# =========================
# マップ文字 → 意味 変換テーブル
# =========================

TILE_MAP = {
    "B": WALL,
    ".": FLOOR,
    "G": SPAWN,
    "N": SPAWN_EDGE,
    "E": ENTRANCE,
    "O": EXIT,
    "W": WAIT,
    "T": TABLE,
    "S": SEAT,
    "H": TIME_LABEL,
    "C": CROWD_LABEL,
    "A": CUSTOMER_LABEL,
    "D": WAIT_LABEL,
}

# =========================
# マップデータ
# =========================
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
