from setting import *
from customer import Customer
from simple_mover import SimpleMover
import random
import pyglet
from loguru import logger

# 顧客管理クラス
class CustomerManager:
    # 顧客の生成と管理を担当
    def __init__(self, parent, map_data, map, num_customers=10):
        self.parent = parent
        self.map = map
        self.map_data = map_data

        self.batch = self.parent.game_screen_batch

        # 座標
        self.general_area = self.map.spawn_area # 顧客が生成されるエリアの座標リスト
        self.wait_positions = self.map.wait_queue # 待機列の座標

        # 管理
        self.customers = [] # 店内に存在する顧客のリスト
        self.wait_chair = [False] * len(self.wait_positions) # 待機椅子の使用状況
        self.waiting_queue = [] # 待機列 [(Customer, 待機位置インデックス), ...]
        self.current_entrance_buffer = 0

        # 制御
        self.max_customers = MAX_CUSTOMERS # 店内に同時に存在できる顧客の最大数（待機も含む）
        self.spawn_interval = SPAWN_TIME # 顧客生成の基本間隔（秒）初期設定
        self.spawn_timer = 0.0 # 顧客生成のタイマー

        # 時間
        self.hours = 0 # 時間帯（0-23）# 時間帯の初期値
        self.time_count = 0 # 時間計測用のカウンター

        # 生成
        self.num_customers_to_initialize = num_customers
        self.setup_initial_customers()


    # =========================
    # 初期生成
    # =========================
    def setup_initial_customers(self):
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()


    # =========================
    # メイン更新
    # =========================
    def update(self, dt):
        self.handle_spawn(dt)
        self.handle_entrance()
        self.move_to_entrance(dt)
        self.handle_wait_move(dt)
        self.handle_waiting(dt)
        self.handle_deletion()
        # self.shift_waiting_customers_forward()

        self.update_time(dt)


    # =========================
    # 生成
    # =========================
    # self.hourの時間によって生成間隔を変更する
    def handle_spawn_control(self):
        SPAWN_TIME = get_spawn_time(self.hours)
        # logger.info(f"生成制御：hour={self.hours}, spawn_time={SPAWN_TIME}")
        return SPAWN_TIME


    def handle_spawn(self, dt):
        self.spawn_timer += dt
        # 生成制御の更新
        SPAWN_TIME = self.handle_spawn_control()
        self.spawn_interval = SPAWN_TIME

        # 一定時間経過していない場合は生成しない
        if self.spawn_timer < self.spawn_interval:
            return

        self.spawn_timer = 0.0 # タイマーをリセット
        # 店内の顧客数が最大数を超えている場合は生成しない
        if len(self.customers) >= self.max_customers:
            return

        self.spawn_customer()

        logger.info(f"生成：hour={self.hours}, interval={self.spawn_interval}")

    # =========================
    # 顧客生成 
    # =========================
    def spawn_customer(self):
        if not self.general_area:
            return
        # 生成位置をランダムに選択
        x, y = random.choice(self.general_area)
        # 生成位置をピクセル座標に変換
        x, y = self.map.to_pyglet_x_y(x, y)

        # 顧客を生成して管理リストに追加
        mover = SimpleMover((x, y), (x, y),
                            "outside",
                            self.map,
                            batch=self.batch)
        # 顧客の状態を初期化
        self.customers.append(mover)

        logger.info(f"生成 id={mover.id}, state={mover.state}")


    # =========================
    # 入口処理
    # =========================
    # 入口に向かう顧客を制御
    def handle_entrance(self):
        for cu in self.customers:
            if cu.state != "outside":
                continue

            x, y = self.map.to_pyglet_x_y(*self.map.entrance_pos)
            cu.setup_new_target(x, y)

            logger.info(f"生成 id={cu.id}, state={cu.state}")

            cu.state = "moving_to_entrance"

    # =========================
    # 入口に向かう顧客の移動
    # =========================
    def move_to_entrance(self, dt):
        for cu in self.customers:
            if cu.state != "moving_to_entrance":
                continue

            cu.update(dt)
            logger.info(f"生成 id={cu.id}, state={cu.state}")


            if cu.reached:
                cu.state = "arrive"
                cu.reached = False


    # =========================
    # 待機
    # =========================
    def handle_wait_move(self, dt):
        for cu in self.customers:
            if cu.state != "arrive":
                continue

            self.assign_wait_slot(cu)

    # =========================
    # 待機列の移動
    # =========================
    def assign_wait_slot(self, cu):
        for i, occupied in enumerate(self.wait_chair):
            if occupied:
                continue

            self.wait_chair[i] = True
            # 待機列に追加
            self.waiting_queue.append((cu, i))
            # 待機位置に移動
            x, y = self.map.to_pyglet_x_y(*self.wait_positions[i])
            cu.setup_new_target(x, y)

            logger.info(f"生成 id={cu.id}, state={cu.state}")


            cu.state = "moving_to_wait"
            logger.info(f"待機アサイン id={cu.id}")
            break

    # =========================
    # 待機列の移動と状態更新
    # =========================
    def handle_waiting(self, dt):
        for num, (cu, idx) in enumerate(self.waiting_queue):

            if cu.state != "moving_to_wait":
                continue

            x, y = self.map.to_pyglet_x_y(*self.wait_positions[idx])
            cu.setup_new_target(x, y)
            cu.update(dt)

            logger.info(f"[待機列の移動] 客のid {cu.id}, target: {(x, y)}, state: {cu.state}")

            if not cu.reached:
                continue

            cu.reached = False
            # 待機位置に到達したら全員「待機状態」に統一
            cu.state = "waiting_in_queue"
            # 最前列だけ「席へ移動する状態」にする
            if num == 0:
                cu.state = "waiting_to_sit_to_seat"

    # =========================
    # 待機列を前に詰める
    # =========================
    def shift_waiting_customers_forward(self):
        for i in range(len(self.wait_chair)):
            if not self.wait_chair[i]:

                for idx, (cu, current_i) in enumerate(self.waiting_queue):
                    # 後ろにいる客を前へ詰める
                    if current_i > i:
                        # 元の位置を空ける
                        self.wait_chair[current_i] = False

                        # 新しい位置を埋める
                        self.wait_chair[i] = True

                        # waiting_queue を更新
                        self.waiting_queue[idx] = (cu, i)

                        # 目的地を更新（wait_queueを使用）
                        x, y = self.map.wait_queue[i]

                        logger.info(f"[詰める] 客のid {cu.id}, target: {(x, y)}, state: {cu.state}")

                        # 移動指示
                        cu.setup_new_target(x, y)
                        # 最前列だけ「席へ移動する状態」にする
                        if i == 0:
                            cu.state = "waiting_to_sit_to_seat"
                            logger.info(f"【最前列】id:{cu.id} state:{cu.state}")


                        break
    # def shift_waiting_customers_forward(self):
    #     """待機列の顧客を前に詰める"""
    #     # 待機列が空の場合は何もしない
    #     if not self.waiting_queue:
    #         return

    #     # 待機列の顧客を前から順に再配置
    #     new_waiting_queue = []

    #     # 待機列の最前列（一番下）のインデックス
    #     front_y = self.wait_positions[0][1] # 待機列の最前列のy座標を取得(この場合13)
        
    #     for i, (cu, waiting_idx) in enumerate(self.waiting_queue):
    #         # 待機位置のインデックスを更新
    #         new_idx = self.wait_positions[waiting_idx][1] - 1 # 待機列のy座標を1つ前に詰める
    #         logger.info(f"待機列移動前: id={cu.id}, new_idx={new_idx}")
    #         # ターゲット位置を設定
    #         x, y = self.map.to_pyglet_x_y(*self.wait_positions[new_idx])
    #         cu.setup_new_target(x, y)

    #         # 客が待機場所の最前列（一番下）にいる場合のみ座席移動を開始する
    #         if waiting_idx == front_y:
    #             cu.state = "waiting_to_sit_to_seat"
    #         # else: 既に "waiting_in_queue" 状態のため変更不要

    #         new_waiting_queue.append((cu, new_idx))

    #     self.waiting_queue = new_waiting_queue

    # =========================
    # 削除
    # =========================
    def handle_deletion(self):
        for cu in self.customers[:]:
            if cu.state != "exited":
                continue

            if hasattr(cu, "sprite") and cu.sprite:
                cu.sprite.delete()

            self.customers.remove(cu)


    # =========================
    # 混雑制御
    # =========================
    def customer_crowd(self):
        for h, val in CUSTOMER_CROWD.items():
            if h != self.hours:
                continue

            if val == "c":
                return CROWD_GENERATE
            elif val == "e":
                return EMPTY_GENERATE

        return None


    # =========================
    # 時間
    # =========================
    def update_time(self, dt):
        self.time_count += int(dt * 60) * 10

        self.hours = self.time_count // 3600
        self.hours %= 24

        minutes = (self.time_count % 3600) // 60

        try:
            self.parent.map.statistic_time.text = f"時刻 {self.hours:02}:{minutes:02}"
        except AttributeError:
            pass


    # =========================
    # ユーティリティ
    # =========================
    def get_wait_chair_in_use(self):
        return sum(self.wait_chair)