import pyglet

# ---------------------------------------------------------
# Customer: 詳細は持たず、Managerから与えられたイベント定義を使う
# ---------------------------------------------------------
class CustomerDispatcher:
    def __init__(self, event_types):
        self._dispatcher = pyglet.event.EventDispatcher()
        
        # マネージャーから受け取ったリストを元に登録
        for event_name in event_types:
            self._dispatcher.register_event_type(event_name)

    # 窓口（委譲）
    def push_handlers(self, *args, **kwargs):
        self._dispatcher.push_handlers(*args, **kwargs)

    def dispatch_event(self, event_type, *args, **kwargs):
        self._dispatcher.dispatch_event(event_type, *args, **kwargs)

    def buy_item(self, item):
        # print(f"[{self.name}] {item}を買います")
        self.dispatch_event("OUTSIDE")


    # OUTSIDE
    