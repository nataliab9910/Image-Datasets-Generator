from enum import Enum, auto


DEFAULT_IMAGE_WIDTH = 100
DEFAULT_IMAGE_HEIGHT = 100


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
