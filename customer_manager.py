from setting import *
from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover
import random
import queue
from loguru import logger


class CustomerManager:
    def __init__(self, parent, map_data, map, num_customers=10):
        self.parent = parent

        self.batch = self.parent.batch

        # map_dataの取得
        self.map_data = map_data

        # mapクラスの呼び出し
        self.map = map

        # yの計算
        self.real_grid_y = len(self.map_data)

        self.general_area = self.parent.map.general_costomer_area
        
        # 初期顧客数
        self.num_customers_to_initialize = num_customers

        # mapのWの場所のリストを取得
        self.wait_queue = self.map.wait_queue
        # logger.debug(f"待機場所の座標{self.wait_queue}")

        # 入り口のキュー（エントランスと待合室のマックスの人数）
        self.max_entrance_buffer = len(self.wait_queue) + 1

        # 現在の入り口キューへの客入りの状況
        self.current_entrance_buffer = 0

        # 顧客の入口での管理のためのキュー
        # 1, 待機場所管理リスト
        self.wait_chair = [False for i in range(len(self.wait_queue))]
        # print(self.wait_chair)
        # 2, 顧客本体のリスト
        self.customers = []
        # 3, 顧客と待機場所の紐づけ
        self.waiting_queue = []

        # 待機場所が使われているかどうかのリスト
        self.wait_pos_in_use = [False] * len(self.wait_chair)
        # 新規顧客の生成
        self.spawn_timer = 0.0

        # # time_managerのよびだし
        # self.hours = self.parent.time_manager.hours
        
        # # [宿題]
        # タイマーの時間の取得
        # self.hours = self.parent.time_manager.hours
        # logger.info(f"時計の確認{self.hours}")

        # 顧客生成間隔（s）
        self.hours = 0
        self.result_crowd = 0
        self.crowd = CUSTOMER_CROWD
        self.spawn_interval = SPAWN_TIME # 5秒ごとに新しい顧客を生成
        # self.spawn_interval = 1

        # self.spawn_interval = self.customer_crowd() # 時間ごとに客の混み具合が違う


        # 生成される顧客数の上限
        self.max_customers = MAX_CUSTOMERS  # 任意：上限を設定したい場合
        # logger.debug(f"max_customer: {self.max_customers}")

        # 初期顧客
        self.setup_initial_customers()

        # 客のターゲット座標のリスト
        self.target_list = []

        self.count = 1

    # 初期顧客の生成
    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()
                
                


    def update(self, dt):
        # 入口まで割り当て
        self.assign_entrance()

        # 入口まで移動
        self.move_to_entrance(dt)

        # 待機場所への割り当て
        self.assign_wait_area()

        # 待機場所への移動
        self.moving_to_waiting_area(dt)

        # 客の削除
        self.delete_customer(dt)

        # 宿題
        # ループさせる
        # スポーンタイマーで客の更新
        self.spawn_timer += dt
        # # self.setup_initial_customers()
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            if len(self.customers) <= self.max_customers:
                
                self.hours = self.parent.time_manager.hours
                if self.customer_crowd():
                    self.spawn_interval = self.customer_crowd()
                self.spawn_customer()
                
                # if self.customer_crowd(self.hours):
                #     self.spawn_interval = self.customer_crowd(self.hours)
                logger.info(f"[生成時間の確認] 今の時間：{self.hours}, 生成間隔の時間: {self.spawn_interval}")
                
            else:
                pass
        else:
            pass


    # 顧客生成
    def spawn_customer(self):

        # general_area: 生成エリア　から取り出す
        random_G = random.choice(self.general_area) if self.general_area else None
        # マップのグリッドサイズの取得
        row_grid = len(self.map_data)
        
        x, y = random_G
        x, y = self.map.to_pyglet_x_y(x, y)

        grid = (x, y)

        # 状態を決める
        # 顧客生成(店外)
        state = "outside"

        # 生成する直後は動かないのでスタート位置とゴール位置を同じにする
        simple_mover = SimpleMover(grid, grid,
                                    state, self.map,
                                    batch=self.batch)
        logger.info(f"キャラID：{simple_mover.id}が生成されました。 state: {state}")
        

        # # そのインスタンスをリストの中にいれて管理する
        self.customers.append(simple_mover)

        # # [宿題]
        # # タイマーの時間の取得
        # self.hours = self.parent.time_manager.hours
        # logger.info(f"時計の確認{self.hours}")

        # # [客の混み具合の変更]
        # self.spawn_interval = self.customer_crowd() # 時間ごとに客の混み具合が違う







    # 入り口までアサインする（受付）
    def assign_entrance(self):
        for cu in self.customers:
            if cu.state == "outside":
                    x, y = self.map.entrance_pos
                    x, y = self.map.to_pyglet_x_y(x, y)
                    # y = self.real_grid_y - (y + 1)
                    cu.setup_new_target(x, y)
                    cu.state = "moving_to_entrance"
                    logger.info(f"[入り口にアサイン]キャラID：{cu.id} state: {cu.state}")

                    # logger.info(f"中の客の数(増える場合){self.inside_customer_num}")


    def move_to_entrance(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_entrance":
                cu.update(dt)
                if cu.reached:
                    cu.state = "arrive"
                    logger.info(f"[入り口に移動]キャラID：{cu.id} state: {cu.state}")
                    cu.reached = False




    def assign_wait_area(self):
        for cu in self.customers:
            if cu.state == "arrive":
                # 最も近い人を待機場所に割り当てる
                # logger.debug(f"{self.wait_chair}")
                for j, chaired in enumerate(self.wait_chair):
                    if not chaired:
                        self.wait_chair[j] = True
                        
                        # 紐付けようのリストに入れる
                        self.waiting_queue.append((cu, j))

                        x, y = self.wait_queue[j]
                        x, y = self.map.to_pyglet_x_y(x, y)

                        cu.state = "moving_to_wait" 
                        logger.info(f"[待機場所にアサイン]キャラID：{cu.id} state: {cu.state}")

                        # self.outside_customer_num -= 1        

                        break

                

    def moving_to_waiting_area(self, dt):
        for index, cu_waiting_queue in enumerate(self.waiting_queue):
            cu = cu_waiting_queue[0]
            # logger.debug(f"{cu.grid_x, cu.grid_y}")
            if cu.state == "moving_to_wait":
                x, y = (self.wait_queue[index])
                x, y = self.map.to_pyglet_x_y(x, y)
                cu.setup_new_target(x, y)
                cu.update(dt)

                if cu.reached:
                    if index == 0:
                        cu.state = "waiting_to_sit_to_seat"
                        # logger.info(f"[席に移動]キャラID：{cu.id} state: {cu.state}")

                        # cu.reached = False

                        # [宿題]
                        logger.info(f"【待機場所に到着】キャラID: {cu.id} pos: {cu.grid_x, cu.grid_y} \
                                        state: {cu.state}")
                    else:
                        cu.state = "waiting_for_top"
                    # else:
                    #     cu.state = "waiting_for_top"
                    cu.reached = False
                


    # 客が削除される
    def delete_customer(self, dt):
        for i, cu in enumerate(self.customers):
            # logger.info(f"state: {cu.state}")
            if cu.state == "exited":
                # logger.info(f"state: {cu.state}")
                # # そのインスタンスをリストの中にいれて管理する

                logger.info(f"[キャラの削除]キャラID：{cu.id} state: {cu.state}")
                
                # 明示的にスプライトを削除
                if hasattr(cu, 'sprite') and cu.sprite:
                    cu.sprite.delete()

                self.customers.pop(i)


    def chack_waiting(self):
        pass

    # 詰める処理
    def shift_waiting_customers_forward(self):
        for i in range(len(self.wait_chair)):
            if not self.wait_chair[i]:
                # 後の顧客を詰める
                for idx, (customer, current_i) in enumerate(self.waiting_queue):
                    # もし、紐付けられた座席が昇順の座席よりも大きい値ならば、一致させる
                    if current_i > i:
                        # idxにいる客をiに移動
                        self.waiting_queue[idx] = (customer, i)
                        # wait_chairのidxの座席をFalseにしてiをTrueにする
                        self.wait_chair[current_i] = False
                        self.wait_chair[i] = True
                        x, y = (self.wait_queue[i])
                        logger.info(f"[詰める] 客のid {customer.id}, 詰める処理のx,y {x, y}, state: {customer.state}")
                        customer.setup_new_target(17, 5)
                        customer.state = "moving_to_wait"

                        break
    
    # [宿題]
    # 時間ごとの顧客の生成間隔
    def customer_crowd(self):
        # if 0 <= hours < 2:
        #     result = 0.5
        # elif 2 <= hours < 8:
        #     result = 3
        # elif 8 <= hours < 10:
        #     result = 0.5
        # elif 10 <= hours < 13:
        #     result = 3
        # elif 13 <= hours < 15:
        #     result = 0.5
        # else:
        #     result = 3
        # return result
    
        for id, val in self.crowd.items():
            if id == self.hours:
                logger.info(f"index: {id}, 時間：{self.hours}")
                if val == "c":
                    self.result_crowd = 0.5
                elif val == "e":
                    self.result_crowd = 3
                logger.info(f"{id}時：{val}")
                print(id, val, self.hours, self.result_crowd)
                return self.result_crowd
            else:
                pass
            
            


        # for idx, val in CUSTOMER_CROWD.items():
        #     if hours == idx:
        #         logger.info(f"客の混み具合 {hours}時: 辞書の時間：{idx}, 客の生成間隔(s){val}")
        #         self.result_crowd = val
        #     else:
        #         break
        # return self.result_crowd

        # for idx, val in CUSTOMER_CROWD.items():
            #     return 
            # if val == EMPTY:
            #     logger.info(f"客の混み具合 {idx}時: 客の数{val}")
            #     return EMPTY
            # elif val == CROWD:
            #     logger.info(f"客の混み具合 {idx}時: 客の数{val}")
            #     return CROWD

