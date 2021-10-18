import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, \
    QFileDialog, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QStatusBar


class GeneratorUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image datasets generator')
        self.setFixedWidth(500)
        self.layout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.layout)
        self._createInterface()

    def _createInterface(self):

        self.layout.addWidget(self._prepareSearchEngineGroup())
        self.layout.addWidget(self._preparePathGroup())
        self.layout.addWidget(self._prepareSearchBox())
        self.layout.addWidget(self._prepareAdditionalOptions())
        self.layout.addWidget(self._prepareGenerateButton(), alignment=Qt.AlignCenter)

        self.statusBarWidget = QStatusBar()
        self.setStatusBar(self.statusBarWidget)

    def _prepareSearchEngineGroup(self):
        searchEngineGroup = QGroupBox()
        searchEngineLayout = QHBoxLayout()
        searchEngineLayout.addWidget(QLabel('Search engine:'))
        self.searchEngineBox = QComboBox()
        self.searchEngineBox.addItems(['Google', 'Yahoo', 'Bing'])
        searchEngineLayout.addWidget(self.searchEngineBox)
        searchEngineGroup.setLayout(searchEngineLayout)

        return searchEngineGroup

    def _preparePathGroup(self):
        selectPathGroup = QGroupBox()
        selectPathLayout = QHBoxLayout()
        selectPathLayout.addWidget(QLabel('Local path:'))
        self.pathLine = QLineEdit()
        self.pathLine.setReadOnly(True)
        selectPathLayout.addWidget(self.pathLine)
        self.selectPathButton = QPushButton('Choose path...')
        self.selectPathButton.clicked.connect(self._saveFile)
        selectPathLayout.addWidget(self.selectPathButton)
        selectPathGroup.setLayout(selectPathLayout)

        return selectPathGroup

    def _prepareSearchBox(self):
        searchBox = QGroupBox()
        searchLayout = QVBoxLayout()

        singleSearchGroup = QGroupBox()
        singleSearchLayout = QGridLayout()

        self.singleSearchCheck = QCheckBox()
        self.singleSearchCheck.setText('Single search')
        singleSearchLayout.addWidget(self.singleSearchCheck, 0, 0)
        singleSearchLayout.addWidget(QLabel('Search entry:'), 1, 0)
        self.singleSearchInputLine = QLineEdit()
        singleSearchLayout.addWidget(self.singleSearchInputLine, 1, 1)

        singleSearchGroup.setLayout(singleSearchLayout)
        searchLayout.addWidget(singleSearchGroup)

        groupSearchGroup = QGroupBox()
        groupSearchLayout = QGridLayout()
        self.groupSearchCheck = QCheckBox()
        self.groupSearchCheck.setText('Group search')
        groupSearchLayout.addWidget(self.groupSearchCheck, 0, 0)
        groupSearchLayout.addWidget(QLabel('Group name:'), 1, 0)
        self.groupNameInputLine = QLineEdit()
        groupSearchLayout.addWidget(self.groupNameInputLine, 1, 1)
        groupSearchLayout.addWidget(QLabel('Search entries (split by comma):'), 2, 0)
        self.groupSearchEntriesInputLine = QLineEdit()
        groupSearchLayout.addWidget(self.groupSearchEntriesInputLine, 2, 1)

        groupSearchGroup.setLayout(groupSearchLayout)
        searchLayout.addWidget(groupSearchGroup)

        self.singleSearchCheck.clicked.connect(lambda: self._changedEnabledOptions('single'))
        self.groupSearchCheck.clicked.connect(lambda: self._changedEnabledOptions('group'))

        searchBox.setLayout(searchLayout)

        return searchBox

    def _prepareAdditionalOptions(self):
        additionalOptionsGroup = QGroupBox()
        additionalOptionsLayout = QGridLayout()

        additionalOptionsLayout.addWidget(QLabel('Desired images format:'), 0, 0)
        self.searchEngineBox = QComboBox()
        self.searchEngineBox.addItems(['png', 'jpg'])
        additionalOptionsLayout.addWidget(self.searchEngineBox, 0, 1, 1, 3)

        additionalOptionsLayout.addWidget(QLabel('Desired image resolution:'), 1, 0)
        self.imageWidthInput = QLineEdit()
        self.imageWidthInput.setText('100')
        additionalOptionsLayout.addWidget(self.imageWidthInput, 1, 1)
        additionalOptionsLayout.addWidget(QLabel('x'), 1, 2)
        self.imageHeightInput = QLineEdit()
        self.imageHeightInput.setText('100')
        additionalOptionsLayout.addWidget(self.imageHeightInput, 1, 3)

        self.augmentationCheckbox = QCheckBox()
        self.augmentationCheckbox.setText('Augmentation')
        additionalOptionsLayout.addWidget(self.augmentationCheckbox, 2, 0)

        additionalOptionsGroup.setLayout(additionalOptionsLayout)

        return additionalOptionsGroup

    def _prepareGenerateButton(self):
        self._generateButton = QPushButton('Generate')
        self._generateButton.setFixedSize(100, 40)
        self._generateButton.clicked.connect(lambda: self.changeStatus('In progress...'))
        self._generateButton.clicked.connect(lambda: self._generateButton.setEnabled(False))

        return self._generateButton

    def _saveFile(self):
        path = QFileDialog.getExistingDirectory(self, 'Select directory')
        self.pathLine.setText(path)

    def _changedEnabledOptions(self, toEnable):
        if toEnable == 'single':
            self.singleSearchInputLine.setReadOnly(False)
            self.groupNameInputLine.setText('')
            self.groupNameInputLine.setReadOnly(True)
            self.groupSearchEntriesInputLine.setText('')
            self.groupSearchEntriesInputLine.setReadOnly(True)
            self.groupSearchCheck.setChecked(False)
        elif toEnable == 'group':
            self.groupNameInputLine.setReadOnly(False)
            self.groupSearchEntriesInputLine.setReadOnly(False)
            self.singleSearchInputLine.setText('')
            self.singleSearchInputLine.setReadOnly(True)
            self.singleSearchCheck.setChecked(False)

    def changeStatus(self, status):
        self.statusBarWidget.showMessage(status)

    def enableGenerateButton(self):
        self._generateButton.setEnabled(True)


def main():
    generator = QApplication(sys.argv)
    view = GeneratorUi()
    view.show()
    sys.exit(generator.exec_())


if __name__ == '__main__':
    main()
