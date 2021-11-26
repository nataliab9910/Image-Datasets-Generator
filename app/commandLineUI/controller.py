from app import consts
from app.exceptionLog import exceptionLogSave
from app.generator import Generator


def processInput(inputText):
    print('Processing your inputs...')
    inputData = _getInputArray(inputText)
    generator = Generator(inputData)

    try:
        generator.validateInputs()
        print('Generating dataset...')
        savedImagesCount = generator.generateDataset(isCli=True)
        print(f'Collected {savedImagesCount} images!')
    except (KeyError, NotADirectoryError, ValueError) as e:
        exceptionLogSave(e)
        print(str(e))
        return
    except Exception as e:
        exceptionLogSave(e)
        print('Unexpected error happened.')
        raise


def _getInputArray(inputText):
    validKeys = [item.value for item in consts.Inputs]

    result = {}
    for option in inputText.split(';'):
        key, value = option.split(':', 1)
        if key not in validKeys:
            raise KeyError(f'Provided key is not valid: {key}')
        result[consts.Inputs(key)] = value

    return result
