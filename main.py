import pyglet
from map import Map
from setting import *
from customer_manager import CustomerManager
from seat_manager import SeatManager
from loguru import logger


# メインクラス
class Main():
    def __init__(self):
        # ログ設定
        logger.remove()
        logger.add("log_state.log", level="INFO", 
                   filter=lambda record: record["level"].name in ["INFO"],
                   encoding="utf-8")

        # ウィンドウの幅と高さ
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT


        # windowの設定
        self.window = pyglet.window.Window(width=self.width, height=self.height,
                                            caption=WINDOW_TITLE, resizable=True)
        self.window.set_location(CENTER_X, CENTER_Y) # パソコンの幅から中央にウィンドウをセットする
        self.window.set_minimum_size(width=500, height=500) # 最小サイズの設定
        
        # ゲームスクリーン用のバッチの作成
        self.game_screen_batch = pyglet.graphics.Batch()

        # 背景のmapクラスの呼び出し
        self.map = Map(self)

        # CustomerMageクラスの呼び出し
        self.customer_manager = CustomerManager(self)
        
        # SeatManagerクラスの呼び出し
        self.seat_manager = SeatManager(self)

        
        pyglet.clock.schedule_interval(self.update, 1/FPS)



    def on_draw(self):
        self.window.clear()
        self.game_screen_batch.draw()


    def update(self, dt: float):
        self.customer_manager.update(dt)
        self.seat_manager.update(dt)
        
        

if __name__ == "__main__":
    game = Main()
    pyglet.app.run()
