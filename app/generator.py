import io
import random
import os
import requests
from PIL import Image, ImageEnhance

import app.consts as consts
from app.api import ApiProvider


class Validator:
    def __init__(self, data):
        self._data = data

    def keyExists(self, key):
        if key not in self._data or not self._data[key]:
            raise KeyError(f'Required key {key} is not provided.')

    def isValueInEnum(self, key, enum):
        if self._data[key] not in [i.value for i in enum]:
            raise ValueError(f'{self._data[key]} value of {key} key is not supported.')

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
        self.inputData = inputData

    def validateInputs(self):
        # self.inputData[consts.Inputs.SEARCH_ENGINE] = 'ojoj'
        validator = Validator(self.inputData)

        # validate search engine
        validator.keyExists(consts.Inputs.SEARCH_ENGINE)
        validator.isValueInEnum(consts.Inputs.SEARCH_ENGINE, consts.SearchEngines)

        # validate local path
        validator.keyExists(consts.Inputs.LOCAL_PATH)
        validator.isDirectory(self.inputData[consts.Inputs.LOCAL_PATH])

        # validate search option
        # validate single search option
        if validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_SINGLE_SEARCH):
            validator.keyExists(consts.Inputs.SINGLE_SEARCH_ENTRY)

            destinationDirectory = self.inputData[consts.Inputs.LOCAL_PATH] \
                                   + '/' \
                                   + self.inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]
            try:
                validator.isEmptyDirectory(destinationDirectory)
            except NotADirectoryError:
                pass
        # validate group search option
        elif validator.conditionKeyExistsAndIsTrue(consts.Inputs.IS_GROUP_SEARCH):
            validator.keyExists(consts.Inputs.GROUP_NAME)
            validator.keyExists(consts.Inputs.GROUP_SEARCH_ENTRIES)
            self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES] = \
                [entry for entry in self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES].split(',') if entry]
        # no option defined
        else:
            raise KeyError('Type of search not defined.')

        # validate image format
        validator.keyExists(consts.Inputs.IMAGE_FORMAT)
        validator.isValueInEnum(consts.Inputs.IMAGE_FORMAT, consts.ImageFormats)

        # validate image size params
        validator.keyExists(consts.Inputs.IMAGE_HEIGHT)
        validator.keyExists(consts.Inputs.IMAGE_WIDTH)

        try:
            self.inputData[consts.Inputs.IMAGE_HEIGHT] = int(self.inputData[consts.Inputs.IMAGE_HEIGHT])
            self.inputData[consts.Inputs.IMAGE_WIDTH] = int(self.inputData[consts.Inputs.IMAGE_WIDTH])
        except ValueError:
            raise KeyError('Provided image height or width is not a valid number.')

        if not 0 < self.inputData[consts.Inputs.IMAGE_HEIGHT] <= consts.MAX_IMAGE_SIZE \
                or not 0 < self.inputData[consts.Inputs.IMAGE_WIDTH] <= consts.MAX_IMAGE_SIZE:
            raise ValueError(f'Provided image height and width should be higher than 0 and less than or equal '
                             f'{consts.MAX_IMAGE_SIZE}.')

        # validate keep ratio
        try:
            validator.keyExists(consts.Inputs.KEEP_RATIO)
        except KeyError:
            self.inputData[consts.Inputs.KEEP_RATIO] = False

        if consts.Inputs.IS_AUGMENTATION not in self.inputData:
            self.inputData[consts.Inputs.IS_AUGMENTATION] = False
        else:
            if consts.Inputs.AUGMENTATION_LEVEL not in self.inputData:
                self.inputData[consts.Inputs.AUGMENTATION_LEVEL] = consts.DEFAULT_AUGMENTATION_LEVEL
            else:
                try:
                    self.inputData[consts.Inputs.AUGMENTATION_LEVEL] = int(self.inputData[consts.Inputs.AUGMENTATION_LEVEL])
                except ValueError:
                    raise KeyError('Provided augmentation level is not a valid number.')

                if self.inputData[consts.Inputs.AUGMENTATION_LEVEL] < 2 or self.inputData[consts.Inputs.AUGMENTATION_LEVEL] > 50:
                    raise ValueError('Provided augmentation level should be any integer from range [2, 50].')

            if consts.Inputs.IS_HORIZONTAL_FLIP not in self.inputData:
                self.inputData[consts.Inputs.IS_HORIZONTAL_FLIP] = False

            if consts.Inputs.IS_VERTICAL_FLIP not in self.inputData:
                self.inputData[consts.Inputs.IS_VERTICAL_FLIP] = False

            if consts.Inputs.ROTATION_LEVEL not in self.inputData:
                self.inputData[consts.Inputs.ROTATION_LEVEL] = consts.DEFAULT_ROTATION_LEVEL
            else:
                try:
                    self.inputData[consts.Inputs.ROTATION_LEVEL] = float(self.inputData[consts.Inputs.ROTATION_LEVEL])
                except ValueError:
                    raise KeyError('Provided rotation level is not a valid number.')

                if self.inputData[consts.Inputs.ROTATION_LEVEL] < 0 or self.inputData[consts.Inputs.ROTATION_LEVEL] > 1:
                    raise ValueError('Provided rotation level should be higher than or equal to 0 and lower than or equal to 1.')

            if consts.Inputs.SHARPNESS_MIN not in self.inputData:
                self.inputData[consts.Inputs.SHARPNESS_MIN] = consts.DEFAULT_SHARPNESS_MIN
            else:
                try:
                    self.inputData[consts.Inputs.SHARPNESS_MIN] = float(self.inputData[consts.Inputs.SHARPNESS_MIN])
                except ValueError:
                    raise KeyError('Provided minimum sharpness level is not a valid number.')

                if self.inputData[consts.Inputs.SHARPNESS_MIN] < 0:
                    raise ValueError('Minimum sharpness level should be higher than or equal to 0.')

            if consts.Inputs.SHARPNESS_MAX not in self.inputData:
                self.inputData[consts.Inputs.SHARPNESS_MAX] = consts.DEFAULT_SHARPNESS_MAX
            else:
                try:
                    self.inputData[consts.Inputs.SHARPNESS_MAX] = float(self.inputData[consts.Inputs.SHARPNESS_MAX])
                except ValueError:
                    raise KeyError('Provided maximum sharpness level is not a valid number.')

                if self.inputData[consts.Inputs.SHARPNESS_MAX] > 2:
                    raise ValueError('Maximum sharpness level should be lower than or equal to 2')

            if self.inputData[consts.Inputs.SHARPNESS_MIN] > self.inputData[consts.Inputs.SHARPNESS_MAX]:
                raise ValueError('Minimum sharpness level should be lower than or equal to maximum sharpness level.')

            if consts.Inputs.BRIGHTNESS_MIN not in self.inputData:
                self.inputData[consts.Inputs.BRIGHTNESS_MIN] = consts.DEFAULT_SHARPNESS_MIN
            else:
                try:
                    self.inputData[consts.Inputs.BRIGHTNESS_MIN] = float(self.inputData[consts.Inputs.BRIGHTNESS_MIN])
                except ValueError:
                    raise KeyError('Provided minimum sharpness level is not a valid number.')

                if self.inputData[consts.Inputs.BRIGHTNESS_MIN] < 0:
                    raise ValueError('Minimum sharpness level should be higher than or equal to 0.')

            if consts.Inputs.BRIGHTNESS_MAX not in self.inputData:
                self.inputData[consts.Inputs.BRIGHTNESS_MAX] = consts.DEFAULT_BRIGHTNESS_MAX
            else:
                try:
                    self.inputData[consts.Inputs.BRIGHTNESS_MAX] = float(self.inputData[consts.Inputs.BRIGHTNESS_MAX])
                except ValueError:
                    raise KeyError('Provided maximum sharpness level is not a valid number.')

                if self.inputData[consts.Inputs.BRIGHTNESS_MAX] > 2:
                    raise ValueError('Maximum sharpness level should be lower than or equal to 2')

            if self.inputData[consts.Inputs.BRIGHTNESS_MIN] > self.inputData[consts.Inputs.BRIGHTNESS_MAX]:
                raise ValueError('Minimum sharpness level should be lower than or equal to maximum sharpness level.')

            if consts.Inputs.CONTRAST_MIN not in self.inputData:
                self.inputData[consts.Inputs.CONTRAST_MIN] = consts.DEFAULT_CONTRAST_MIN
            else:
                try:
                    self.inputData[consts.Inputs.CONTRAST_MIN] = float(self.inputData[consts.Inputs.CONTRAST_MIN])
                except ValueError:
                    raise KeyError('Provided minimum sharpness level is not a valid number.')

                if self.inputData[consts.Inputs.CONTRAST_MIN] < 0:
                    raise ValueError('Minimum sharpness level should be higher than or equal to 0.')

            if consts.Inputs.CONTRAST_MAX not in self.inputData:
                self.inputData[consts.Inputs.CONTRAST_MAX] = consts.DEFAULT_CONTRAST_MAX
            else:
                try:
                    self.inputData[consts.Inputs.CONTRAST_MAX] = float(self.inputData[consts.Inputs.CONTRAST_MAX])
                except ValueError:
                    raise KeyError('Provided maximum sharpness level is not a valid number.')

                if self.inputData[consts.Inputs.CONTRAST_MAX] > 2:
                    raise ValueError('Maximum sharpness level should be lower than or equal to 2')

            if self.inputData[consts.Inputs.CONTRAST_MIN] > self.inputData[consts.Inputs.CONTRAST_MAX]:
                raise ValueError('Minimum sharpness level should be lower than or equal to maximum sharpness level.')

        if consts.Inputs.SHUFFLE_IMAGES not in self.inputData:
            self.inputData[consts.Inputs.SHUFFLE_IMAGES] = False

    def generateDataset(self):
        savedImagesNum = 0
        try:
            api = ApiProvider.getApi(self.inputData[consts.Inputs.SEARCH_ENGINE])
            if self.inputData[consts.Inputs.IS_SINGLE_SEARCH]:
                entry = self.inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]
                imageUrls = api.getImages(entry)
                print(imageUrls)
                images = self._processImages(imageUrls)
                savedImagesNum += self._saveImages(images, entry)
            elif self.inputData[consts.Inputs.IS_GROUP_SEARCH]:
                for entry in self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES]:
                    imageUrls = api.getImages(entry)
                    images = self._processImages(imageUrls)
                    print('before save')
                    savedImagesNum += self._saveImages(images, entry, True)
        except Exception:
            raise

        return savedImagesNum

    def _processImages(self, imageUrls):
        desiredImageSize = (self.inputData[consts.Inputs.IMAGE_WIDTH], self.inputData[consts.Inputs.IMAGE_HEIGHT])

        images = []
        for index, imageUrl in enumerate(imageUrls):
            try:
                response = requests.get(imageUrl, timeout=10)
                if response.status_code == 200 and response.headers['content-type'].startswith('image/'):
                    image_bytes = io.BytesIO(response.content)
                    with Image.open(image_bytes) as image:
                        print(index)
                        if self.inputData[consts.Inputs.KEEP_RATIO]:
                            image.thumbnail(desiredImageSize, Image.ANTIALIAS)
                        else:
                            image = image.resize(desiredImageSize, Image.ANTIALIAS)

                        images.append(image)
            except Exception as e:
                print(e)  # save to logs exception with link to image
                continue

        print(images)
        return self._augmentImages(images)

    def _augmentImages(self, images):
        if not self.inputData[consts.Inputs.IS_AUGMENTATION]:
            return images

        print('augmentation')
        multiplicationLevel = self.inputData[consts.Inputs.AUGMENTATION_LEVEL]
        rotationLevel = self.inputData[consts.Inputs.ROTATION_LEVEL]
        sharpnessRange = self.inputData[consts.Inputs.SHARPNESS_MIN], self.inputData[consts.Inputs.SHARPNESS_MAX]
        contrastRange = self.inputData[consts.Inputs.CONTRAST_MIN], self.inputData[consts.Inputs.CONTRAST_MAX]
        brightnessRange = self.inputData[consts.Inputs.BRIGHTNESS_MIN], self.inputData[consts.Inputs.BRIGHTNESS_MAX]

        augmentedImages = []
        for idx, image in enumerate(images):
            image = image.convert('RGB')
            print(image)
            print(idx)
            augmentedImages.append(image)
            for i in range(1, multiplicationLevel):
                print(i)
                augmentedImage = image.rotate(random.uniform(-rotationLevel, rotationLevel) * 180)
                print('rotation')
                if self.inputData[consts.Inputs.IS_VERTICAL_FLIP] and bool(random.getrandbits(1)):
                    print('a')
                    augmentedImage = augmentedImage.transpose(Image.FLIP_TOP_BOTTOM)
                print('topbottom')
                if self.inputData[consts.Inputs.IS_HORIZONTAL_FLIP] and bool(random.getrandbits(1)):
                    augmentedImage = augmentedImage.transpose(Image.FLIP_LEFT_RIGHT)
                print('leftright')
                augmentedImage = ImageEnhance.Sharpness(augmentedImage).enhance(random.uniform(*sharpnessRange))
                print('sharpness')
                augmentedImage = ImageEnhance.Contrast(augmentedImage).enhance(random.uniform(*contrastRange))
                print('contrast')
                augmentedImage = ImageEnhance.Brightness(augmentedImage).enhance(random.uniform(*brightnessRange))
                print('bright')
                augmentedImages.append(augmentedImage)
                print('append')

        if self.inputData[consts.Inputs.SHUFFLE_IMAGES]:
            random.shuffle(augmentedImages)
        print('exit augm')
        return augmentedImages

    def _saveImages(self, images, entry, isGroupSearch=False):
        destinationDir = self.inputData[consts.Inputs.LOCAL_PATH] + '/'

        if isGroupSearch:
            destinationDir = destinationDir + self.inputData[consts.Inputs.GROUP_NAME] + '/'
            if not os.path.exists(destinationDir):
                os.mkdir(destinationDir)

        destinationDir = destinationDir + entry + '/'
        print(destinationDir)
        os.mkdir(destinationDir)
        print('dircreated')

        savedImagesCount = 0
        for img in images:
            img.save(f'{destinationDir}{entry}{savedImagesCount+1:03}.'
                     f'{self.inputData[consts.Inputs.IMAGE_FORMAT]}')
            savedImagesCount += 1

        return savedImagesCount
