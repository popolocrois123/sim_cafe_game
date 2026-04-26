import pyglet
from loguru import logger
import glob
from setting import *


# =========================
# マップクラス
# =========================
class Map():
    def __init__(self, parent):
        self.parent = parent
        self.map_data = MAP_DATA
        self.cell_size = CELL_SIZE
        self.batch = parent.game_screen_batch
        self.height = parent.height

        #=========================
        # マップ構造
        #=========================

        self.tiles = [] # 描画用のタイルやスプライトを保存するリスト

        self.wait_queue = [] # 待機エリアのグリッド座標を保存するリスト
        self.seat_positions = [] # 席のグリッド座標を保存するリスト
        self.table_positions = [] # テーブルのグリッド座標を保存するリスト
        self.spawn_area = [] # 顧客の出現エリアのグリッド座標を保存するリスト

        self.entrance_pos = None # 入口のグリッド座標
        self.exit_pos = None # 出口のグリッド座標

        self.s_time = 0.0 # 混雑率計算用の時間計測開始点
        self.rate_crowd = 0.0 # 混雑率計算用の混雑率保存変数

        self.statistic_time = None # 時刻表示用のラベル（初期化後に設定される）
        self.statistic_crowd = None # 混雑率表示用のラベル（初期化後に設定される）
        self.statistic_customer = None # 客数表示用のラベル（初期化後に設定される）
        self.statistic_wait_chair = None # 席待機占有率表示用のラベル（初期化後に設定される）

        # マップ解析と初期描画
        self._parse_map()

        # 待機エリアは後ろから埋まっていくようにするため、待機エリアのリストを逆順にしておく
        self.wait_queue.reverse()
        # キャラクターファイルのリストを取得
        self.chara_file = glob.glob("./characters/*")
        # print("Map")


    # =========================
    # マップ解析
    # =========================
    def _parse_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                px, py = self._to_pixel(x, y)
                tile_type = TILE_MAP.get(cell, FLOOR)

                if tile_type == WALL:
                    self._create_wall(px, py)
                elif tile_type == FLOOR:
                    continue
                elif tile_type == SPAWN:
                    self.spawn_area.append((x, y))
                elif tile_type == SPAWN_EDGE:
                    self._draw_rect(px, py, (0, 255, 255))
                elif tile_type == ENTRANCE:
                    self.entrance_pos = (x, y)
                elif tile_type == EXIT:
                    self.exit_pos = (x, y)
                elif tile_type == WAIT:
                    self._create_wait_area(px, py)
                    self.wait_queue.append((x, y))
                elif tile_type == TABLE:
                    self._create_table(px, py)
                    self.table_positions.append((x, y))
                elif tile_type == SEAT:
                    self._create_chair(px, py, x)
                    self.seat_positions.append((x, y))
                # INFOラベル系
                elif tile_type == TIME_LABEL:
                    self._create_time_label(px, py)
                elif tile_type == CROWD_LABEL:
                    self._create_crowd_label(px, py)
                elif tile_type == CUSTOMER_LABEL:
                    self._create_customer_label(px, py)
                elif tile_type == WAIT_LABEL:
                    self._create_wait_label(px, py)

    # =========================
    # 描画ユーティリティ
    # =========================
    def _draw_rect(self, px, py, color):
        rect = pyglet.shapes.Rectangle(px, py, self.cell_size, self.cell_size, color=color, batch=self.batch)
        # print(rect.batch)
        self.tiles.append(rect)

    def _to_pixel(self, x, y):
        return x * self.cell_size, (len(self.map_data) - (y + 1)) * self.cell_size

    # =========================
    # 各タイル描画関数
    # =========================
    def _create_wall(self, px, py):
        self._draw_rect(px, py, (64, 64, 64))

    def _create_wait_area(self, px, py):
        self._draw_rect(px, py, (0, 0, 255))

    def _create_table(self, px, py):
        img = pyglet.resource.image("table.png")
        sprite = pyglet.sprite.Sprite(img, px, py - 10, batch=self.batch)
        sprite.scale_x = 0.08
        sprite.scale_y = 0.11
        self.tiles.append(sprite)

    def _create_chair(self, px, py, x):
        img = pyglet.resource.image("chair.png")
        sprite = pyglet.sprite.Sprite(img, px, py - 20, batch=self.batch)
        sprite.scale_y = 0.11
        sprite.scale_x = -0.08 if x in (2, 6) else 0.08
        if x in (2, 6): sprite.x += sprite.width
        self.tiles.append(sprite)

    # =========================
    # INFOラベル生成
    # =========================
    def _create_time_label(self, px, py):
        self.statistic_time = self._create_label("時刻：0", px, py)

    def _create_crowd_label(self, px, py):
        self.statistic_crowd = self._create_label("席の混み率：0%", px, py)

    def _create_customer_label(self, px, py):
        self.statistic_customer = self._create_label("客数：0人", px, py)

    def _create_wait_label(self, px, py):
        self.statistic_wait_chair = self._create_label("席待機占有率：0%", px, py)

    def _create_label(self, text, px, py):
        label = pyglet.text.Label(text, font_name="Times New Roman", font_size=20, x=px, y=py + 5, batch=self.batch)
        self.tiles.append(label)
        return label

    # =========================
    # ユーティリティ
    # =========================
    def is_walkable(self, x, y):
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            tile_type = TILE_MAP.get(self.map_data[y][x], FLOOR)
            return tile_type != WALL
        return False

    def to_pyglet_x_y(self, x, y):
        return x, len(self.map_data) - y - 1



# =========================
# 背景
# =========================
class Background():
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch

        img = pyglet.image.load('map_sample.png')
        self.sprite = pyglet.sprite.Sprite(img, x=0, y=0, batch=self.batch)

        self.sprite.scale_x = window.width / img.width
        self.sprite.scale_y = window.height / img.height