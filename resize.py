import pyglet
from pyglet import shapes

# 1. ウィンドウの作成
window = pyglet.window.Window(width=640, height=480, resizable=True, caption="Event Demo")

# 円の生成（初期設定）
circle = shapes.Circle(x=320, y=240, radius=50, color=(50, 225, 30))

# 2. 名前が一致するパターンのイベント定義
@window.event
def on_resize(width, height):
    """ウィンドウサイズが変わったときに実行される"""
    print(f"Resize Event: {width} x {height}")
    
    # ウィンドウサイズに合わせて円の位置を中央に更新
    circle.x = width // 2
    circle.y = height // 2
    
    # デフォルトの挙動（プロジェクション行列の更新など）を維持するため必須
    return pyglet.event.EVENT_HANDLED

"""
以下のコードをコメントアウトするとオーバーライドするので、
以下のイベントが発火しなくなる（on_resizeの方が優先される）ため、名前が一致しないパターンのイベント定義を使用することができる。
"""

# @window.event('on_resize')
# def my_custom_resize_logic(width, height):
#     print(f"カスタム関数が発火しました！ 新しいサイズ: {width} x {height}")
#     circle.x = width // 2
#     circle.y = height // 2
#     return pyglet.event.EVENT_HANDLED

# 3. 描画イベント
@window.event
def on_draw():
    """画面の描画更新が必要なときに実行される"""
    window.clear()
    circle.draw()

# アプリケーションの実行
if __name__ == "__main__":
    pyglet.app.run()