from enum import Enum


class IMETransition(Enum):
    REQUEST_TO_OFF = 3
    REQUEST_TO_ON = 4
    TRANSITIONING_ON = 1
    TRANSITIONING_OFF = 2
    IDLE = 0