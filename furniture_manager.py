from setting import *
from customer import Customer
import pyglet
from simple_mover import SimpleMover
import random
import queue
from loguru import logger

class FurnitureManager:
    def __init__(self, parent):
        self.parent = parent
        
        # 机
        # self.table = pyglet.resource.image("table.png")

        # 椅子