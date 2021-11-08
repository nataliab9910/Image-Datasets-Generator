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
        groupSearchLayout.addWidget(self.groupNameInputLine, 1, 1)
        groupSearchLayout.addWidget(QtWidgets.QLabel('Search entries (split by comma):'), 2, 0)
        self.groupSearchEntriesInputLine = QtWidgets.QLineEdit()
        groupSearchLayout.addWidget(self.groupSearchEntriesInputLine, 2, 1)

        groupSearchBox.setLayout(groupSearchLayout)
        searchLayout.addWidget(groupSearchBox)

        self.singleSearchCheck.clicked.connect(lambda: self._changedEnabledOptions(consts.SearchOptions.SINGLE_SEARCH))
        self.groupSearchCheck.clicked.connect(lambda: self._changedEnabledOptions(consts.SearchOptions.GROUP_SEARCH))

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
        additionalOptionsLayout.addWidget(self.keepRatioCheckbox, 2, 0)

        self.augmentationCheckbox = QtWidgets.QCheckBox()
        self.augmentationCheckbox.setText('Augmentation')
        additionalOptionsLayout.addWidget(self.augmentationCheckbox, 3, 0)

        additionalOptionsGroup.setLayout(additionalOptionsLayout)

        return additionalOptionsGroup

    def _prepareGenerateButton(self):
        self.generateButton = QtWidgets.QPushButton('Generate')
        self.generateButton.setFixedSize(100, 40)
        self.generateButton.clicked.connect(lambda: self.generateButton.setEnabled(False))

        return self.generateButton

    def _saveFile(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        self.pathLine.setText(path)

    def _changedEnabledOptions(self, toEnable):
        if toEnable == consts.SearchOptions.SINGLE_SEARCH:
            self.singleSearchInputLine.setReadOnly(False)
            self.groupNameInputLine.setText('')
            self.groupNameInputLine.setReadOnly(True)
            self.groupSearchEntriesInputLine.setText('')
            self.groupSearchEntriesInputLine.setReadOnly(True)
            self.groupSearchCheck.setChecked(False)
        elif toEnable == consts.SearchOptions.GROUP_SEARCH:
            self.groupNameInputLine.setReadOnly(False)
            self.groupSearchEntriesInputLine.setReadOnly(False)
            self.singleSearchInputLine.setText('')
            self.singleSearchInputLine.setReadOnly(True)
            self.singleSearchCheck.setChecked(False)

    def changeStatus(self, status):
        self.statusBarWidget.showMessage(status)

    def enableGenerateButton(self):
        self.generateButton.setEnabled(True)
