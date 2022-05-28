import io
import os
import sys

from pythontool.conf.airflow.utils import dates
from pythontool.conf.configration.configuration import conf


def show_config():
    """Show current application configuration"""
    with io.StringIO() as output:
        conf.write(output)
        code = output.getvalue()
        print(code)


if __name__ == '__main__':
    print("world###########################################################")
    print(os.environ)
    show_config()
    print(dates.days_ago(1))