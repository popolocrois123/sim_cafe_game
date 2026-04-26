import pyglet
from pyglet import shapes

# 1. キャラクタークラス（変更なし）
class Character(pyglet.event.EventDispatcher):
    def __init__(self, x, y):
        self.rect = shapes.Rectangle(x=x, y=y, width=40, height=40, color=(255, 0, 0)) # 赤色
        self.is_jumping = False
        self.velocity_y = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = 15
            # --- 疎結合の合図 ---
            self.dispatch_event('on_jump')

    def update(self, dt):
        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y -= 1.0
            if self.rect.y <= 50:
                self.rect.y = 50
                self.is_jumping = False
                self.velocity_y = 0

Character.register_event_type('on_jump')

# 2. メインプログラム
window = pyglet.window.Window(width=600, height=400, caption="色が変わるジャンプ")
player = Character(x=280, y=50)

# --- イベントハンドラ（色を変える処理） ---
def on_jump_effect():
    # 色を青にする
    player.rect.color = (0, 0, 255)
    # 0.2秒後に色を赤に戻す（タイマー機能）
    pyglet.clock.schedule_once(reset_color, 0.2)

def reset_color(dt):
    # 色を赤に戻す
    player.rect.color = (255, 0, 0)

# 連結
player.push_handlers(on_jump=on_jump_effect)

@window.event
def on_draw():
    window.clear()
    player.rect.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        player.jump()

def update(dt):
    player.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()