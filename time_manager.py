import pyglet
from setting import *
from loguru import logger

class TimeManager:
    def __init__(self, parent):
        self.parent = parent
        # 時計ラベルの位置の取得
        grid_x, grid_y = TIMER_GRID
        # x, y = grid_x, grid_y
        x, y = self.parent.map.to_pyglet_x_y(grid_x, grid_y)
        pixel_x = x * CELL_SIZE
        pixel_y = y * CELL_SIZE

        self.timer_time = 0.0
        # 時計の表示時間
        self.clock = "00時"
        # 0時から24時までの時間計算用
        self.hour = 0
        # 今のdtの時間を判別する
        self.current_hour = 0

        # 時計のラベルを作成
        self.timer_label = pyglet.text.Label(str(self.timer_time), font_name="Times New Roman", 
                                             font_size=20, x=pixel_x, y=pixel_y,
                                             anchor_y="bottom")
        
        # タイマーの呼び出し
        pyglet.clock.schedule_interval(self.update, 10.0)
        
    def update(self, dt):
        self.timer_time += dt
        logger.info(f"dtの値{self.timer_time}")
        self.change_clock(self.timer_time)
        # self.change_clock(dt, timer_time)
        # self.timer_label.text = self.change_clock(self.timer_time)
        # self.timer_label.text = str(int(self.timer_time))

    # 秒数を時計形式に変換
    def change_clock(self, timer_time):
        if int(self.timer_time) % 10 == 0 and self.current_hour != int(self.timer_time):
            if self.hour == 24:
                self.hour = 0
            else:
                self.hour += 1
            self.current_hour += 1
            self.timer_label.text = f"{self.hour}時"
        else:
            pass
        


        # # if int(timer_time) % 10 == 0:
        #     if self.hour == 24:
        #         self.hour = 0
        #     else:
        #         self.hour += 1
        # # else:
        #     pass
        # return f"{self.hour}時"

            
        # if self.hour == 24:
        #     self.hour = 0
        # else:
        #     self.hour += 1
        # return f"{self.hour}時"

        