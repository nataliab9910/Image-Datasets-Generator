from app.view import GeneratorUi
import app.consts as consts
from app.generator import Generator


class GeneratorController:
    def __init__(self, view: GeneratorUi):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.generateButton.clicked.connect(lambda: self.collectInputData())

    def collectInputData(self):
        self._view.changeStatus('Collecting inputs...')
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
            consts.Inputs.AUGMENTATION: self._view.augmentationCheckbox.isChecked()
        }
        self.processInputData(inputData)

    def processInputData(self, inputData):
        generator = Generator(inputData)
        self._view.changeStatus('Processing inputs...')
