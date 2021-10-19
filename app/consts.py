from enum import Enum, auto


class Inputs(Enum):
    SEARCH_ENGINE = auto()
    LOCAL_PATH = auto()
    IS_SINGLE_SEARCH = auto()
    SINGLE_SEARCH_ENTRY = auto()
    IS_GROUP_SEARCH = auto()
    GROUP_NAME = auto()
    GROUP_SEARCH_ENTRIES = auto()
    IMAGE_FORMAT = auto()
    IMAGE_WIDTH = auto()
    IMAGE_HEIGHT = auto()
    AUGMENTATION = auto()
