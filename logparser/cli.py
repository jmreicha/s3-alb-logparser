import click
import time
from collections import Counter
from logparser import helpers

# Set up some defaults
bucket_name =  'techtest-alb-logs'
bucket_prefix = 'webservices/AWSLogs/158469572311/elasticloadbalancing/us-west-2/'

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

    # Check if there is a directory for the parsed date
    if (helpers.s3_directory_exists(bucket_name, bucket_prefix + from_date)) is False:
        print("No logs for " + from_date)
        exit(0)
    if (helpers.s3_directory_exists(bucket_name, bucket_prefix + to_date)) is False:
        print("No logs for " + to_date)
        exit(0)

    print('Collecting ALB logs for ' + from_date + ' - ' + to_date)

    # TODO Add  a progress bar
    # Iterate over dates in range and get all the logs
    logs = helpers.filter_s3_logs(from_date, to_date)
    print('Analyzing status codes for ' + str(len(logs)) + ' log files')
    print('This could take awhile ...')
    time.sleep(5)

    # Filter status codes
    statuses= helpers.analyze_codes(*logs)
    counter = Counter(statuses)

    print("Status codes")
    print(counter.most_common(max_num))


@logparser.command('geturls')
@click.option('--code', is_flag=True, help='error code to filter')
@click.option('--from_date', is_flag=True, help='beginning date to filter')
@click.option('--to_date', is_flag=True, help='ending date to filter')
@click.option('--for_date', is_flag=True, help='relative date to filter')
@click.option('--max_num', is_flag=True, help='max number of error codes to return')
def geturls(code, from_date, to_date, for_date, max_num):

    # Default output if no args are provided
    click.echo('Nothing to parse.  Try adding filter dates.')


@logparser.command('getuas')
@click.option('--code', is_flag=True, help='error code to filter')
@click.option('--from_date', is_flag=True, help='beginning date to filter')
@click.option('--to_date', is_flag=True, help='ending date to filter')
@click.option('--for_date', is_flag=True, help='relative date to filter')
@click.option('--max_num', is_flag=True, help='max number of error codes to return')
def getuas(code, from_date, to_date, for_date, max_num):

    # Default output if no args are provided
    click.echo('Nothing to parse.  Try adding filter dates.')


@logparser.command('getreport')
@click.option('--from_date', is_flag=True, help='beginning date to filter')
@click.option('--to_date', is_flag=True, help='ending date to filter')
@click.option('--for_date', is_flag=True, help='relative date to filter')
@click.option('--max_num', is_flag=True, help='max number of error codes to return')
def getuas(from_date, to_date, for_date, max_num):

    # Default output if no args are provided
    click.echo('Nothing to parse.  Try adding filter dates.')


if __name__ == '__main__':
    logparser()

