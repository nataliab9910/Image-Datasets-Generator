import io
import numpy as np
import os
import requests
from PIL import Image

import app.consts as consts
from app.api import ApiProvider


class Generator:
    def __init__(self, inputData):
        self.inputData = inputData

    def validateInputs(self):
        if consts.Inputs.SEARCH_ENGINE not in self.inputData \
                or self.inputData[consts.Inputs.SEARCH_ENGINE] not in [i.value for i in consts.SearchEngines]:
            raise KeyError('Search engine not defined or not supported.')

        if consts.Inputs.LOCAL_PATH not in self.inputData \
                or not os.path.isdir(self.inputData[consts.Inputs.LOCAL_PATH]):
            raise NotADirectoryError('Output directory is not defined or not valid.')

        if consts.Inputs.IS_SINGLE_SEARCH in self.inputData and self.inputData[consts.Inputs.IS_SINGLE_SEARCH]:
            if consts.Inputs.SINGLE_SEARCH_ENTRY not in self.inputData \
                    or not self.inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]:
                raise KeyError('Search entry not defined.')
            destinationDirectory = self.inputData[consts.Inputs.LOCAL_PATH] \
                + '/' \
                + self.inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]
            if os.path.isdir(destinationDirectory) and os.listdir(destinationDirectory):
                raise ValueError(f'Directory {destinationDirectory} already exists and is not empty.')
        elif consts.Inputs.IS_GROUP_SEARCH in self.inputData and self.inputData[consts.Inputs.IS_GROUP_SEARCH]:
            if consts.Inputs.GROUP_NAME not in self.inputData \
                    or not self.inputData[consts.Inputs.GROUP_NAME]:
                raise KeyError('Group name not defined.')
            if consts.Inputs.GROUP_SEARCH_ENTRIES not in self.inputData \
                    or not self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES]:
                raise KeyError('Search entries not defined.')
            self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES] = \
                [entry for entry in self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES].split(',') if entry]
        else:
            raise KeyError('Type of search not defined.')

        if consts.Inputs.IMAGE_FORMAT not in self.inputData \
                or self.inputData[consts.Inputs.IMAGE_FORMAT] not in [i.value for i in consts.ImageFormats]:
            raise KeyError('Image format not defined or not supported.')

        if consts.Inputs.IMAGE_HEIGHT not in self.inputData or not self.inputData[consts.Inputs.IMAGE_HEIGHT] \
                or consts.Inputs.IMAGE_WIDTH not in self.inputData or not self.inputData[consts.Inputs.IMAGE_HEIGHT]:
            raise KeyError('Image height or width not defined.')

        try:
            self.inputData[consts.Inputs.IMAGE_HEIGHT] = int(self.inputData[consts.Inputs.IMAGE_HEIGHT])
            self.inputData[consts.Inputs.IMAGE_WIDTH] = int(self.inputData[consts.Inputs.IMAGE_WIDTH])
        except ValueError:
            raise KeyError('Provided image height or width is not valid.')

        if not 0 < self.inputData[consts.Inputs.IMAGE_HEIGHT] <= consts.MAX_IMAGE_SIZE \
                or not 0 < self.inputData[consts.Inputs.IMAGE_WIDTH] <= consts.MAX_IMAGE_SIZE:
            raise ValueError(f'Provided image height and width should be higher than 0 and less than or equal '
                             f'{consts.MAX_IMAGE_SIZE}.')

        if consts.Inputs.KEEP_RATIO not in self.inputData:
            self.inputData[consts.Inputs.KEEP_RATIO] = False

        if consts.Inputs.AUGMENTATION not in self.inputData:
            self.inputData[consts.Inputs.AUGMENTATION] = False

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

        return self._augmentImages(images)

    def _augmentImages(self, images):
        return images

    def _saveImages(self, images, entry, isGroupSearch=False):
        destinationDir = self.inputData[consts.Inputs.LOCAL_PATH] + '/'

        if isGroupSearch:
            destinationDir = destinationDir + self.inputData[consts.Inputs.GROUP_NAME] + '/'

        destinationDir = destinationDir + entry + '/'
        os.mkdir(destinationDir)

        savedImagesCount = 0
        for img in images:
            img.save(f'{destinationDir}{entry}{savedImagesCount+1:03}.'
                     f'{self.inputData[consts.Inputs.IMAGE_FORMAT]}')
            savedImagesCount += 1

        return savedImagesCount
