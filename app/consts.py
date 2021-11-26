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
DEFAULT_ERROR_LOG_FILE = 'error.log'


class Inputs(Enum):
    SEARCH_ENGINE = 'engine'
    LOCAL_PATH = 'path'
    IS_SINGLE_SEARCH = 'isSingle'
    SINGLE_SEARCH_ENTRY = 'singleEntry'
    IS_GROUP_SEARCH = 'isGroup'
    GROUP_NAME = 'groupName'
    GROUP_SEARCH_ENTRIES = 'groupEntries'
    IMAGE_FORMAT = 'imgFormat'
    IMAGE_WIDTH = 'imgWidth'
    IMAGE_HEIGHT = 'imgHeight'
    KEEP_RATIO = 'keepRatio'
    IS_AUGMENTATION = 'augment'
    AUGMENTATION_LEVEL = 'augLevel'
    IS_HORIZONTAL_FLIP = 'horizontalFlip'
    IS_VERTICAL_FLIP = 'verticalFlip'
    ROTATION_LEVEL = 'rotation'
    SHARPNESS_MIN = 'sharpnessMin'
    SHARPNESS_MAX = 'sharpnessMax'
    CONTRAST_MIN = 'contrastMin'
    CONTRAST_MAX = 'contrastMax'
    BRIGHTNESS_MIN = 'brightnessMin'
    BRIGHTNESS_MAX = 'brightnessMax'
    SHUFFLE_IMAGES = 'shuffle'


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
