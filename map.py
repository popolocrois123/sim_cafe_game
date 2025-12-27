import pyglet
import queue
from loguru import logger


class Map():
    def __init__(self, map_data, cell_size, batch, height):
        self.map_data = map_data
        self.cell_size = cell_size
        self.batch = batch
        self.height = height


        self.tiles = []
        # 通れないブロックのリスト
        self.block_tiles = ["B", "T"]

        # 待機場所ｗの数
        self.w_count = self.map_data.count("W")

        # 待機場所のキュー作成
        # self.wait_queue = queue.Queue(self.w_count)
        self.wait_queue = []

        # 席のキュー
        self.seat_queue = []

        # [宿題]机のキュー
        self.table_queue = []

        # 生成場所
        self.general_costomer_area = []

        # 店の入り口
        self.entrance_pos = None

        # 店の出口
        self.exit_pos = None

        # playerのスタート位置
        self.player_start = (0, 1)

        self.load_map()

        # # 待機場所がマップ座標とpygletの座標系と原点が違うのでリバースしている
        # logger.debug(f"wait_queueの確認（リバース変更前）{self.wait_queue}")
        self.wait_queue.reverse()
        
        # logger.debug(f"wait_queueの確認（リバース変更後）{self.wait_queue}")

        # self.log("マップの初期化完了しました。")
        # print(self.general_costomer_area)


    # セルの対応文字ごとにいろと役割を設定する（例：Bはグレーなど）
    # マップの文字情報（グリッド）をピクセル座標に変換する
    # キャラクターがマップの各マス（グリッド）に移動できるかどうかを判別する関数（is_walkable)
    def load_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                # x, y = self.to_pyglet_x_y(x, y)
                # y = self.height - (y + 1)
                # y = len(self.map_data) - (y + 1)
                pixel_x = x * self.cell_size
                # pixel_y = self.height - (y + 1) * self.cell_size
                pixel_y = (len(self.map_data) - (y + 1)) * self.cell_size
                # pixel_y = y * self.cell_size


                # ブロックごとの座標
                # print(f"{cell}: {pixel_x}, {pixel_y}")
                # 場合分け
                # 壁
                if cell == "B":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, 
                                                   self.cell_size, color=(64, 64, 64), 
                                                   batch=self.batch)
                    self.tiles.append(rect)

                # 何もない場所（移動可能）
                elif cell == ".":
                    pass
                # elif cell == "P":
                #     rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, self.cell_size, 
                #                                    color=(255, 0, 0), batch=self.batch)
                #     self.player_start = (x, y)
                #     # print(f"{cell}: {pixel_x}, {pixel_y}")
                #     self.log(f"{cell}: {pixel_x}, {pixel_y}")

                # 生成エリア
                elif cell == "G":
                    self.general_costomer_area.append((x, y))

                # 入り口
                elif cell == "N":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, 
                                                   self.cell_size, color=(0, 255, 255), 
                                                   batch=self.batch)
                    self.tiles.append(rect)

                # 入り口
                elif cell == "E":
                    self.entrance_pos = (x, y)
                    logger.debug(f"【入り口の座標の追加】{x, y}")

                # 出口
                elif cell == "O":
                    self.exit_pos = (x, y)
                    logger.debug(f"【出口座標の追加】{x, y}")

                
                # 待機場所
                elif cell == "W":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, 
                                                   self.cell_size, color=(0, 0, 255), 
                                                   batch=self.batch)
                    self.tiles.append(rect)
                    # print(f"もとの待機場所xy{x, y}")
                    # y = len(self.map_data) - (y + 1)
                    self.wait_queue.append((x, y))

                    # logger.debug(f"【待機場所の座標の追加】{x, y}")
                    # print(self.wait_queue.pop())


                # テーブル
                elif cell == "T":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, 
                                                   self.cell_size, color=(255, 255, 0), 
                                                   batch=self.batch)
                    self.tiles.append(rect)
                    # [宿題]
                    self.table_queue.append((x, y))

                # キャラクター
                elif cell == "C":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, 
                                                  self.cell_size, color=(255, 0, 0), 
                                                   batch=self.batch)
                    self.tiles.append(rect)

                # 席
                elif cell == "S":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, 
                                                   self.cell_size, color=(0, 100, 255), 
                                                   batch=self.batch)
                    self.tiles.append(rect)
                    # print(f"元のxy{x, y}")
                    # y = len(self.map_data) - (y + 1)
                    self.seat_queue.append((x, y))



    def is_walkable(self, x, y):
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            # 通れないにキャラが入っているかどうかを判別
            return self.map_data[y][x] not in self.block_tiles
        return False
                        

    # リストのｘ、ｙをpygletのx,yに変換する
    def to_pyglet_x_y(self, x, y):
        return x, len(self.map_data) - y - 1
                

class Background():
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch
        # マップのイラストの読み込み
        self.background_pic = pyglet.image.load('map_sample.png')
        # マップのイラストをspriteに設定する
        self.background_sprite = pyglet.sprite.Sprite(self.background_pic, x = 0, y = 0, batch=self.batch)
        self.background_sprite.z = 0
        # 引数として渡されたウィンドウのwidthとheightを取り出す
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]
        # スケーリング係数を設定
        self.background_sprite.scale_x = window.width / self.background_pic.width
        self.background_sprite.scale_y = window.height / self.background_pic.height
    
        
