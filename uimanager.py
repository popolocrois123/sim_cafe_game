from pyglet.window import key

class UIManager:
    def __init__(self):
        self.is_paused = False

    def on_key_press_01(self, symbol, modifiers):
        print("3. UIManagerが放送を受信しました！")
        if symbol == key.P:
            self.is_paused = not self.is_paused

    