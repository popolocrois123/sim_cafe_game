import pyglet
from setting import *
from loguru import logger
import datetime
import time


class TimeManager:
    def __init__(self, parent):
        self.parent = parent

        self.hours = 0

    
        # 授業
        self.time_count = 0
        
    def update(self, dt):
        self.time_count += int(dt * 60) * 10
        self.hours = self.time_count // 3600
        if self.hours > 23:
            self.hours = self.hours % 24
        minutes =  (self.time_count % 3600) // 60

        try:
            self.parent.map.statistic_time.text = f"時刻 {self.hours:02}:{minutes:02}"
        except AttributeError:
            pass