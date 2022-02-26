import datetime
import edgar


def run():
    date = datetime.date.today()
    date = datetime.date(2022, 1, 27)

    while date >= datetime.date(2021, 1, 1):
        date = date - datetime.timedelta(days=1)
        edgar.downloadDate(date)

run()
