import pyglet
import random
from setting import *
from loguru import logger


class SimpleMover:
    _id_counter = 0

    def __init__(self, start_pos, target_pos, state, map, batch):
        # =========================
        # 基本情報
        # =========================
        self.id = SimpleMover._id_counter # 顧客IDを割り当て
        SimpleMover._id_counter += 1 # 次の顧客IDのためにカウンターをインクリメント

        # 状態の初期化
        """
        状況の種類：
        - "outside": 店外（生成直後の状態）
        - "entering": 入口に向かっている状態 
        - "waiting": 待機エリアで待っている状態
        - "seating": 席に向かっている状態
        - "sitting": 席で過ごしている状態
        - "exiting": 出口に向かっている状態
        """
        self.state = state 
        self.map = map

        # グリッド座標（論理座標）
        self.grid_x, self.grid_y = start_pos
        self.target_x, self.target_y = target_pos

        # ピクセル座標（描画用）
        self.pixel_x = self.grid_x * CELL_SIZE
        self.pixel_y = self.grid_y * CELL_SIZE

        # =========================
        # スプライト
        # =========================
        chara_path = random.choice(self.map.chara_file)
        self.sprite_sheet = pyglet.image.load(chara_path)

        self.animations = self._create_animations()

        self.current_animation = "right"
        self.sprite = pyglet.sprite.Sprite(
            self.animations[self.current_animation],
            x=self.pixel_x,
            y=self.pixel_y,
            batch=batch
        )

        # =========================
        # 移動制御
        # =========================
        self.moving = False
        self.move_duration = 0.2
        self.move_timer = 0.0

        self.start_pixel = (self.pixel_x, self.pixel_y)
        self.dest_pixel = (self.pixel_x, self.pixel_y)

        # =========================
        # 状態
        # =========================
        self.reached = False
        self.stay_timer = 0.0
        self.STAY_DURATION = STAY_DURATION + random.randint(3, 10)
        self.has_reserved_seat = False  # 席予約フラグ


    # =========================
    # ターゲット設定
    # =========================
    def setup_new_target(self, x, y):
        self.target_x = x
        self.target_y = y


    # =========================
    # 更新
    # =========================
    def update(self, dt):
        self._move(dt)


    # =========================
    # 移動処理
    # =========================
    def _move(self, dt):
        if self.moving:
            self._update_moving(dt)
        else:
            self._start_next_step()


    def _update_moving(self, dt):
        self.move_timer += dt
        t = min(self.move_timer / self.move_duration, 1.0)

        sx, sy = self.start_pixel
        dx, dy = self.dest_pixel

        self._update_direction(sx, sy, dx, dy)

        self.pixel_x = sx + (dx - sx) * t
        self.pixel_y = sy + (dy - sy) * t

        self.sprite.x = self.pixel_x
        self.sprite.y = self.pixel_y

        if t >= 1.0:
            self.moving = False


    def _start_next_step(self):
        if (self.grid_x, self.grid_y) == (self.target_x, self.target_y):
            self.reached = True
            return

        dx = self.target_x - self.grid_x
        dy = self.target_y - self.grid_y

        if dx != 0:
            step_x = 1 if dx > 0 else -1
            new_x = self.grid_x + step_x
            new_y = self.grid_y
        else:
            step_y = 1 if dy > 0 else -1
            new_x = self.grid_x
            new_y = self.grid_y + step_y

        self._start_move_to(new_x, new_y)


    def _start_move_to(self, new_x, new_y):
        self.start_pixel = (self.pixel_x, self.pixel_y)
        self.dest_pixel = (new_x * CELL_SIZE, new_y * CELL_SIZE)

        self.grid_x = new_x
        self.grid_y = new_y

        self.move_timer = 0.0
        self.moving = True


    # =========================
    # 向き制御
    # =========================
    def _update_direction(self, sx, sy, dx, dy):
        if dx < sx:
            direction = "left"
        elif dx > sx:
            direction = "right"
        elif dy < sy:
            direction = "down"
        elif dy > sy:
            direction = "up"
        else:
            return

        if self.current_animation != direction:
            self.current_animation = direction
            self.sprite.image = self.animations[direction]


    # =========================
    # アニメーション生成
    # =========================
    def _create_animations(self):
        frames = []

        fw = self.sprite_sheet.width // 3
        fh = self.sprite_sheet.height // 4

        for row in range(4):
            for col in range(3):
                x = col * fw
                y = row * fh
                frame = self.sprite_sheet.get_region(x, y, fw, fh)
                frames.append(frame)


        return {
            "down": pyglet.image.Animation.from_image_sequence(frames[9:12], 0.1, True),
            "left": pyglet.image.Animation.from_image_sequence(frames[6:9], 0.1, True),
            "right": pyglet.image.Animation.from_image_sequence(frames[3:6], 0.1, True),
            "up": pyglet.image.Animation.from_image_sequence(frames[0:3], 0.1, True),
        }