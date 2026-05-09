import pyglet
from pyglet.window import key

# -----------------
# 放送で使うイベントの登録を行うクラス
# -----------------
class Dispatcher(pyglet.event.EventDispatcher):
    def __init__(self):
        print("2. Dispatcherで放送を流します！")
        self.register_event_type('on_key_press_01')
