import pyglet
from loguru import logger
from setting import *
import random

class SeatManager():
    def __init__(self, parent):
        self.parent = parent
        self.map = self.parent.map

        # 座標
        self.seat_positions = self.map.seat_positions

        # 席使用状況
        self.seat_in_use = [False for _ in range(len(self.seat_positions))]

        # 客
        self.customers = self.parent.customer_manager.customers

        # y補正
        self.real_grid_y = len(self.map.map_data)

        # 顧客の状態遷移フロー
        # "outside" → "moving_to_entrance" → "arrive" → "moving_to_wait" 
        # → "waiting_in_queue" → "waiting_to_sit_to_seat" → "moving_to_seat" 
        # → "seated" → "leaving" → "exited"
        # CustomerState = self.parent.customer_manager.customer_state

    def update(self, dt):
        self.assign_seat()
        self.move_to_seat(dt)
        self.eating(dt)
        self.move_to_exit(dt)
        self.view_crowd_result()


    # =========================
    # 席割り当て
    # =========================
    def assign_seat(self):
        for cu in self.customers:
            if cu.state == CustomerState.WAITING_TO_SIT_TO_SEAT and not cu.has_reserved_seat:

                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        # 席確保
                        self.seat_in_use[j] = True
                        cu.has_reserved_seat = True # 席を確保したフラグ
                        cu.seat_index = j

                        # 座標設定
                        x, y = self.seat_positions[j]
                        y = self.real_grid_y - (y + 1)

                        cu.setup_new_target(x, y)
                        cu.state = CustomerState.MOVING_TO_SEAT

                        logger.info(f"【席アサイン】id: {cu.id} seat:{j} state:{cu.state}")

                        # 待機列処理
                        for cu_value in self.parent.customer_manager.waiting_queue:
                            if cu in cu_value:
                                cu_number = cu_value[1]

                        self.parent.customer_manager.wait_chair[cu_number] = False

                        self.parent.customer_manager.waiting_queue = [
                            x for x in self.parent.customer_manager.waiting_queue if x[0] != cu
                        ]
                        # 待機列を前に詰める
                        self.parent.customer_manager.shift_waiting_customers_forward()

                        break


    # =========================
    # 移動（席へ）
    # =========================
    def move_to_seat(self, dt):
        for cu in self.customers:
            if cu.state == CustomerState.MOVING_TO_SEAT:
                cu.update(dt)

                if cu.reached:
                    cu.state = CustomerState.SEATED
                    cu.reached = False

                    logger.info(f"[着席] id:{cu.id}")


    # =========================
    # 食事
    # =========================
    def eating(self, dt):
        for cu in self.customers:
            if cu.state == CustomerState.SEATED:

                cu.stay_timer += dt

                # 向き制御（席番号ベース）
                seat_i = cu.seat_index
                if seat_i % 2 == 0:
                    direction = "right"
                else:
                    direction = "left"

                cu.current_animation = direction
                cu.sprite.image = cu.animations[direction]

                if cu.stay_timer >= cu.STAY_DURATION:
                    # 出口へ
                    x, y = self.map.exit_pos
                    y = self.real_grid_y - (y + 1)

                    cu.setup_new_target(x, y)
                    cu.state = CustomerState.LEAVING

                    logger.info(f"[退店開始] id:{cu.id}")

                    # 席解放
                    self.seat_in_use[cu.seat_index] = False
                    cu.has_reserved_seat = False
                    cu.seat_index = None


    # =========================
    # 出口へ
    # =========================
    def move_to_exit(self, dt):
        for cu in self.customers:
            if cu.state == CustomerState.LEAVING:
                cu.update(dt)

                if cu.reached:
                    cu.state = CustomerState.EXITED
                    logger.info(f"[退店完了] id:{cu.id}")


    # =========================
    # 統計
    # =========================
    def get_seat_in_use(self):
        return sum(self.seat_in_use)


    def view_crowd_result(self):
        use_total = self.get_seat_in_use() + self.parent.customer_manager.get_wait_chair_in_use()
        total = len(self.seat_positions) + len(self.parent.customer_manager.wait_chair)

        result = f"{int(use_total / total * 100)}%"
        self.parent.map.statistic_crowd.text = result