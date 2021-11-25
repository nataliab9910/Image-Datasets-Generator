from enum import Enum, auto

DEFAULT_IMAGE_WIDTH = 100
DEFAULT_IMAGE_HEIGHT = 100
MAX_IMAGE_SIZE = 500
DEFAULT_SHARPNESS_MIN, DEFAULT_SHARPNESS_MAX = 1.0, 1.0
DEFAULT_CONTRAST_MIN, DEFAULT_CONTRAST_MAX = 1.0, 1.0
DEFAULT_BRIGHTNESS_MIN, DEFAULT_BRIGHTNESS_MAX = 1.0, 1.0
DEFAULT_ROTATION_LEVEL = 0
DEFAULT_AUGMENTATION_LEVEL = 3
AUGMENTATION_LEVEL_MIN, AUGMENTATION_LEVEL_MAX = 2, 50
ROTATION_LEVEL_MIN, ROTATION_LEVEL_MAX = 0, 1
SHARPNESS_MIN, SHARPNESS_MAX = 0., 2.
BRIGHTNESS_MIN, BRIGHTNESS_MAX = 0., 2.
CONTRAST_MIN, CONTRAST_MAX = 0., 2.

DEFAULT_MOCK_PATH = '../mocks/{}/{}.json'


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
    KEEP_RATIO = auto()
    IS_AUGMENTATION = auto()
    AUGMENTATION_LEVEL = auto()
    IS_HORIZONTAL_FLIP = auto()
    IS_VERTICAL_FLIP = auto()
    ROTATION_LEVEL = auto()
    SHARPNESS_MIN = auto()
    SHARPNESS_MAX = auto()
    CONTRAST_MIN = auto()
    CONTRAST_MAX = auto()
    BRIGHTNESS_MIN = auto()
    BRIGHTNESS_MAX = auto()
    SHUFFLE_IMAGES = auto()


class AppStatuses(Enum):
    COLLECTING_DATA = 'Collecting inputs...'
    VALIDATING_DATA = 'Validating inputs..'
    SEARCHING = 'Searching...'
    PROCESSING_IMAGES = 'Processing images...'
    SAVING_IMAGES = 'Preparing dataset...'
    FINISH = 'Your database is ready!'
    ERROR_VALIDATION = 'Error during validation. Please, check provided data and try again.'


class SearchOptions(Enum):
    SINGLE_SEARCH = 'singleSearch'
    GROUP_SEARCH = 'groupSearch'


class SearchEngines(Enum):
    GOOGLE = 'Google'
    YAHOO = 'Yahoo'
    BING = 'Bing'


class ImageFormats(Enum):
    PNG = 'png'
    JPG = 'jpg'
