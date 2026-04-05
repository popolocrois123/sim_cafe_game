from enum import Enum

class State(Enum):
    WAITING = 1
    MOVING = 2
    SEATED = 3

if __name__ == "__main__":
    # Enumの使用例
    state = State.WAITING

    if state == State.WAITING:
        print("現在の状態: 待機中")
    elif state == State.MOVING:
        print("現在の状態: 移動中")
    elif state == State.SEATED:
        print("現在の状態: 着席中")
