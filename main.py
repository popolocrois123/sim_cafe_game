import pyglet
from map import Map
from setting import *
from customer_manager import CustomerManager
from seat_manager import SeatManager
from loguru import logger
from pyglet.window import key


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
        
        # 更新の切り替えのためのフラグ
        self.is_paused = False

        # on_draw()を実行するためのイベントハンドラーをウィンドウに登録
        # selfでもできるけど入れた方が明示的でわかりやすいと思う
        self.window.push_handlers(self.on_draw, self.on_key_press)

        # ゲームスクリーン用のバッチの作成
        self.game_screen_batch = pyglet.graphics.Batch()

        # 背景のmapクラスの生成
        self.map = Map(self)

        # CustomerMageクラスの生成
        self.customer_manager = CustomerManager(self)
        
        # SeatManagerクラスの生成
        self.seat_manager = SeatManager(self)

        
        pyglet.clock.schedule_interval(self.update, 1/FPS)



    def on_draw(self):
        self.window.clear()
        self.game_screen_batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            self.is_paused = not self.is_paused
            # logger.info(f"キーが押されました: {symbol}")


    def update(self, dt: float):
        if self.is_paused:
            return # ゲームが一時停止中の場合は更新をスキップ
        self.customer_manager.update(dt)
        self.seat_manager.update(dt)
   

if __name__ == "__main__":
    game = Main()
    pyglet.app.run()
