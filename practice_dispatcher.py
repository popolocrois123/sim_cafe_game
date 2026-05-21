# from pyglet.event import EventDispatcher

# class CharacterA(EventDispatcher):
#     def __init__(self):
#         super().__init__() # EventDispatcherの初期化を呼び出す
#         # 薬草の初期所持数
#         self.item_count = 1  # Aさんは最初に薬草を1つ持っていると仮定
#         self.register_event_type('on_give_item') # カスタムイベントの登録
#         # self.register_event_type('on_receive_item') # カスタムイベントの登録

#     def give_item(self):
#         # print("Aさんが薬草を渡しました")
#         self.item_count -= 1  # Aさんの薬草数を減らす
#         # self.dispatch_event('on_give_item') # イベントの発火


#     def on_give_item(self):
#         print("CharacterA: Bさんに薬草を渡しました")
#         self.give_item()

#     # def receive_item(self):
#     #     print("CharacterBがアイテムを受け取りました")
#     #     self.dispatch_event('on_receive_item') # イベントの発火

# class CharacterB(EventDispatcher):
#     def __init__(self):
#         super().__init__() # EventDispatcherの初期化を呼び出す
#         self.item_count = 0  # Bさんは最初に薬草を0つ持っていると仮定
#         # self.register_event_type('on_give_item') # カスタムイベントの登録
#         self.register_event_type('on_receive_item') # カスタムイベントの登録
    
#     def receive_item(self):
#         print("CharacterBがアイテムを受け取りました")
#         self.item_count += 1  # Bさんの薬草数を増やす
#         # self.dispatch_event('on_receive_item') # イベントの発火

#     def on_receive_item(self):
#         print("CharacterB: Aさんから薬草を受け取りました")
#         self.receive_item()

#     def on_give_item(self):
#         self.receive_item()

#     # def give_item(self):
#     #     print("CharacterAがアイテムを渡しました")
#     #     self.dispatch_event('on_give_item') # イベントの発火


# class Main():
#     def __init__(self):
#         characterA = CharacterA()
#         characterB = CharacterB()
#         # CharacterAのイベントをCharacterBがリッスン
#         characterA.push_handlers(characterB)
#         # CharacterBのイベントをCharacterAがリッスン
#         # characterB.push_handlers(characterA)

#         # 薬草の初期所持数を表示
#         print(f"初期状態: Aさんの薬草数 = {characterA.item_count}, Bさんの薬草数 = {characterB.item_count}")

#         # # AがBにアイテムを渡す
#         # characterA.give_item()
#         # キャラクターAのイベントディスパッチャを発火する
#         characterA.dispatch_event('on_give_item')
#         # characterB.dispatch_event('on_receive_item')

#         # 薬草の最終所持数を表示
#         print(f"最終状態: Aさんの薬草数 = {characterA.item_count}, Bさんの薬草数 = {characterB.item_count}")


# if __name__ == "__main__":
#     main = Main()


# --------------------------
# 違う呼び出し型
# --------------------------

# from pyglet.event import EventDispatcher

# class CharacterA(EventDispatcher):
#     def __init__(self):
#         super().__init__()
#         self.item_count = 1  # 最初は薬草を1つ持っている
        
#         # ① 'on_give_item' というイベント名をこのクラスに登録する
#         self.register_event_type('on_give_item') 

#     def give_item(self):
#         if self.item_count > 0:
#             self.item_count -= 1  # Aさんの薬草を減らす
#             print("CharacterA: 薬草を渡しました。")
            
#             # ③ イベントを発火（通知）する
#             self.dispatch_event('on_give_item')


# class CharacterB():
#     def __init__(self):
#         self.item_count = 0  # 最初は薬草を持っていない
#         # ※ Bさんはイベントを発火しない（受け取るだけ）ので、EventDispatcherの継承は不要です

#     # ② イベントを受け取ったときに実行される「ハンドラ（関数）」
#     # 発火するイベント名（on_give_item）と同じ名前にします
#     def on_give_item(self):
#         self.item_count += 1  # Bさんの薬草を増やす
#         print("CharacterB: 薬草を受け取りました！")


# class Main():
#     def __init__(self):
#         characterA = CharacterA()
#         characterB = CharacterB()

