import io
import os
import urllib.request
from time import sleep

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
            if self.inputData[consts.Inputs.IMAGE_HEIGHT] <= 0 or self.inputData[consts.Inputs.IMAGE_WIDTH] <= 0:
                raise ValueError
        except ValueError:
            raise KeyError('Provided image height or width is not valid.')

        if consts.Inputs.AUGMENTATION not in self.inputData:
            self.inputData[consts.Inputs.AUGMENTATION] = False

    def generateDataset(self):
        savedImagesNum = 0
        try:
            api = ApiProvider.getApi(self.inputData[consts.Inputs.SEARCH_ENGINE])
            if self.inputData[consts.Inputs.IS_SINGLE_SEARCH]:
                entry = self.inputData[consts.Inputs.SINGLE_SEARCH_ENTRY]
                images = api.getImages(entry)
                print(images)
                savedImagesNum += self._saveImages(images, entry)
            elif self.inputData[consts.Inputs.IS_GROUP_SEARCH]:
                for entry in self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES]:
                    images = api.getImages(entry)
                    savedImagesNum += self._saveImages(images, entry, True)
        except Exception:
            raise

        return savedImagesNum

    def _saveImages(self, images, entry, isGroupSearch=False):
        destinationDir = self.inputData[consts.Inputs.LOCAL_PATH] + '/'

        if isGroupSearch:
            destinationDir = destinationDir + self.inputData[consts.Inputs.GROUP_NAME] + '/'

        savedImagesCount = 0
        for index, imageUrl in enumerate(images):
            try:
                response = requests.get(imageUrl, timeout=10)
                if response.status_code == 200:
                    image_bytes = io.BytesIO(response.content)
                    with Image.open(image_bytes) as img:
                        print(index)
                        savedImagesCount += 1
                        if index == 34:
                            img.show()
            except Exception as e:
                print(imageUrl)
                print(e)
                continue

        return savedImagesCount



    def _augmentImage(self, image):
        pass
