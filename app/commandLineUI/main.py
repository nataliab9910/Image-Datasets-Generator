import app.commandLineUI.controller as controller


def main():
    print('Hello! Please, provide options of enter END to finish.')
    inputText = str(input())
    while inputText.upper() != 'END':
        controller.processInput(inputText)

        print('Please, provide options of enter END to finish.')
        inputText = str(input())


if __name__ == '__main__':
    main()
