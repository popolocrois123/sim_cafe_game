from pyglet.event import EventDispatcher

class CharacterA(EventDispatcher):
    def __init__(self):
        super().__init__() # EventDispatcherの初期化を呼び出す
        self.register_event_type('on_give_item') # カスタムイベントの登録
        # self.register_event_type('on_receive_item') # カスタムイベントの登録

    def give_item(self):
        print("Aさんが薬草を渡しました")
        self.dispatch_event('on_give_item') # イベントの発火

    # def receive_item(self):
    #     print("CharacterBがアイテムを受け取りました")
    #     self.dispatch_event('on_receive_item') # イベントの発火

class CharacterB(EventDispatcher):
    def __init__(self):
        super().__init__() # EventDispatcherの初期化を呼び出す
        # self.register_event_type('on_give_item') # カスタムイベントの登録
        self.register_event_type('on_receive_item') # カスタムイベントの登録
    
    # def receive_item(self):
    #     print("CharacterBがアイテムを受け取りました")
    #     self.dispatch_event('on_receive_item') # イベントの発火

    def on_give_item(self):
        print("CharacterB: Aさんから薬草を受け取りました")
        self.receive_item()

    # def give_item(self):
    #     print("CharacterAがアイテムを渡しました")
    #     self.dispatch_event('on_give_item') # イベントの発火


class Main():
    def __init__(self):
        characterA = CharacterA()
        characterB = CharacterB()
        # CharacterAのイベントをCharacterBがリッスン
        characterA.push_handlers(characterB)
        # CharacterBのイベントをCharacterAがリッスン
        characterB.push_handlers(characterA)

        # AさんとBさんの薬草所持数を管理するリスト
        self.item_counts = [0, 0]  # [Aの薬草数, Bの薬草数]

        # AがBにアイテムを渡す
        characterA.give_item()


if __name__ == "__main__":
    main = Main()

