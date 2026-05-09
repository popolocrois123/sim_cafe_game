import pyglet
from pyglet.event import EventDispatcher
from pyglet.window import key

# 1. Dispatcherを継承したクラス
class GameCharacter(EventDispatcher):
    def __init__(self):
        super().__init__()
        self.hp = 100
        self.enemy_attack_power = 20
        # カスタムイベントの登録
        self.register_event_type('on_game_over')

    # ダメージを受けるメソッド（キー入力とは切り離す）
    def take_damage(self):
        self.hp -= self.enemy_attack_power
        print(f"攻撃を受けた！現在のHP: {self.hp}")
        if self.hp <= 0:
            self.dispatch_event('on_game_over')

# 2. メインウィンドウクラス
class Main(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=400, height=300, caption="Game")
        self.character = GameCharacter()
        
        # ゲームオーバーイベントをMainクラスで監視する設定
        self.character.push_handlers(on_game_over=self.on_game_over_event)

    def on_key_press(self, symbol, modifiers):
        # 攻撃キー(P)が押されたらキャラクターにダメージ処理を依頼
        if symbol == key.P:
            self.character.take_damage()

    def on_game_over_event(self):
        print("Mainクラスで検知：ゲームオーバー！終了します。")
        self.close()

# 実行
if __name__ == "__main__":
    window = Main()
    pyglet.app.run()