#         # 状態の確認
#         print(f"【初期状態】 Aさんの薬草: {characterA.item_count}個, Bさんの薬草: {characterB.item_count}個")
#         print("-" * 50)

#         # ② CharacterAのイベントの受け手として、CharacterBを登録する
#         characterA.push_handlers(characterB)

#         # Aさんがアイテムを渡す（この中でイベントが発火します）
#         characterA.give_item()
#         # characterA.dispatch_event('on_give_item')

#         print("-" * 50)
#         # 状態の確認
#         print(f"【最終状態】 Aさんの薬草: {characterA.item_count}個, Bさんの薬草: {characterB.item_count}個")


# if __name__ == "__main__":
#     Main()





import pyglet
from pyglet.event import EventDispatcher

# 2. CharacterAクラス（イベントの発信源 ＆ 自分の電波も受信する）
class CharacterA(EventDispatcher):
    def __init__(self):
        super().__init__()
        self.item_count = 1
        self.register_event_type('on_give_item')

    def on_give_item(self):
        self.item_count -= 1
        print("CharacterA: 自分のイベントを検知して、薬草を1つ減らしました。")

# 3. CharacterBクラス（電波を受信するだけ）
class CharacterB():
    def __init__(self):
        self.item_count = 0

    def on_give_item(self):
        self.item_count += 1
        print("CharacterB: イベントを検知して、薬草を1つ増やしました。")


# 4. メイン処理をまとめたMainクラス
class Main():
    def __init__(self):
        # キャラクターの作成（インスタンス化）
        characterA = CharacterA()
        characterB = CharacterB()

        # 【初期状態の確認】
        print(f"【開始前】 Aさんの薬草: {characterA.item_count}個, Bさんの薬草: {characterB.item_count}個")
        print("-" * 50)

        # Aさんのイベント（電波）を、BさんとAさん自身に紐付ける
        characterA.push_handlers(characterB)
        # characterA.push_handlers(characterA) # ★自分も登録！

        # イベントを直接発火！
        characterA.dispatch_event('on_give_item')

        print("-" * 50)
        # 【最終状態の確認】
        print(f"【終了後】 Aさんの薬草: {characterA.item_count}個, Bさんの薬草: {characterB.item_count}個")


# 5. 一番下はMainクラスを呼び出すだけのシンプルな1行に！
if __name__ == "__main__":
    Main()

# ---------------------
# キャラクターをまとめる
# ----------------------


# import pyglet
# from pyglet.event import EventDispatcher

# # 2. キャラクターの設計図（共通クラス）
# class Character(EventDispatcher):
#     def __init__(self, name, item_count=0):
#         super().__init__()
#         self.name = name
#         self.item_count = item_count
#         self.register_event_type('on_give_item')

#     def receive_item(self):
#         """アイテムを受け取る関数"""
#         self.item_count += 1
#         print(f"[{self.name}]: 薬草を1つ受け取りました！ (現在: {self.item_count}個)")


# # 3. すべての管理と実行を行うMainクラス
# class Main():
#     def __init__(self):
#         # キャラクターの作成
#         self.characterA = Character("Aさん", item_count=1)
#         self.characterB = Character("Bさん", item_count=0)

#         # 【初期状態の確認】
#         print(f"【開始前】 Aさん: {self.characterA.item_count}個, Bさん: {self.characterB.item_count}個")
#         print("-" * 50)

#         # イベントの紐付け（配線）
#         # ① Aさんが発火したら、Bさんが受け取る
#         self.characterA.push_handlers(on_give_item=self.characterB.receive_item)
        
#         # ② Aさんが発火したら、Aさん自身のアイテムを1つ減らす（ラムダ式）
#         self.characterA.push_handlers(on_give_item=lambda: setattr(self.characterA, 'item_count', self.characterA.item_count - 1))

#         # イベントの実行
#         self.characterA.dispatch_event('on_give_item')

#         print("-" * 50)
#         # 【最終状態の確認】
#         print(f"【終了後】 Aさん: {self.characterA.item_count}個, Bさん: {self.characterB.item_count}個")


# # 4. 最下部は呼び出すだけのシンプルな1行に！
# if __name__ == "__main__":
#     Main()