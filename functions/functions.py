from loader import logsDirect
import re
from datetime import datetime, date, time, timedelta

# check time difference between time.now() and last line in logs
def timeDifferenceMoreThanTen():
    # open log
    with open(logsDirect, 'r') as file:
        # get last line time
        lastLineDate = datetime.strptime(re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}', file.read())[-1].replace('T', ' '),'%Y-%m-%d %H:%M:%S.%f')
        timeDifference = datetime.now() - lastLineDate
        if timeDifference.seconds < 600:
            return False
        else:
            return True