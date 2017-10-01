import click
import sys
import time
from collections import Counter
from logparser import helpers

# Click setup
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0')
def logparser():
    """Manage S3 logs."""

# TODO add a flag to toggle on realtime streaming of logs

@logparser.command('getcodes')
@click.option('--from_date', help='beginning date to filter')
@click.option('--to_date', help='ending date to filter')
@click.option('--max_num', default=10, help='max number of error codes to return - 10 is default')
def getcodes(from_date, to_date, max_num):
    # Check that we get the date formatted correctly
    from_date = helpers.normalize_date(from_date)
    to_date = helpers.normalize_date(to_date)
    print('Collecting ALB logs for ' + from_date + ' - ' + to_date)
    # Iterate over dates in range and get all the logs
    logs = helpers.filter_s3_logs(from_date, to_date)
    print('Analyzing status codes for ' + str(len(logs)) + ' log files')
    print('This could take awhile ...')
    time.sleep(5)

    # Filter status codes
    statuses = helpers.analyze_codes(*logs)
    status_counter = Counter(statuses)

    print('Top ' + str(max_num) + ' status codes')
    print(status_counter.most_common(max_num))


@logparser.command('geturls')
@click.option('--code', default=404, help='error code to filter')
@click.option('--for_date', is_flag=True, help='relative date to filter')
@click.option('--from_date', help='beginning date to filter')
@click.option('--to_date', help='ending date to filter')
@click.option('--max_num', default=10, help='max number of error codes to return - 10 is default')
def geturls(code, from_date, to_date, for_date, max_num):
    # Check that we get the date formatted correctly
    from_date = helpers.normalize_date(from_date)
    to_date = helpers.normalize_date(to_date)
    print('Collecting ALB logs for ' + from_date + ' - ' + to_date)
    # Iterate over dates in range and get all the logs
    logs = helpers.filter_s3_logs(from_date, to_date)
    print('Analyzing urls for status code ' + str(code))
    print('This could take awhile ...')
    time.sleep(5)

    urls = helpers.analyze_urls(logs, code)
    url_counter = Counter(urls)

    print('Top ' + str(max_num) + ' urls for ' + str(code) + ' status code')
    print(url_counter.most_common(max_num))


@logparser.command('getuas')
@click.option('--code', default=404, help='error code to filter')
@click.option('--for_date', is_flag=True, help='relative date to filter')
@click.option('--from_date', help='beginning date to filter')
@click.option('--to_date', help='ending date to filter')
@click.option('--max_num', default=10, help='max number of error codes to return - 10 is default')
def getuas(code, from_date, to_date, for_date, max_num):
    # Check that we get the date formatted correctly
    from_date = helpers.normalize_date(from_date)
    to_date = helpers.normalize_date(to_date)
    print('Collecting ALB logs for ' + from_date + ' - ' + to_date)
    # Iterate over dates in range and get all the logs
    logs = helpers.filter_s3_logs(from_date, to_date)
    print('Analyzing user agents for ' + str(code) + ' status codes')
    print('This could take awhile ...')
    time.sleep(5)

    user_agents = helpers.analyze_uas(logs, code)
    agent_counter = Counter(user_agents)

    print('Top ' + str(max_num) + ' user agents for ' + str(code) + ' status code')
    print(agent_counter.most_common(max_num))


@logparser.command('getreport')
@click.option('--for_date', is_flag=True, help='relative date to filter')
@click.option('--from_date', help='beginning date to filter')
@click.option('--to_date', help='ending date to filter')
@click.option('--max_num', default=10, help='max number of error codes to return - 10 is default')
def getreport(from_date, to_date, for_date, max_num):
    # Check that we get the date formatted correctly
    from_date = helpers.normalize_date(from_date)
    to_date = helpers.normalize_date(to_date)
    print('Collecting ALB logs for ' + from_date + ' - ' + to_date)
    # Iterate over dates in range and get all the logs
    logs = helpers.filter_s3_logs(from_date, to_date)
    print('Analyzing top ' + str(max_number) + ' log results for ' + from_date + ' - ' + to_date)
    print('This could take awhile ...')
    time.sleep(5)

    # Get stats
    statuses = helpers.analyze_codes(*logs)
    status_counter = Counter(statuses)
    top_statuses = status_counter.most_common(max_num)
    #urls = helpers.analyze_urls(logs, code)
    #url_counter = Counter(urls)
    #top_urls = url_counter.most_common(max_num)
    #user_agents = helpers.analyze_uas(logs, code)
    #agent_counter = Counter(user_agents)
    #top_agents = agent_counter.most_common(max_num)

    # Just overwrite the logfile every time
    with open('/tmp/logreport.csv', 'w') as logreport:
        wr = csv.writer(logreport, quoting=csv.QUOTE_ALL)
        # Top error codes
        wr.writerow('Top status codes', top_statuses)
        # Top urls
        #wr.writerow('Top urls', top_urls)
        # Top user agents
        #wr.writerow('Top user agents', top_agents)
        # Total log files
        #wr.writerow('Log files analyzed', len(logs))

    print('log report written to /tmp/logreport.csv')

if __name__ == '__main__':
    logparser()

