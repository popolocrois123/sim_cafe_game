import pyglet
from pyglet.window import key
# from model import Character, Hero
from map import Background, Map
from setting import *
import time
from customer import Customer
from customer_manager import CustomerManager
from seat_manager import SeatManager
from loguru import logger
import sys


class Main():
    def __init__(self):
        # 客の動きを記録
        # self.log_file = open(LOG_PATH, "w", encoding="utf-8")
        # self.start_time = time.time()

        # ログ関数を作って渡す
        # self.logger = Logger(LOG_PATH, max_logs=MAX_LOGS)
        # self.log = self._create_logger()
        # logger.add(sys.stderr, level="SUCCESS")
        ## デフォルト（INFO 以上がコンソールへ）を消す
        logger.remove()

        # INFO のみ通すコンソール出力を追加
        # logger.add(
        #     sink=lambda msg: print(msg, end=""),
        #     filter=lambda r: r["level"].name in ("INFO"),
        #     colorize=True
        # )

        # ログファイル
        logger.add("log_state.log", level="INFO", encoding="utf-8")

        



        # 引数として渡されたwidthとheightを取り出す
        self.width = len(MAP_DATA[0]) * CELL_SIZE
        self.height = len(MAP_DATA) * CELL_SIZE

        # windowの設定
        self.window = pyglet.window.Window(width=self.width, height=self.height,
                                            caption="rpg", resizable=True)
        self.window.set_location(x=400, y=200)
        self.window.set_minimum_size(width=500, height=500)

        # キーを押している間だけ動く
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        
        # batchの作成
        self.batch = pyglet.graphics.Batch()

        # キャラクターのリスト
        self.characters = []


        # self.logger.log("マップの読み込み開始")
        # 背景のmapクラスの呼び出し
        self.map = Map(MAP_DATA, CELL_SIZE, self.batch, self.height)

        # 背景の呼び出し
        # self.background = Background(self.window, self.batch)

        # # playerのスタート位置の呼び出し
        # px, py = self.map.player_start

        # CustomerMageクラスの呼び出し
        self.customer_manager = CustomerManager(self, MAP_DATA, self.map)
        
        # SeatManagerクラスの呼び出し
        self.seat_manager = SeatManager(self, self.map)

        # mainでデバッグを使う方法
        logger.debug("mainの初期化完了しました。")

        
        # Heroの操作用
        self.window.push_handlers(self)

        pyglet.clock.schedule_interval(self.update, 1/30)


    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def update(self, dt: float):
        self.customer_manager.update(dt)
        self.seat_manager.update(dt)
        

if __name__ == "__main__":
    game = Main()
    pyglet.app.run()
