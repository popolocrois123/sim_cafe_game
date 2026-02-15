import pyglet
from setting import *
from loguru import logger
import datetime
import time


class TimeManager:
    def __init__(self, parent, start_time):
        self.parent = parent

        self.start_time = start_time
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
        # self.count_time_hour = 0

        # 時計のラベルを作成
        self.timer_label = pyglet.text.Label(str(self.timer_time), font_name="Times New Roman", 
                                             font_size=20, x=pixel_x, y=pixel_y,
                                             anchor_y="bottom")
        
        # タイマーの呼び出し
        # pyglet.clock.schedule_interval(self.update, 10.0)

        self.end_time = time.time()
        self.difference = self.end_time - self.start_time
        self.count_time_hour = 0
        self.now_difference = 0
        self.timer_label.text = f"{self.hour}時"

        # 授業
        self.time_count = 0

        # self.difference = self.end_time - self.start_time
        
    def update(self, dt):
        # self.timer_label.text = f"dt: {int(dt * 60 * 60)}"
        self.time_count += int(dt * 60) * 10
        hours = self.time_count // 3600
        minutes =  (self.time_count % 3600) // 60

        self.timer_label.text = f"dt: {hours:02}:{minutes:02}"
        # 経過時間の計測
        # self.end_time = time.time()
        # self.difference = self.end_time - self.start_time
        # self.count_timer(self.difference)
        

        # logger.info(f"end_time: {self.end_time}")
        # self.difference = self.end_time - self.start_time
        # logger.info(f"now_difference: {self.now_difference}")
        # logger.info(f"difference: {self.difference}")
        # if int(self.difference) == 0:
        #     # self.count_time_hour = 0
        #     self.now_difference += 1
        #     self.count_timer(self.difference)
        # if int(self.now_difference) == int(self.difference):
        #     print("実行された", f"{int(self.now_difference)}", f"{int(self.difference)}")
        #     pass
        # else:
        #     self.count_time_hour = 0
        #     self.now_difference += 1
        #     self.count_timer(self.difference)

        # self.timer_time += dt
        # logger.info(f"dtの値{self.timer_time}")
        # if int(self.difference) % 5 == 0:
        #     self.count_time_hour = 0
        
        # self.change_clock(self.timer_time)
        # self.change_clock(dt, timer_time)
        # self.timer_label.text = self.change_clock(self.timer_time)
        # self.timer_label.text = str(int(self.timer_time))


    # 0時から23時までカウントして戻る、timer_labelを変更する関数
    def count_timer(self, difference):
        difference = difference
        self.timer_label.text = f"{int(difference)}時"
        # for t in range(0, 24, 1):
        # difference = difference
        # if difference_int % 5 == 0 and self.count_time_hour == 0:
        #     self.hour += 1
        #     self.count_time_hour += 1
        #     if self.hour >= 24:
        #         self.hour = self.hour % 24
        #     self.timer_label.text = f"{self.hour}時"
        # else:

        # difference = difference
        # if difference % 5 == 0:
        #     if self.count_time_hour == 0:
        #         self.hour += 1
        #         if self.hour >= 24:
        #             self.hour = self.hour % 24
        #         self.count_time_hour += 1
        #         self.timer_label.text = f"{self.hour}時"
        #     else:
        #         pass
        # else:
        #     pass
            

            # time.sleep(1)
    # # 秒数を時計形式に変換
    # def change_clock(self, timer_time):
    #     if int(self.timer_time) % 10 == 0 and self.current_hour != int(self.timer_time):
    #         if self.hour == 24:
    #             self.hour = 0
    #         else:
    #             self.hour += 1
    #         self.current_hour += 1
    #         self.timer_label.text = f"{self.hour}時"
    #     else:
    #         pass
        


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

        