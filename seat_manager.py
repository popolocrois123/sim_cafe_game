import pyglet
from loguru import logger
from setting import *
import random

class SeatManager():
    def __init__(self, parent, map):
        self.parent = parent

        # mapデータの取得
        self.map = map

        # MAP上の座席の座標リスト
        self.seat_positions = self.map.seat_queue

        # 席管理のためのキュー
        # 1, 座席管理リスト
        self.seat_in_use = [False for i in range(len(self.seat_positions))]
        # 2, カスタマーのリストを取得
        self.customers = self.parent.customer_manager.customers
        for cu in self.customers:
            logger.debug(f"{cu.reached}")
        # 3, 顧客と座席の紐づけ
        self.seat_queue = []

        # print(self.seat_in_use)

        # yの計算
        self.real_grid_y = len(self.map.map_data)

        # 席について食べているか、動き始めるかの判定
        self.start_to_exit = False

        self.count_seated = 0

        # --- 統計情報 ---
        # 席についている客の数を数える、空き率の計算のため
        self.s_chair = 0

       



        


    def update(self, dt):
        # 客を席にセット
        self.assign_seat()

        # # 客を席に移動
        self.move_to_seat(dt)

        # 客がごはんを食べる
        self.eating(dt)

        # 客が出口まで移動する
        self.move_to_exit(dt)

        # 統計情報の更新
        # 空き率の計算
        seat_crowd_rate = (self.s_chair / len(self.parent.map.seat_queue)) * 100
        
        # --------
        # --- map の変更 ---
        # map.pyのC 席の混み率の変更
        try:
            self.parent.map.statistic_crowd.text = f"席の混み率： {int(seat_crowd_rate)}%"
        except AttributeError:
            pass
        # map.py のA客数の変更
        # AとDについて
        # 客数の再計算
        self.wait_chair_call()
        
        try:
            self.parent.map.statistic_customer.text = f"客数： {int(self.true_sum_wait_chair)}人"
        except AttributeError:
            pass
        try:
            self.parent.map.statistic_wait_chair.text = f"席待機占有率： {int(self.true_rate_w_s)}%"
        except AttributeError:
            pass



        


    def assign_seat(self):
        for cu in self.customers:
            if cu.state == "waiting_to_sit_to_seat":
                # # 最も近い人を待機場所に割り当てる
                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        self.seat_in_use[j] = True
                        x, y = self.seat_positions[j]
                        y = self.real_grid_y - (y + 1)
                        cu.setup_new_target(x, y)
                        cu.state = "moving_to_seat"
                        logger.info(f"【席にアサイン】id: {cu.id} state: {cu.state}")
                        self.seat_queue.append((cu, j))
                        
                        
                        # cuからwaiting_queueのcuに連結された番号を取り出す
                        for cu_value in self.parent.customer_manager.waiting_queue:
                            if cu in cu_value:
                                cu_number = cu_value[1]

                        # 番号に該当するwait_chairをFalseにすることで席を空席にする
                        self.parent.customer_manager.wait_chair[cu_number] = False

                        # waiting_queueからcuを取り出す 
                        self.parent.customer_manager.waiting_queue = [x for x in self.parent.customer_manager.waiting_queue if x[0] != cu]

                        # logger.debug(f"wait_queue: {self.parent.customer_manager.wait_queue}")

                        self.parent.customer_manager.current_entrance_buffer -= 1

                        # 詰める処理[宿題]
                        self.parent.customer_manager.shift_waiting_customers_forward()
                        
                        break

        



    def move_to_seat(self, dt):
        self.count_seated = 0
        for cu in self.customers:
            if cu.state == "moving_to_seat":
                cu.update(dt)
                if cu.reached:
                    cu.state = "seated"
                    logger.info(f"[席に移動]キャラID：{cu.id} state: {cu.state}")

                    cu.reached = False
                    # 統計情報    
                    # 席についている客の数
                    self.s_chair += 1

    def eating(self, dt):
        for cu in self.customers:
            if cu.state == "seated":

                self.STAY_DURATION = cu.STAY_DURATION
                cu.stay_timer += dt

                for idx, cu_seatnum in enumerate(self.seat_queue):
                    if cu in cu_seatnum:
                        if cu_seatnum[1] % 2 == 0:
                            direction = "right"
                        elif cu_seatnum[1] % 2 == 1:
                            direction = "left"
                        else:
                            direction ="down"
                        
                        cu.current_animation = direction
                        cu.sprite.image = cu.animation_frames[direction]

                # logger.info(f"【食事時間] キャラID：{cu.id} stay_timer: {cu.stay_timer}") 

                if cu.stay_timer >= self.STAY_DURATION:
                    x, y = self.map.exit_pos
                    y = self.real_grid_y - (y + 1)
                    cu.setup_new_target(x, y)

                    cu.state = "leaving"

                    logger.info(f"[出口にアサイン]キャラID：{cu.id} state: {cu.state}")
                    # 統計情報
                    self.s_chair -= 1

                    # 座席の解放
                    for idx, (cust_obj, seat_i) in enumerate(self.seat_queue):
                        if cust_obj == cu:
                            self.seat_in_use[seat_i] = False
                            self.seat_queue.pop(idx)
 



    def move_to_exit(self, dt):
        for cu in self.customers:
            if cu.state == "leaving":
                cu.update(dt)
                if cu.reached:
                    cu.state = "exited"
                    logger.info(f"[出口に移動]キャラID：{cu.id} state: {cu.state}")
                    

                    


    # [宿題]
    # 店にいる客数や席と待機場所の占有率について
        # 座席と待機場所の呼び出し
    def wait_chair_call(self):
        # customer_managerより待機場所の管理リストwait_chairを取得
        self.wait_chair = self.parent.customer_manager.wait_chair

        # 1, 待機場所のtrueの数を取得
        self.true_wait_chair = self.wait_chair.count(True)
        # 2, 席のtrueの数を取得
        self.true_seat_in_use = self.seat_in_use.count(True)
        # true状態の人数の加算
        self.true_sum_wait_chair = self.true_seat_in_use + self.true_wait_chair

        # マップに指定された待機場所の数を取得
        self.W_count = sum(w.count("W") for w in MAP_DATA)
        # マップに指定された席の数を取得
        self.S_count = sum(s.count("S") for s in MAP_DATA)
        # 3, 二つを加算する
        self.sum_w_s_count = self.W_count + self.S_count

        # 占有率の計算
        self.true_rate_w_s = self.true_sum_wait_chair / self.sum_w_s_count * 100


    