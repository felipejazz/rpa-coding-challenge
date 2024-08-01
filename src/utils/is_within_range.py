from .month_diff import month_diff
import datetime

MONTHS = {
    'Jan.': 1, 'Feb.': 2, 'Mar.': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'Aug.': 8, 'Sept.': 9, 'Oct.': 10, 'Nov.': 11, 'Dec.': 12
}

def parse_date(date_str: str) -> datetime.datetime:
    for month_name, month_number in MONTHS.items():
        if month_name in date_str:

            month = month_number
            day_year = date_str.split(month_name)[1].strip()
            day, year = day_year.split(', ')
            return datetime.datetime(year=int(year), month=month, day=int(day))
    raise ValueError(f"Invalid date format: {date_str}")
def is_within_range(date_str, month_range):
    try:
        news_date = parse_date(date_str)

        current_date = datetime.datetime.now()


        diff = month_diff(news_date, current_date)

        if 0 <= diff <= month_range:

            return True

        return False
    except ValueError:

        return False