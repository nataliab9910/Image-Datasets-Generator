import app.consts as consts

from app.exceptionLogger import exceptionLogSave
from app.generator import Generator
from app.graphicUI.view import GeneratorUi


class GeneratorController:
    def __init__(self, view: GeneratorUi):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.generateButton.clicked.connect(lambda: self.processInputData())

    def processInputData(self):
        inputData = {
            consts.Inputs.SEARCH_ENGINE: self._view.searchEngineBox.currentText(),
            consts.Inputs.LOCAL_PATH: self._view.pathLine.text(),
            consts.Inputs.IS_SINGLE_SEARCH: self._view.singleSearchCheck.isChecked(),
            consts.Inputs.SINGLE_SEARCH_ENTRY: self._view.singleSearchInputLine.text(),
            consts.Inputs.IS_GROUP_SEARCH: self._view.groupSearchCheck.isChecked(),
            consts.Inputs.GROUP_NAME: self._view.groupNameInputLine.text(),
            consts.Inputs.GROUP_SEARCH_ENTRIES: self._view.groupSearchEntriesInputLine.text(),
            consts.Inputs.IMAGE_FORMAT: self._view.imageFormatBox.currentText(),
            consts.Inputs.IMAGE_WIDTH: self._view.imageWidthInput.text(),
            consts.Inputs.IMAGE_HEIGHT: self._view.imageHeightInput.text(),
            consts.Inputs.IS_AUGMENTATION: self._view.augmentationCheckbox.isChecked(),
            consts.Inputs.AUGMENTATION_LEVEL: self._view.augmentationLevelInput.text(),
            consts.Inputs.IS_HORIZONTAL_FLIP: self._view.horizontalFlipCheckbox.isChecked(),
            consts.Inputs.IS_VERTICAL_FLIP: self._view.verticalFLipCheckbox.isChecked(),
            consts.Inputs.ROTATION_LEVEL: self._view.rotationLevelInput.text(),
            consts.Inputs.SHARPNESS_MIN: self._view.sharpnessMinInput.text(),
            consts.Inputs.SHARPNESS_MAX: self._view.sharpnessMaxInput.text(),
            consts.Inputs.CONTRAST_MIN: self._view.contrastMinInput.text(),
            consts.Inputs.CONTRAST_MAX: self._view.contrastMaxInput.text(),
            consts.Inputs.BRIGHTNESS_MIN: self._view.brightnessMinInput.text(),
            consts.Inputs.BRIGHTNESS_MAX: self._view.brightnessMaxInput.text(),
            consts.Inputs.SHUFFLE_IMAGES: self._view.shuffleImagesCheckbox.isChecked()
        }
        try:
            self.generateAction(inputData)
            self._view.enableGenerateButton()
        except Exception as e:
            exceptionLogSave(e)
            self._view.changeStatus('Sorry, something unexpected happened :(')
            self._view.enableGenerateButton()

    def generateAction(self, inputData):
        generator = Generator(inputData)

        try:
            generator.validateInputs()
            savedImagesCount = generator.generateDataset()
            self._view.changeStatus(f'Collected {savedImagesCount} images!')
        except (KeyError, NotADirectoryError, ValueError) as e:
            exceptionLogSave(e)
            self._view.changeStatus(str(e))
            self._view.enableGenerateButton()
            return
        except Exception as e:
            exceptionLogSave(e)
            self._view.changeStatus('Unexpected error happened.')
            raise


