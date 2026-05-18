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



from pyglet.event import EventDispatcher

class CharacterA(EventDispatcher):
    def __init__(self):
        super().__init__()
        self.item_count = 1  # 最初は薬草を1つ持っている
        
        # ① 'on_give_item' というイベント名をこのクラスに登録する
        self.register_event_type('on_give_item') 

    def give_item(self):
        if self.item_count > 0:
            self.item_count -= 1  # Aさんの薬草を減らす
            print("CharacterA: 薬草を渡しました。")
            
            # ③ イベントを発火（通知）する
            self.dispatch_event('on_give_item')


class CharacterB():
    def __init__(self):
        self.item_count = 0  # 最初は薬草を持っていない
        # ※ Bさんはイベントを発火しない（受け取るだけ）ので、EventDispatcherの継承は不要です

    # ② イベントを受け取ったときに実行される「ハンドラ（関数）」
    # 発火するイベント名（on_give_item）と同じ名前にします
    def on_give_item(self):
        self.item_count += 1  # Bさんの薬草を増やす
        print("CharacterB: 薬草を受け取りました！")


class Main():
    def __init__(self):
        characterA = CharacterA()
        characterB = CharacterB()

        # 状態の確認
        print(f"【初期状態】 Aさんの薬草: {characterA.item_count}個, Bさんの薬草: {characterB.item_count}個")
        print("-" * 50)

        # ② CharacterAのイベントの受け手として、CharacterBを登録する
        characterA.push_handlers(characterB)

        # Aさんがアイテムを渡す（この中でイベントが発火します）
        characterA.give_item()
        # characterA.dispatch_event('on_give_item')

        print("-" * 50)
        # 状態の確認
        print(f"【最終状態】 Aさんの薬草: {characterA.item_count}個, Bさんの薬草: {characterB.item_count}個")


if __name__ == "__main__":
    Main()