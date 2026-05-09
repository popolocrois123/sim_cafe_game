import pyglet

class Customer:
    def __init__(self, name):
        self.name = name
        # 継承せずに、インスタンス変数として保持する（コンポジション）
        self._dispatcher = pyglet.event.EventDispatcher()
        
        # 内部のディスパッチャに対してイベントタイプを登録
        self._dispatcher.register_event_type('on_buy')

    # --- 外部から使う機能を委譲（Delegation） ---
    
    def push_handlers(self, *args, **kwargs):
        """Pygletの push_handlers をそのまま利用"""
        self._dispatcher.push_handlers(*args, **kwargs)

    def dispatch_event(self, event_type, *args, **kwargs):
        """イベント発火も内部のディスパッチャへ渡す"""
        self._dispatcher.dispatch_event(event_type, *args, **kwargs)

    # ------------------------------------------

    def buy_item(self, item, price):
        print(f"{self.name}が{item}を買いました")
        # 保持しているディスパッチャ経由で発火
        self.dispatch_event('on_buy', item, price)

# 利用側 (Main)
class MainApplication:
    def __init__(self):
        self.customer = Customer("田中さん")
        
        # 継承していなくても、push_handlersが使える！
        self.customer.push_handlers(on_buy=self.handle_on_buy)

    def handle_on_buy(self, item, price):
        print(f"[UI通知] {item} ({price}円) が売れました")

    def run(self):
        self.customer.buy_item("りんご", 100)

app = MainApplication()
app.run()