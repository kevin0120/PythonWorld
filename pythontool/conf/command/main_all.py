
import os

import argcomplete

from pythontool.conf.airflow.cli import cli_parser
from pythontool.conf.airflow.configuration import conf

if __name__ == '__main__':
    """Main executable function"""
    if conf.get("core", "security") == 'kerberos':
        os.environ['KRB5CCNAME'] = conf.get('kerberos', 'ccache')
        os.environ['KRB5_KTNAME'] = conf.get('kerberos', 'keytab')
    parser = cli_parser.get_parser()
    # sensors
    # default_timeout
    # 自动补全命令
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print("hhh")
    args.func(args)
