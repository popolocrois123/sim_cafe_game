import pyglet
from loguru import logger
from setting import *

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



    def update(self, dt):
        # 客を席にセット
        self.assign_seat()

        # # 客を席に移動
        self.move_to_seat(dt)

        # 客がごはんを食べる
        self.eating(dt)

        # 客が出口まで移動する
        self.move_to_exit(dt)


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

                        # 最初の席を埋まっていない
                        # self.parent.customer_manager.wait_pos_in_use[0] = False

                        # 待機場所管理リストの変更
                        # self.parent.customer_manager.wait_chair[0] = False

                        # 詰める処理[宿題]
                        self.parent.customer_manager.shift_waiting_customers_forward()
                        
                        # 案内されたら色を変える　青に
                        # cu.sprite.color=(150, 125, 255)
                        # self.parent.customer_manager.inside_customer_num -= 1
 

                        break
                # pass

        



    def move_to_seat(self, dt):
        self.count_seated = 0
        for cu in self.customers:
            if cu.state == "moving_to_seat":
                cu.update(dt)
                if cu.reached:
                    cu.state = "seated"
                    logger.info(f"[席に移動]キャラID：{cu.id} state: {cu.state}")

                    cu.reached = False
                # cu.state = "seated"
                
    

    def eating(self, dt):
        for cu in self.customers:
            if cu.state == "seated":
                cu.stay_timer += dt
                # [宿題]食べている間向きの変更をする
                # for idx, i in enumerate(self.map.table_queue):
                #     logger.debug(f"テーブルの座標{self.map.table_queue}")
                #     if cu.grid_y in i and (cu.grid_x+1) in i:
                #         direction = "right"
                        
                #     elif cu.grid_y in i and (cu.grid_x-1) in i:
                #         direction = "left"

                #     else:
                #         direction = "down"
                #         logger.debug(f"キャラの座標{(cu.grid_x, cu.grid_y)}")

                    
                    # cu.current_animation = direction
                    # cu.sprite.image = cu.animation_frames[direction]
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


                if cu.stay_timer >= STAY_DURATION:
                    x, y = self.map.exit_pos
                    y = self.real_grid_y - (y + 1)
                    cu.setup_new_target(x, y)
                    # [宿題]色を変える: 緑に
                    # cu.sprite.color=(0, 255, 0)

                    # [宿題]　キャラの向きを机の方向にする
                    # if cu.sprite.x == 2:
                    # cu.current_animation = "left"
                    # cu.sprite.image = self.animation_frames["left"]

                    cu.state = "leaving"
                    logger.info(f"[出口にアサイン]キャラID：{cu.id} state: {cu.state}")


                    # 変更
                    self.parent.customer_manager.inside_customer_num -= 1

                    

                    # 座席の解放
                    for idx, (cust_obj, seat_i) in enumerate(self.seat_queue):
                        if cust_obj == cu:
                            self.seat_in_use[seat_i] = False
                            self.seat_queue.pop(idx)
                            # logger.info(f"【座席解放】id: {cu.id} seat: [{seat_i}]") 
 



    def move_to_exit(self, dt):
        for cu in self.customers:
            if cu.state == "leaving":
                cu.update(dt)
                if cu.reached:
                    cu.state = "exited"
                    logger.info(f"[出口に移動]キャラID：{cu.id} state: {cu.state}")

                    





    