import pyglet
from pyglet import shapes

window = pyglet.window.Window(width=640, height=480, resizable=True, caption="Name Mismatch Demo")
circle = shapes.Circle(x=320, y=240, radius=50, color=(255, 100, 100))

# 名前が一致しないパターン
# イベント名 'on_resize' を明示的に指定しているため、
# 関数名は自由に決められる（ここでは my_custom_resize_logic にしています）
@window.event('on_resize')
def my_custom_resize_logic(width, height):
    print(f"カスタム関数が発火しました！ 新しいサイズ: {width} x {height}")
    circle.x = width // 2
    circle.y = height // 2
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    window.clear()
    circle.draw()

if __name__ == "__main__":
    pyglet.app.run()