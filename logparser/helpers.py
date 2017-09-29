import boto3
import re
import sys

def match_date(url, date):
    """Helper function to determine if a date is contained in a given S3 URL.
    :param url: URL to check for date
    :param date: Date to match

    :returns: the verified date
    """

    # Use provided date as the pattern
    date_regex = re.escape(date)
    date_pattern = re.search(date_regex, url)
    if (date_pattern):
        print(date_pattern.group())
        print("Date valid")
        return date_pattern.group()
    else:
        print('No date found for ' + date)
        sys.exit(1)

# Helper function to dump out all logs that fall within a date range
def filter_s3_logs():
    return

