import pyglet
from pyglet.window import key
# from model import Character, Hero
from map import Background, Map
from setting import *
import time
from customer import Customer
from customer_manager import CustomerManager
from seat_manager import SeatManager
from time_manager import TimeManager
from crowd_manager import CrowdManager

from loguru import logger
import time
import sys


class Main():
    def __init__(self):
        logger.remove()
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
        
        # ゲームスクリーン用のバッチの作成
        self.game_screen_batch = pyglet.graphics.Batch()

        # キャラクターのリスト
        self.characters = []


        # 背景のmapクラスの呼び出し
        self.map = Map(self, MAP_DATA, CELL_SIZE, self.game_screen_batch, self.height)

        # TimeManagerクラスの呼び出し
        self.time_manager = TimeManager(self)

        # CustomerMageクラスの呼び出し
        self.customer_manager = CustomerManager(self, MAP_DATA, self.map)
        
        # SeatManagerクラスの呼び出し
        self.seat_manager = SeatManager(self, self.map)

        # CrowdManagerクラスの呼び出し
        self.crowd_manager = CrowdManager(self)

        # mainでデバッグを使う方法
        logger.debug("mainの初期化完了しました。")

        
        # Heroの操作用
        self.window.push_handlers(self)

        
        pyglet.clock.schedule_interval(self.update, 1/60)



    def on_draw(self):
        self.window.clear()
        self.game_screen_batch.draw()
        # self.crowd_manager.crowd_label.draw()


    def update(self, dt: float):
        self.customer_manager.update(dt)
        self.seat_manager.update(dt)
        # self.time_manager.update(dt)
        # self.crowd_manager.update(dt)
        
        

if __name__ == "__main__":
    game = Main()
    pyglet.app.run()
