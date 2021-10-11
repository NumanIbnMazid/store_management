from django.test import TestCase
import datetime
import dateutil
# import timezone

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 12, 31)

time_delta = datetime.timedelta(days=1)

while start_date <= end_date:
    print(start_date.strftime("%A"))
    start_date += time_delta
