import pyglet
from setting import *
from loguru import logger


class CrowdManager:
    def __init__(self, parent):
        self.parent = parent

        self.crowd_count = self.parent.customer_manager.crowd_count


        # 混み具合の表示
        self.crowd_status = "空席"

        # 混み具合ラベルの位置の取得
        grid_x, grid_y = CROWD_GRID
        # x, y = grid_x, grid_y
        x, y = self.parent.map.to_pyglet_x_y(grid_x, grid_y)
        pixel_x = x * CELL_SIZE
        pixel_y = y * CELL_SIZE

        # 混み具合のラベルを作成
        self.crowd_label = pyglet.text.Label(str(self.crowd_status), font_name="Times New Roman", 
                                             font_size=20, x=pixel_x, y=pixel_y,
                                             anchor_y="bottom")
        
        
        
    def p_00(self):
        return "空席"
    
    def p_01(self):
        return "すこし空席"
    
    def p_02(self):
        return "満席"
    
    def p_run(self, num):
        # 混み具合を辞書にする
        # p_00: AVAILABLE, p_01: LIMITED_SEATING, p_02: FULL_CUSTOMER
        # self.croud_dict = {
        #         0: self.p_00,
        #         1: self.p_01,
        #         2: self.p_02
        #         }

        match num:
            case n if n <= AVAILABLE:
                return self.p_00()
            case n if AVAILABLE < n <= LIMITED_SEATING:
                return self.p_00()
            case n if LIMITED_SEATING < n <= FULL_CUSTOMER:
                return self.p_01()
            case n if FULL_CUSTOMER < n:
                return self.p_02()
            


    def update(self, dt):
        self.crowd_count = self.parent.customer_manager.crowd_count
        self.crowd_label.text = self.p_run(self.crowd_count)
        # logger.info(f"店内の客数：{self.crowd_count}")

    
    # # 混み具合の判定
    # def crowd_level(self):
    #     if self.crowd_count <= AVAILABLE: