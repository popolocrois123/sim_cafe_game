from enum import IntEnum

class CustomerState(IntEnum):
    OUTSIDE = 1
    MOVING_TO_ENTRANCE = 2
    ARRIVE = 3
    MOVING_TO_WAIT = 4
    WAITING_IN_QUEUE = 5
    WAITING_TO_SIT_TO_SEAT = 6
    MOVING_TO_SEAT = 7
    SEATED = 8
    LEAVING = 9
    EXITED = 10



if __name__ == "__main__":
    s = CustomerState.OUTSIDE
    print(s.name)


