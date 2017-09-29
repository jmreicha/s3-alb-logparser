import click

from logparser import helpers

# Set up some defaults
bucket_name =  'techtest-alb-logs'
prefix = 'webservices/AWSLogs/158469572311/elasticloadbalancing/us-west-2/'
s3_url = prefix + '2017/08/01/158469572311_elasticloadbalancing_us-west-2_app.webservices.2f179337c6c8adb5_20170801T0000Z_54.148.145.231_2gqui3gc.log.gz'

# Click setup
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0')
def logparser():
    """Manage S3 logs."""


@logparser.command('getcodes')
@click.option('--from_date', is_flag=True, help='beginning date to filter')
@click.option('--to_date', is_flag=True, help='ending date to filter')
@click.option('--max_num', is_flag=True, help='max number of error codes to return')
def getcodes(from_date, to_date, max_num):
    helpers.match_date(s3_url, '2017/08/01')

    # Default output if no args are provided
    #click.echo('Nothing to parse.  Try adding filter dates.')


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

