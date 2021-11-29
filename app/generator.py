import io
import os
import random
import requests

from PIL import Image, ImageEnhance

import app.consts as consts

from app.api import ApiProvider
from app.exceptionLogger import exceptionLogSave


class Validator:
    def __init__(self, data):
        self._data = data

    def keyExists(self, key):
        if key not in self._data or not self._data[key]:
            raise KeyError(f'Required key {key.value} is not provided.')

    def isValueInEnum(self, key, enum):
        if self._data[key] not in [i.value for i in enum]:
            raise ValueError(f'{self._data[key]} value of {key.value} key is not supported.')

    def conditionKeyExistsAndIsTrue(self, key):
        try:
            self.keyExists(key)
        except KeyError:
            return False

        return self._data[key]

    def isDirectory(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f'{path} is not a directory.')

    def isEmptyDirectory(self, path):
        self.isDirectory(path)
        if os.listdir(path):
            raise ValueError(f'{path} is not empty.')


class Generator:
    def __init__(self, inputData):
        self._inputData = inputData
        self._validator = Validator(self._inputData)

    def validateInputs(self):
        # validate search engine
        self._validator.keyExists(consts.Inputs.SEARCH_ENGINE)
        self._validator.isValueInEnum(consts.Inputs.SEARCH_ENGINE, consts.SearchEngines)

        # validate local path
        self._validator.keyExists(consts.Inputs.LOCAL_PATH)
        self._validator.isDirectory(self._inputData[consts.Inputs.LOCAL_PATH])

        # validate search option
        # validate single search option
        if self._validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_SINGLE_SEARCH):
            self._validator.keyExists(consts.Inputs.SINGLE_SEARCH_ENTRY)

            destinationDirectory = self._inputData[consts.Inputs.LOCAL_PATH] \
                                   + '/' \
                                   + self._inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]
            try:
                self._validator.isEmptyDirectory(destinationDirectory)
            except NotADirectoryError:
                pass
        # validate group search option
        elif self._validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_GROUP_SEARCH):
            self._validator.keyExists(consts.Inputs.GROUP_NAME)
            self._validator.keyExists(consts.Inputs.GROUP_SEARCH_ENTRIES)
            self._inputData[consts.Inputs.GROUP_SEARCH_ENTRIES] = \
                [entry for entry in self._inputData[consts.Inputs.GROUP_SEARCH_ENTRIES].split(',') if entry]
        # no option defined
        else:
            raise KeyError('Type of search not defined.')

        # validate image format
        self._validator.keyExists(consts.Inputs.IMAGE_FORMAT)
        self._validator.isValueInEnum(consts.Inputs.IMAGE_FORMAT, consts.ImageFormats)

        # validate image size params
        self._validator.keyExists(consts.Inputs.IMAGE_HEIGHT)
        self._validator.keyExists(consts.Inputs.IMAGE_WIDTH)

        try:
            self._inputData[consts.Inputs.IMAGE_HEIGHT] = int(self._inputData[consts.Inputs.IMAGE_HEIGHT])
            self._inputData[consts.Inputs.IMAGE_WIDTH] = int(self._inputData[consts.Inputs.IMAGE_WIDTH])
        except ValueError:
            raise ValueError('Provided image height or width is not a valid number.')

        if not 0 < self._inputData[consts.Inputs.IMAGE_HEIGHT] <= consts.MAX_IMAGE_SIZE \
                or not 0 < self._inputData[consts.Inputs.IMAGE_WIDTH] <= consts.MAX_IMAGE_SIZE:
            raise ValueError(f'Provided image height and width should be higher than 0 and less than or equal '
                             f'{consts.MAX_IMAGE_SIZE}.')

        # validate augmentation
        if self._validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_AUGMENTATION):
            self._validateAugmentationOptions()
        else:
            self._inputData[consts.Inputs.IS_AUGMENTATION] = False

        # validate shuffle option
        if not self._validator.conditionKeyExistsAndIsTrue(consts.Inputs.SHUFFLE_IMAGES):
            self._inputData[consts.Inputs.SHUFFLE_IMAGES] = False

    def generateDataset(self, isCli=False):
        savedImagesNum = 0
        try:
            api = ApiProvider.getApi(self._inputData[consts.Inputs.SEARCH_ENGINE])
            if self._inputData[consts.Inputs.IS_SINGLE_SEARCH]:
                entry = self._inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]
                imageUrls = api.getImages(entry, isCli)
                images = self._processImages(imageUrls)
                savedImagesNum += self._saveImages(images, entry)
            elif self._inputData[consts.Inputs.IS_GROUP_SEARCH]:
                for entry in self._inputData[consts.Inputs.GROUP_SEARCH_ENTRIES]:
                    imageUrls = api.getImages(entry, isCli)
                    images = self._processImages(imageUrls)
                    savedImagesNum += self._saveImages(images, entry, True)
        except Exception:
            raise

        return savedImagesNum

    def _processImages(self, imageUrls):
        desiredImageSize = self._inputData[consts.Inputs.IMAGE_WIDTH], self._inputData[consts.Inputs.IMAGE_HEIGHT]

        images = []
        for index, imageUrl in enumerate(imageUrls):
            try:
                response = requests.get(imageUrl, timeout=10)
                if response.status_code == 200 and response.headers['content-type'].startswith('image/'):
                    image_bytes = io.BytesIO(response.content)
                    with Image.open(image_bytes) as image:
                        print(index)
                        image = image.resize(desiredImageSize, Image.ANTIALIAS)
                        images.append(image)
            except Exception as e:
                exceptionLogSave(e, imageUrl)
                continue

        return self._augmentImages(images)

    def _augmentImages(self, images):
        if not self._inputData[consts.Inputs.IS_AUGMENTATION]:
            return images

        multiplicationLevel = self._inputData[consts.Inputs.AUGMENTATION_LEVEL]
        rotationLevel = self._inputData[consts.Inputs.ROTATION_LEVEL]
        sharpnessRange = self._inputData[consts.Inputs.SHARPNESS_MIN], self._inputData[consts.Inputs.SHARPNESS_MAX]
        contrastRange = self._inputData[consts.Inputs.CONTRAST_MIN], self._inputData[consts.Inputs.CONTRAST_MAX]
        brightnessRange = self._inputData[consts.Inputs.BRIGHTNESS_MIN], self._inputData[consts.Inputs.BRIGHTNESS_MAX]

        augmentedImages = []
        for idx, image in enumerate(images):
            image = image.convert('RGB')

            augmentedImages.append(image)
            for i in range(1, multiplicationLevel):
                augmentedImage = image.rotate(random.uniform(-rotationLevel, rotationLevel) * 180)
                if self._inputData[consts.Inputs.IS_VERTICAL_FLIP] and bool(random.getrandbits(1)):
                    augmentedImage = augmentedImage.transpose(Image.FLIP_TOP_BOTTOM)
                if self._inputData[consts.Inputs.IS_HORIZONTAL_FLIP] and bool(random.getrandbits(1)):
                    augmentedImage = augmentedImage.transpose(Image.FLIP_LEFT_RIGHT)
                augmentedImage = ImageEnhance.Sharpness(augmentedImage).enhance(random.uniform(*sharpnessRange))
                augmentedImage = ImageEnhance.Contrast(augmentedImage).enhance(random.uniform(*contrastRange))
                augmentedImage = ImageEnhance.Brightness(augmentedImage).enhance(random.uniform(*brightnessRange))
                augmentedImages.append(augmentedImage)

        if self._inputData[consts.Inputs.SHUFFLE_IMAGES]:
            random.shuffle(augmentedImages)
        return augmentedImages

    def _saveImages(self, images, entry, isGroupSearch=False):
        destinationDir = self._inputData[consts.Inputs.LOCAL_PATH] + '/'

        if isGroupSearch:
            destinationDir = destinationDir + self._inputData[consts.Inputs.GROUP_NAME] + '/'
            if not os.path.exists(destinationDir):
                os.mkdir(destinationDir)

        destinationDir = destinationDir + entry + '/'
        os.mkdir(destinationDir)

        savedImagesCount = 0
        for img in images:
            try:
                img.save(f'{destinationDir}{entry}{savedImagesCount + 1:04}.'
                         f'{self._inputData[consts.Inputs.IMAGE_FORMAT]}')
                savedImagesCount += 1
            except Exception as e:
                exceptionLogSave(e)
                continue

        return savedImagesCount

    def _validateAugmentationOptions(self):
        # validate level
        try:
            self._validator.keyExists(consts.Inputs.AUGMENTATION_LEVEL)
            self._inputData[consts.Inputs.AUGMENTATION_LEVEL] = int(self._inputData[consts.Inputs.AUGMENTATION_LEVEL])
            if self._inputData[consts.Inputs.AUGMENTATION_LEVEL] < consts.AUGMENTATION_LEVEL_MIN \
                    or self._inputData[consts.Inputs.AUGMENTATION_LEVEL] > consts.AUGMENTATION_LEVEL_MAX:
                raise ValueError
        except KeyError:
            self._inputData[consts.Inputs.AUGMENTATION_LEVEL] = consts.DEFAULT_AUGMENTATION_LEVEL
        except ValueError:
            raise ValueError(f'Provided augmentation level is not a valid integer from range ['
                             f'{consts.AUGMENTATION_LEVEL_MIN}, {consts.AUGMENTATION_LEVEL_MAX}].')

        # validate flips
        if not self._validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_HORIZONTAL_FLIP):
            self._inputData[consts.Inputs.IS_HORIZONTAL_FLIP] = False
        if not self._validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_VERTICAL_FLIP):
            self._inputData[consts.Inputs.IS_VERTICAL_FLIP] = False

        # validate rotation level
        try:
            self._validator.keyExists(consts.Inputs.ROTATION_LEVEL)
            self._inputData[consts.Inputs.ROTATION_LEVEL] = float(self._inputData[consts.Inputs.ROTATION_LEVEL])
            if self._inputData[consts.Inputs.ROTATION_LEVEL] < consts.ROTATION_LEVEL_MIN \
                    or self._inputData[consts.Inputs.ROTATION_LEVEL] > consts.ROTATION_LEVEL_MAX:
                raise ValueError
        except KeyError:
            self._inputData[consts.Inputs.ROTATION_LEVEL] = consts.DEFAULT_ROTATION_LEVEL
        except ValueError:
            raise ValueError(f'Provided rotation level is not a valid number from range ['
                             f'{consts.ROTATION_LEVEL_MIN}, {consts.ROTATION_LEVEL_MAX}].')

        # validate sharpness level
        self._validateImageAdjustmentOptions('sharpness', consts.Inputs.SHARPNESS_MIN, consts.Inputs.SHARPNESS_MAX,
                                             consts.DEFAULT_SHARPNESS_MIN, consts.DEFAULT_SHARPNESS_MAX,
                                             consts.SHARPNESS_MIN, consts.SHARPNESS_MAX)

        # validate brightness level
        self._validateImageAdjustmentOptions('brightness', consts.Inputs.BRIGHTNESS_MIN, consts.Inputs.BRIGHTNESS_MAX,
                                             consts.DEFAULT_BRIGHTNESS_MIN, consts.DEFAULT_BRIGHTNESS_MAX,
                                             consts.BRIGHTNESS_MIN, consts.BRIGHTNESS_MAX)

        # validate contrast level
        self._validateImageAdjustmentOptions('contrast', consts.Inputs.CONTRAST_MIN, consts.Inputs.CONTRAST_MAX,
                                             consts.DEFAULT_CONTRAST_MIN, consts.DEFAULT_CONTRAST_MAX,
                                             consts.CONTRAST_MIN, consts.CONTRAST_MAX)

    def _validateImageAdjustmentOptions(self, optionName, minInput, maxInput, defaultMin, defaultMax, minValue,
                                        maxValue):
        try:
            self._validator.keyExists(minInput)
            self._inputData[minInput] = float(self._inputData[minInput])
            if self._inputData[minInput] < minValue:
                raise ValueError
        except KeyError:
            self._inputData[minInput] = defaultMin
        except ValueError:
            raise ValueError(f'Provided {optionName} level is not a valid number higher than or equal to {minValue}.')

        try:
            self._validator.keyExists(maxInput)
            self._inputData[maxInput] = float(self._inputData[maxInput])
            if self._inputData[maxInput] > maxValue:
                raise ValueError
        except KeyError:
            self._inputData[maxInput] = defaultMax
        except ValueError:
            raise ValueError(f'Provided {optionName} level is not a valid number lower than or equal to {maxValue}.')

        if self._inputData[minInput] > self._inputData[maxInput]:
            raise ValueError(f'Minimum {optionName} level should be lower than or equal to maximum {optionName} level.')
