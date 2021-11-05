import os
import app.consts as consts


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
        elif consts.Inputs.IS_GROUP_SEARCH in self.inputData and self.inputData[consts.Inputs.IS_GROUP_SEARCH]:
            if consts.Inputs.GROUP_NAME not in self.inputData\
                    or not self.inputData[consts.Inputs.GROUP_NAME]:
                raise KeyError('Group name not defined.')
            if consts.Inputs.GROUP_SEARCH_ENTRIES not in self.inputData\
                    or not self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES]:
                raise KeyError('Search entries not defined.')
            self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES] =\
                [entry for entry in self.inputData[consts.Inputs.GROUP_SEARCH_ENTRIES].split(',') if entry]
        else:
            raise KeyError('Type of search not defined.')

        if consts.Inputs.IMAGE_FORMAT not in self.inputData\
                or self.inputData[consts.Inputs.IMAGE_FORMAT] not in [i.value for i in consts.ImageFormats]:
            raise KeyError('Image format not defined or not supported.')

        if consts.Inputs.IMAGE_HEIGHT not in self.inputData or not self.inputData[consts.Inputs.IMAGE_HEIGHT]\
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
        pass
