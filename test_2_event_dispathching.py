# from pyglet.event import EventDispatcher

# # 1. Dispatcherを継承したクラスを作る
# class GameCharacter(EventDispatcher):
#     def __init__(self):
#         super().__init__()
#         # 2. カスタムイベントを登録する（必ずon_から始める）
#         self.register_event_type('on_game_over')

#     def hit_by_enemy(self):
#         print("敵に当たった！")
#         # 3. イベントを通知（発火）する
#         self.dispatch_event('on_game_over')

# # --- 使い方 ---

# character = GameCharacter()

# # 反応する処理を登録
# def handle_game_over():
#     print("ゲームオーバー！残念！")

# # push_handlersを使って、イベントと関数を結びつける
# character.push_handlers(on_game_over=handle_game_over)

# # 実行
# character.hit_by_enemy()


from pyglet.event import EventDispatcher

# 1. Publisher（発信者）
class MyPublisher(EventDispatcher):
    def __init__(self):
        super().__init__()
        # イベントを登録
        self.register_event_type('on_my_event')

    def trigger_method(self, data):
        # 処理を行い、イベントを発火
        print(f"トリガー発動！データ: {data}")
        self.dispatch_event('on_my_event', data)

# 2. Subscriber（受信者）
class MySubscriber:
    def on_my_event(self, data):
        # 受け取った時の処理
        print(f"【テスト】イベントが届いた！受け取ったデータは {data} です")

# 3. インスタンスの生成
publisher = MyPublisher()
subscriber = MySubscriber()

# 4. 結びつける
publisher.push_handlers(on_my_event=subscriber.on_my_event)

# 5. トリガー関数を使って動作させる
# ★修正ポイント：クラス名ではなく、インスタンス名(publisher)を使います
publisher.trigger_method("Hello!")