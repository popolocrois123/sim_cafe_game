import pyglet
from setting import *
from loguru import logger
import datetime
import time


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
        self.hours = 0

        # 時計のラベルを作成
        self.timer_label = pyglet.text.Label(str(self.timer_time), font_name="Times New Roman", 
                                             font_size=20, x=pixel_x, y=pixel_y,
                                             anchor_y="bottom")
    

        # 授業
        self.time_count = 0
        
    def update(self, dt):
        self.time_count += int(dt * 60) * 10
        self.hours = self.time_count // 3600
        if self.hours > 23:
            self.hours = self.hours % 24
        minutes =  (self.time_count % 3600) // 60

        self.timer_label.text = f"タイマー {self.hours:02}:{minutes:02}"
