import pyglet
from setting import *
import random

class Customer:
    def __init__(self, start_pos, state, window_height, cell_size, color, batch):
        # 初期グリッド
        self.grid_x, self.grid_y = start_pos
        # ターゲットグリッド
        self.target_pos_x, self.target_pos_y = start_pos
        self.cell_size = cell_size
        self.window_height = window_height
        self.state = state
        self.color = color

        # 経過時間
        self.elapsed_time = 0
        
        # 客の画像
        self.sprite = pyglet.shapes.Rectangle(
            x=self.initial_x * CELL_SIZE,
            y=self.window_height - (self.initial_y + 1) * CELL_SIZE,
            width=CELL_SIZE,
            height=CELL_SIZE,
            color=self.color,
            batch=batch
        )

        # 移動用変数
        self.moving = False
        self.move_duration = 0.2
        self.move_timer = 0.0/8
        self.start_pixel = (self.sprite.x, self.sprite.y)

    def start_moving_to(self, new_x, new_y):
        self.start_grid = (self.grid_x, self.grid_y)
        self.target_grid = (new_x, new_y)
        self.start_pixel = (self.sprite.x, self.sprite.y)
        self.dest_pixel = (
        new_x * self.cell_size,
        self.window_height - (new_y + 1) * self.cell_size
        )

        dx = new_x - self.grid_x
        dy = new_y - self.grid_y

        self.move_timer = 0.0
        self.moving = True

        
    def move_target(self, game_map, dt):
        if self.moving:
            self.move_timer += dt
            t = min(self.move_timer / self.move_duration, 1.0)
            sx, sy = self.start_pixel
            dx, dy = self.dest_pixel
            
            # Rectangleの位置を更新
            self.sprite.x = sx + (dx - sx) * t
            self.sprite.y = sy + (dy - sy) * t

            if t >= 1.0:
                self.moving = False
                self.grid_x, self.grid_y = self.target_grid
                
        else:
            if self.grid_x != self.target_pos_x:
                step_x = 1 if self.target_pos_x > self.grid_x else -1
                next_x = self.grid_x + step_x
                if game_map.is_walkable(next_x, self.grid_y):
                    self.start_moving_to(next_x, self.grid_y)
                    return

            if self.grid_y != self.target_pos_y:
                step_y = 1 if self.target_pos_y > self.grid_y else -1
                next_y = self.grid_y + step_y
                if game_map.is_walkable(self.grid_x, next_y):
                    self.start_moving_to(self.grid_x, next_y)

    def update(self, dt, game_map):
        self.move_target(game_map, dt)



        



        
    




