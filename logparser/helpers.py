# System
import re
import sys
import datetime
from collections import Counter
from dateutil import parser
from dateutil.rrule import rrule, DAILY
# 3rd party
import boto3
import smart_open

# AWS globals setup
bucket_name =  'techtest-alb-logs'
bucket_prefix = 'webservices/AWSLogs/158469572311/elasticloadbalancing/us-west-2/'

s3 = boto3.resource('s3')
client = boto3.client('s3')
bucket = s3.Bucket(name=bucket_name)

def normalize_date(date):
    """Helper function to get a normalized date to build an s3 URL."""

    date_obj = parser.parse(date)
    normal_date = datetime.date.strftime(date_obj, "%Y/%m/%d")

    # Check if there is a directory for the parsed date
    if (s3_directory_exists(bucket_name, bucket_prefix + normal_date)) is False:
        print("No logs available for " + normal_date)
        sys.exit(1)

    return normal_date


def s3_directory_exists(bucket, prefix):
    """Helper function to determine if a directory exists."""

    results = client.list_objects(Bucket=bucket, Prefix=prefix)
    return 'Contents' in results

def filter_s3_logs(from_date, to_date):
    """Helper function to dump out all logs that fall within a date range."""

    from_date_obj = parser.parse(from_date)
    to_date_obj = parser.parse(to_date)

    # TODO Handle out of order dates

    s3_log_urls = []
    # Loop over dates
    for single_date in rrule(DAILY, dtstart=from_date_obj, until=to_date_obj):
        # Make a URL and get logs for dates in range
        formatted_date = single_date.strftime("%Y/%m/%d")
        s3_dir = bucket_prefix + formatted_date + '/'
        for obj in bucket.objects.filter(Prefix=s3_dir):
            # Put the full url into the list
            s3_log_urls.append(bucket_name + '/' + obj.key)

    return s3_log_urls


def analyze_codes(*log_urls):
    """ Helper function to Read through log entries and calculate stats."""
    status_codes = []
    for url in log_urls:
        # Decode and read lines from the log files
        for line in smart_open.smart_open('s3://' + url):
            line = line.decode('utf-8')
            # Parse HTTPS codes - the position should always be the same
            line_parts = line.split(' ')
            status_codes.append(line_parts[8])

    return status_codes


def analyze_urls(log_urls, code):
    """ Helper function to Read through log entries and save urls."""
    url_in_log = []
    for url in log_urls:
        # Decode and read lines from the log files
        for line in smart_open.smart_open('s3://' + url):
            line = line.decode('utf-8')
            # Parse urls - only care about specific status codes
            line_parts = line.split(' ')
            # only parse for given status code
            if line_parts[8] == str(code):
                url_in_log.append(line_parts[13])

    return url_in_log


def analyze_uas(log_urls, code):
    """ Helper function to Read through log entries and save useragents."""
    user_agents = []
    for url in log_urls:
        # Decode and read lines from the log files
        for line in smart_open.smart_open('s3://' + url):
            line = line.decode('utf-8')
            # Parse user agents - need to regex for some user agents
            line_parts = line.split(' ')
            # only parse for given status code
            if line_parts[8] == str(code):
                # I'm so sorry
                match = re.search(r'\"[^\"]+\"[^\"]+\"(?P<agent>[^\"]*)\"', line)
                ua = match.group(1)
                user_agents.append(ua)

    return user_agents

# TODO Make this do all the analysis

def log_report(log_urls, max_num):
    """ Helper function to Read through log entries and save useful info."""
    status_codes = []
    url_in_log = []
    user_agents = []
    line_counter = 0
    for url in log_urls:
        # Decode and read lines from the log files
        for line in smart_open.smart_open('s3://' + url):
            line = line.decode('utf-8')
            line_parts = line.split(' ')
            # count lines
            line_counter += 1
            # count status codes
            status_codes.append(line_parts[8])
            # count urls
            url_in_log.append(line_parts[13])
            # count user agents
            match = re.search(r'\"[^\"]+\"[^\"]+\"(?P<agent>[^\"]*)\"', line)
            ua = match.group(1)
            user_agents.append(ua)
            #print(line)

    # Find top N stats
    status_counter = Counter(status_codes)
    top_statuses = status_counter.most_common(max_num)
    url_counter = Counter(url_in_log)
    top_urls = url_counter.most_common(max_num)
    agent_counter = Counter(user_agents)
    top_agents = agent_counter.most_common(max_num)

    # Just overwrite the logfile every time
    with open('/tmp/logreport.txt', 'w') as logreport:
        logreport.write(str(len(log_urls)) + ' log files analyzed\n')
        logreport.write(str(line_counter) + ' log lines analyzed\n')
        logreport.write('\n')
        # Status codes
        logreport.write('Top ' + str(max_num) + ' status codes\n\n')
        logreport.write('\n'.join('%s %s' % x for x in top_statuses))
        logreport.write('\n\n')
        # URLs
        logreport.write('Top ' + str(max_num) + ' urls\n\n')
        logreport.write('\n'.join('%s %s' % x for x in top_urls))
        logreport.write('\n\n')
        # User agents
        logreport.write('Top ' + str(max_num) + ' user agents\n\n')
        logreport.write('\n'.join('%s %s' % x for x in top_agents))
        logreport.write('\n\n')

