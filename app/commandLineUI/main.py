from app.commandLineUI.controller import CliGeneratorController


def main():
    generatorController = CliGeneratorController()
    print('Hello! Please, provide options or enter END to finish.')
    inputText = str(input())
    while inputText.upper() != 'END':
        generatorController.processInput(inputText)

        print('Please, provide options of enter END to finish.')
        inputText = str(input())


if __name__ == '__main__':
    main()
