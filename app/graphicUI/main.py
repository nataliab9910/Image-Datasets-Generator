import sys

from PyQt5.QtWidgets import QApplication

from app.graphicUI.controller import GeneratorController
from app.graphicUI.view import GeneratorUi


def main():
    generator = QApplication(sys.argv)
    view = GeneratorUi()
    view.show()
    GeneratorController(view)
    sys.exit(generator.exec_())


if __name__ == '__main__':
    main()
