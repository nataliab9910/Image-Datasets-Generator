from datetime import datetime

import app.consts as consts

DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


def exceptionLogSave(exception, additionalInfo = None):
    with open(consts.DEFAULT_ERROR_LOG_FILE, 'a') as file:
        file.write(f'[{datetime.now().strftime(DATE_FORMAT)}] An exception occured :(\n'
                   f'Type: {type(exception).__name__}\n'
                   f'Message: {str(exception)}\n')
        if additionalInfo is not None:
            file.write(f'Info: {str(additionalInfo)}\n')
        file.write('\n')
