from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets

import app.consts as consts


class GeneratorUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image datasets generator')
        self.setFixedWidth(500)
        self.layout = QtWidgets.QVBoxLayout()
        self._centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.layout)
        self._createInterface()

    def _createInterface(self):
        self.layout.addWidget(self._prepareSearchEngineGroup())
        self.layout.addWidget(self._preparePathGroup())
        self.layout.addWidget(self._prepareSearchBox())
        self.layout.addWidget(self._prepareAdditionalOptions())
        self.layout.addWidget(self._prepareAugmentationOptions())
        self.layout.addWidget(self._prepareGenerateButton(), alignment=Qt.AlignCenter)

        self.statusBarWidget = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBarWidget)

    def _prepareSearchEngineGroup(self):
        searchEngineGroup = QtWidgets.QGroupBox()
        searchEngineLayout = QtWidgets.QHBoxLayout()
        searchEngineLayout.addWidget(QtWidgets.QLabel('Search engine:'))
        self.searchEngineBox = QtWidgets.QComboBox()
        self.searchEngineBox.addItems([searchEngine.value for searchEngine in consts.SearchEngines])
        searchEngineLayout.addWidget(self.searchEngineBox)
        searchEngineGroup.setLayout(searchEngineLayout)

        return searchEngineGroup

    def _preparePathGroup(self):
        selectPathGroup = QtWidgets.QGroupBox()
        selectPathLayout = QtWidgets.QHBoxLayout()
        selectPathLayout.addWidget(QtWidgets.QLabel('Local path:'))
        self.pathLine = QtWidgets.QLineEdit()
        self.pathLine.setReadOnly(True)
        selectPathLayout.addWidget(self.pathLine)
        self.selectPathButton = QtWidgets.QPushButton('Choose path...')
        self.selectPathButton.clicked.connect(self._saveFile)
        selectPathLayout.addWidget(self.selectPathButton)
        selectPathGroup.setLayout(selectPathLayout)

        return selectPathGroup

    def _prepareSearchBox(self):
        searchBox = QtWidgets.QGroupBox()
        searchLayout = QtWidgets.QVBoxLayout()

        singleSearchBox = QtWidgets.QGroupBox()
        singleSearchLayout = QtWidgets.QGridLayout()

        self.singleSearchCheck = QtWidgets.QCheckBox()
        self.singleSearchCheck.setText('Single search')
        singleSearchLayout.addWidget(self.singleSearchCheck, 0, 0)
        singleSearchLayout.addWidget(QtWidgets.QLabel('Search entry:'), 1, 0)
        self.singleSearchInputLine = QtWidgets.QLineEdit()
        self.singleSearchInputLine.setEnabled(False)
        singleSearchLayout.addWidget(self.singleSearchInputLine, 1, 1)

        singleSearchBox.setLayout(singleSearchLayout)
        searchLayout.addWidget(singleSearchBox)

        groupSearchBox = QtWidgets.QGroupBox()
        groupSearchLayout = QtWidgets.QGridLayout()

        self.groupSearchCheck = QtWidgets.QCheckBox()
        self.groupSearchCheck.setText('Group search')
        groupSearchLayout.addWidget(self.groupSearchCheck, 0, 0)
        groupSearchLayout.addWidget(QtWidgets.QLabel('Group name:'), 1, 0)
        self.groupNameInputLine = QtWidgets.QLineEdit()
        self.groupNameInputLine.setEnabled(False)
        groupSearchLayout.addWidget(self.groupNameInputLine, 1, 1)
        groupSearchLayout.addWidget(QtWidgets.QLabel('Search entries (split by comma):'), 2, 0)
        self.groupSearchEntriesInputLine = QtWidgets.QLineEdit()
        self.groupSearchEntriesInputLine.setEnabled(False)
        groupSearchLayout.addWidget(self.groupSearchEntriesInputLine, 2, 1)

        groupSearchBox.setLayout(groupSearchLayout)
        searchLayout.addWidget(groupSearchBox)

        self.singleSearchCheck.clicked.connect(lambda: self._changedEnabledSearchOptions(consts.SearchOptions.SINGLE_SEARCH))
        self.groupSearchCheck.clicked.connect(lambda: self._changedEnabledSearchOptions(consts.SearchOptions.GROUP_SEARCH))

        searchBox.setLayout(searchLayout)

        return searchBox

    def _prepareAdditionalOptions(self):
        additionalOptionsGroup = QtWidgets.QGroupBox()
        additionalOptionsLayout = QtWidgets.QGridLayout()

        additionalOptionsLayout.addWidget(QtWidgets.QLabel('Desired images format:'), 0, 0)
        self.imageFormatBox = QtWidgets.QComboBox()
        self.imageFormatBox.addItems([imageFormat.value for imageFormat in consts.ImageFormats])
        additionalOptionsLayout.addWidget(self.imageFormatBox, 0, 1, 1, 3)

        additionalOptionsLayout.addWidget(QtWidgets.QLabel('Desired image resolution:'), 1, 0)
        self.imageWidthInput = QtWidgets.QLineEdit()
        self.imageWidthInput.setText(str(consts.DEFAULT_IMAGE_WIDTH))
        additionalOptionsLayout.addWidget(self.imageWidthInput, 1, 1)
        additionalOptionsLayout.addWidget(QtWidgets.QLabel('x'), 1, 2)
        self.imageHeightInput = QtWidgets.QLineEdit()
        self.imageHeightInput.setText(str(consts.DEFAULT_IMAGE_HEIGHT))
        additionalOptionsLayout.addWidget(self.imageHeightInput, 1, 3)

        self.keepRatioCheckbox = QtWidgets.QCheckBox()
        self.keepRatioCheckbox.setText('Keep original image ratio')
        additionalOptionsLayout.addWidget(self.keepRatioCheckbox, 2, 0, 1, 2)

        additionalOptionsGroup.setLayout(additionalOptionsLayout)

        return additionalOptionsGroup

    def _prepareAugmentationOptions(self):
        augmentationOptionsGroup = QtWidgets.QGroupBox()
        augmentationOptionsLayout = QtWidgets.QGridLayout()

        lineNumber = 1
        self.augmentationCheckbox = QtWidgets.QCheckBox()
        self.augmentationCheckbox.setText('Augmentation')
        augmentationOptionsLayout.addWidget(self.augmentationCheckbox, lineNumber, 0)
        self.augmentationCheckbox.clicked.connect(lambda: self._changedEnabledAugmetationOptions(self.augmentationCheckbox.isChecked()))

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('Augmentation level (2-50):'), lineNumber, 0)
        self.augmentationLevelInput = QtWidgets.QLineEdit()
        self.augmentationLevelInput.setText(str(consts.DEFAULT_AUGMENTATION_LEVEL))
        self.augmentationLevelInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.augmentationLevelInput, lineNumber, 1)

        lineNumber += 1
        self.horizontalFlipCheckbox = QtWidgets.QCheckBox()
        self.horizontalFlipCheckbox.setText('Horizontal flip')
        self.horizontalFlipCheckbox.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.horizontalFlipCheckbox, lineNumber, 0)
        self.verticalFLipCheckbox = QtWidgets.QCheckBox()
        self.verticalFLipCheckbox.setText('Vertical flip')
        self.verticalFLipCheckbox.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.verticalFLipCheckbox, lineNumber, 1)

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('Rotation level (0-1)*:'), lineNumber, 0)
        self.rotationLevelInput = QtWidgets.QLineEdit()
        self.rotationLevelInput.setText(str(consts.DEFAULT_ROTATION_LEVEL))
        self.rotationLevelInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.rotationLevelInput, lineNumber, 1)

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('Sharpness range (0-2)**:'), lineNumber, 0)
        self.sharpnessMinInput = QtWidgets.QLineEdit()
        self.sharpnessMinInput.setText(str(consts.DEFAULT_SHARPNESS_MIN))
        self.sharpnessMinInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.sharpnessMinInput, lineNumber, 1)
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('-'), lineNumber, 2)
        self.sharpnessMaxInput = QtWidgets.QLineEdit()
        self.sharpnessMaxInput.setText(str(consts.DEFAULT_SHARPNESS_MAX))
        self.sharpnessMaxInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.sharpnessMaxInput, lineNumber, 3)

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('Contrast range (0-2)**:'), lineNumber, 0)
        self.contrastMinInput = QtWidgets.QLineEdit()
        self.contrastMinInput.setText(str(consts.DEFAULT_CONTRAST_MIN))
        self.contrastMinInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.contrastMinInput, lineNumber, 1)
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('-'), lineNumber, 2)
        self.contrastMaxInput = QtWidgets.QLineEdit()
        self.contrastMaxInput.setText(str(consts.DEFAULT_CONTRAST_MAX))
        self.contrastMaxInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.contrastMaxInput, lineNumber, 3)

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('Brightness range (0-2)**:'), lineNumber, 0)
        self.brightnessMinInput = QtWidgets.QLineEdit()
        self.brightnessMinInput.setText(str(consts.DEFAULT_BRIGHTNESS_MIN))
        self.brightnessMinInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.brightnessMinInput, lineNumber, 1)
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('-'), lineNumber, 2)
        self.brightnessMaxInput = QtWidgets.QLineEdit()
        self.brightnessMaxInput.setText(str(consts.DEFAULT_BRIGHTNESS_MAX))
        self.brightnessMaxInput.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.brightnessMaxInput, lineNumber, 3)

        lineNumber += 1
        self.shuffleImagesCheckbox = QtWidgets.QCheckBox()
        self.shuffleImagesCheckbox.setText('Shuffle images')
        self.shuffleImagesCheckbox.setEnabled(False)
        augmentationOptionsLayout.addWidget(self.shuffleImagesCheckbox, lineNumber, 0)

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('* 0.0 means no change, 1.0 means 180 degrees rotation'), lineNumber, 0, 1, 2)

        lineNumber += 1
        augmentationOptionsLayout.addWidget(QtWidgets.QLabel('** 1.0 means no change'), lineNumber, 0)

        augmentationOptionsGroup.setLayout(augmentationOptionsLayout)

        return augmentationOptionsGroup

    def _prepareGenerateButton(self):
        self.generateButton = QtWidgets.QPushButton('Generate')
        self.generateButton.setFixedSize(100, 40)
        self.generateButton.clicked.connect(lambda: self.generateButton.setEnabled(False))

        return self.generateButton

    def _saveFile(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        self.pathLine.setText(path)

    def _changedEnabledSearchOptions(self, toEnable):
        if toEnable == consts.SearchOptions.SINGLE_SEARCH:
            self.singleSearchInputLine.setEnabled(True)
            self.groupNameInputLine.setEnabled(False)
            self.groupSearchEntriesInputLine.setEnabled(False)
            self.groupSearchCheck.setChecked(False)
        elif toEnable == consts.SearchOptions.GROUP_SEARCH:
            self.groupNameInputLine.setEnabled(True)
            self.groupSearchEntriesInputLine.setEnabled(True)
            self.singleSearchInputLine.setEnabled(False)
            self.singleSearchCheck.setChecked(False)

    def _changedEnabledAugmetationOptions(self, isChecked):
        if isChecked:
            self.augmentationLevelInput.setEnabled(True)
            self.horizontalFlipCheckbox.setEnabled(True)
            self.verticalFLipCheckbox.setEnabled(True)
            self.rotationLevelInput.setEnabled(True)
            self.sharpnessMinInput.setEnabled(True)
            self.sharpnessMaxInput.setEnabled(True)
            self.contrastMinInput.setEnabled(True)
            self.contrastMaxInput.setEnabled(True)
            self.brightnessMinInput.setEnabled(True)
            self.brightnessMaxInput.setEnabled(True)
            self.shuffleImagesCheckbox.setEnabled(True)

        else:
            self.augmentationLevelInput.setEnabled(False)
            self.horizontalFlipCheckbox.setEnabled(False)
            self.verticalFLipCheckbox.setEnabled(False)
            self.rotationLevelInput.setEnabled(False)
            self.sharpnessMinInput.setEnabled(False)
            self.sharpnessMaxInput.setEnabled(False)
            self.contrastMinInput.setEnabled(False)
            self.contrastMaxInput.setEnabled(False)
            self.brightnessMinInput.setEnabled(False)
            self.brightnessMaxInput.setEnabled(False)
            self.shuffleImagesCheckbox.setEnabled(False)

    def changeStatus(self, status):
        self.statusBarWidget.showMessage(status)

    def enableGenerateButton(self):
        self.generateButton.setEnabled(True)
