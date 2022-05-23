#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Command-line interface"""

import argparse
import json
import os
import textwrap
from argparse import Action, ArgumentError, RawTextHelpFormatter
from functools import lru_cache
from typing import Callable, Dict, Iterable, List, NamedTuple, Optional, Union

import lazy_object_proxy

from pythontool.conf.airflow import settings
from pythontool.conf.airflow.cli.commands.legacy_commands import check_legacy_command
from pythontool.conf.airflow.configuration import conf
from pythontool.conf.airflow.exceptions import AirflowException
from pythontool.conf.airflow.executors.executor_constants import CELERY_EXECUTOR, CELERY_KUBERNETES_EXECUTOR
from pythontool.conf.airflow.executors.executor_loader import ExecutorLoader
from pythontool.conf.airflow.utils.cli import ColorMode
from pythontool.conf.airflow.utils.helpers import partition
from pythontool.conf.airflow.utils.module_loading import import_string
from pythontool.conf.airflow.utils.timezone import parse as parsedate

BUILD_DOCS = "BUILDING_AIRFLOW_DOCS" in os.environ


def lazy_load_command(import_path: str) -> Callable:
    """Create a lazy loader for command"""
    _, _, name = import_path.rpartition('.')

    def command(*args, **kwargs):
        func = import_string(import_path)
        return func(*args, **kwargs)

    command.__name__ = name

    return command


class DefaultHelpParser(argparse.ArgumentParser):
    """CustomParser to display help message"""

    def _check_value(self, action, value):
        """Override _check_value and check conditionally added command"""
        if action.dest == 'subcommand' and value == 'celery':
            executor = conf.get('core', 'EXECUTOR')
            if executor not in (CELERY_EXECUTOR, CELERY_KUBERNETES_EXECUTOR):
                executor_cls, _ = ExecutorLoader.import_executor_cls(executor)
                classes = ()
                try:
                    from pythontool.conf.airflow.executors.celery_executor import CeleryExecutor

                    classes += (CeleryExecutor,)
                except ImportError:
                    message = (
                        "The celery subcommand requires that you pip install the celery module. "
                        "To do it, run: pip install 'apache-airflow[celery]'"
                    )
                    raise ArgumentError(action, message)
                try:
                    from pythontool.conf.airflow.executors.celery_kubernetes_executor import CeleryKubernetesExecutor

                    classes += (CeleryKubernetesExecutor,)
                except ImportError:
                    pass
                if not issubclass(executor_cls, classes):
                    message = (
                        f'celery subcommand works only with CeleryExecutor, CeleryKubernetesExecutor and '
                        f'executors derived from them, your current executor: {executor}, subclassed from: '
                        f'{", ".join([base_cls.__qualname__ for base_cls in executor_cls.__bases__])}'
                    )
                    raise ArgumentError(action, message)
        if action.dest == 'subcommand' and value == 'kubernetes':
            try:
                import kubernetes.client  # noqa: F401
            except ImportError:
                message = (
                    "The kubernetes subcommand requires that you pip install the kubernetes python client. "
                    "To do it, run: pip install 'apache-airflow[cncf.kubernetes]'"
                )
                raise ArgumentError(action, message)

        if action.choices is not None and value not in action.choices:
            check_legacy_command(action, value)

        super()._check_value(action, value)

    def error(self, message):
        """Override error and use print_instead of print_usage"""
        self.print_help()
        self.exit(2, f'\n{self.prog} command error: {message}, see help above.\n')


# Used in Arg to enable `None' as a distinct value from "not passed"
_UNSET = object()


class Arg:
    """Class to keep information about command line argument"""

    def __init__(
            self,
            flags=_UNSET,
            help=_UNSET,
            action=_UNSET,
            default=_UNSET,
            nargs=_UNSET,
            type=_UNSET,
            choices=_UNSET,
            required=_UNSET,
            metavar=_UNSET,
            dest=_UNSET,
    ):
        self.flags = flags
        self.kwargs = {}
        for k, v in locals().items():
            if v is _UNSET:
                continue
            if k in ("self", "flags"):
                continue

            self.kwargs[k] = v

    def add_to_parser(self, parser: argparse.ArgumentParser):
        """Add this argument to an ArgumentParser"""
        parser.add_argument(*self.flags, **self.kwargs)


def positive_int(*, allow_zero):
    """Define a positive int type for an argument."""

    def _check(value):
        try:
            value = int(value)
            if allow_zero and value == 0:
                return value
            if value > 0:
                return value
        except ValueError:
            pass
        raise argparse.ArgumentTypeError(f"invalid positive int value: '{value}'")

    return _check


def string_list_type(val):
    """Parses comma-separated list and returns list of string (strips whitespace)"""
    return [x.strip() for x in val.split(',')]


def string_lower_type(val):
    """Lowers arg"""
    if not val:
        return
    return val.strip().lower()


# Shared
ARG_DAG_ID = Arg(("dag_id",), help="The id of the dag")
ARG_TASK_ID = Arg(("task_id",), help="The id of the task")
ARG_EXECUTION_DATE = Arg(("execution_date",), help="The execution date of the DAG", type=parsedate)
ARG_EXECUTION_DATE_OR_RUN_ID = Arg(
    ('execution_date_or_run_id',), help="The execution_date of the DAG or run_id of the DAGRun"
)
ARG_TASK_REGEX = Arg(
    ("-t", "--task-regex"), help="The regex to filter specific task_ids to backfill (optional)"
)
ARG_SUBDIR = Arg(
    ("-S", "--subdir"),
    help=(
        "File location or directory from which to look for the dag. "
        "Defaults to '[AIRFLOW_HOME]/dags' where [AIRFLOW_HOME] is the "
        "value you set for 'AIRFLOW_HOME' config you set in 'airflow.cfg' "
    ),
    default='[AIRFLOW_HOME]/dags' if BUILD_DOCS else settings.DAGS_FOLDER,
)
ARG_START_DATE = Arg(("-s", "--start-date"), help="Override start_date YYYY-MM-DD", type=parsedate)
ARG_END_DATE = Arg(("-e", "--end-date"), help="Override end_date YYYY-MM-DD", type=parsedate)
ARG_OUTPUT_PATH = Arg(
    (
        "-o",
        "--output-path",
    ),
    help="The output for generated yaml files",
    type=str,
    default="[CWD]" if BUILD_DOCS else os.getcwd(),
)
ARG_DRY_RUN = Arg(
    ("-n", "--dry-run"),
    help="Perform a dry run for each task. Only renders Template Fields for each task, nothing else",
    action="store_true",
)
ARG_PID = Arg(("--pid",), help="PID file location", nargs='?')
ARG_DAEMON = Arg(
    ("-D", "--daemon"), help="Daemonize instead of running in the foreground", action="store_true"
)
ARG_STDERR = Arg(("--stderr",), help="Redirect stderr to this file")
ARG_STDOUT = Arg(("--stdout",), help="Redirect stdout to this file")
ARG_LOG_FILE = Arg(("-l", "--log-file"), help="Location of the log file")
ARG_YES = Arg(
    ("-y", "--yes"),
    help="Do not prompt to confirm. Use with care!",
    action="store_true",
    default=False,
)
ARG_OUTPUT = Arg(
    (
        "-o",
        "--output",
    ),
    help="Output format. Allowed values: json, yaml, plain, table (default: table)",
    metavar="(table, json, yaml, plain)",
    choices=("table", "json", "yaml", "plain"),
    default="table",
)
ARG_COLOR = Arg(
    ('--color',),
    help="Do emit colored output (default: auto)",
    choices={ColorMode.ON, ColorMode.OFF, ColorMode.AUTO},
    default=ColorMode.AUTO,
)

# DB args
ARG_VERSION_RANGE = Arg(
    ("-r", "--range"),
    help="Version range(start:end) for offline sql generation. Example: '2.0.2:2.2.3'",
    default=None,
)
ARG_REVISION_RANGE = Arg(
    ('--revision-range',),
    help=(
        "Migration revision range(start:end) to use for offline sql generation. "
        "Example: ``a13f7613ad25:7b2661a43ba3``"
    ),
    default=None,
)

# list_dag_runs
ARG_DAG_ID_OPT = Arg(("-d", "--dag-id"), help="The id of the dag")
ARG_NO_BACKFILL = Arg(
    ("--no-backfill",), help="filter all the backfill dagruns given the dag id", action="store_true"
)
ARG_STATE = Arg(("--state",), help="Only list the dag runs corresponding to the state")

# list_jobs
ARG_LIMIT = Arg(("--limit",), help="Return a limited number of records")

# next_execution
ARG_NUM_EXECUTIONS = Arg(
    ("-n", "--num-executions"),
    default=1,
    type=positive_int(allow_zero=False),
    help="The number of next execution datetimes to show",
)

# backfill
ARG_MARK_SUCCESS = Arg(
    ("-m", "--mark-success"), help="Mark jobs as succeeded without running them", action="store_true"
)
ARG_VERBOSE = Arg(("-v", "--verbose"), help="Make logging output more verbose", action="store_true")
ARG_LOCAL = Arg(("-l", "--local"), help="Run the task using the LocalExecutor", action="store_true")
ARG_DONOT_PICKLE = Arg(
    ("-x", "--donot-pickle"),
    help=(
        "Do not attempt to pickle the DAG object to send over "
        "to the workers, just tell the workers to run their version "
        "of the code"
    ),
    action="store_true",
)
ARG_BF_IGNORE_DEPENDENCIES = Arg(
    ("-i", "--ignore-dependencies"),
    help=(
        "Skip upstream tasks, run only the tasks "
        "matching the regexp. Only works in conjunction "
        "with task_regex"
    ),
    action="store_true",
)
ARG_BF_IGNORE_FIRST_DEPENDS_ON_PAST = Arg(
    ("-I", "--ignore-first-depends-on-past"),
    help=(
        "Ignores depends_on_past dependencies for the first "
        "set of tasks only (subsequent executions in the backfill "
        "DO respect depends_on_past)"
    ),
    action="store_true",
)
ARG_POOL = Arg(("--pool",), "Resource pool to use")
ARG_DELAY_ON_LIMIT = Arg(
    ("--delay-on-limit",),
    help=(
        "Amount of time in seconds to wait when the limit "
        "on maximum active dag runs (max_active_runs) has "
        "been reached before trying to execute a dag run "
        "again"
    ),
    type=float,
    default=1.0,
)
ARG_RESET_DAG_RUN = Arg(
    ("--reset-dagruns",),
    help=(
        "if set, the backfill will delete existing "
        "backfill-related DAG runs and start "
        "anew with fresh, running DAG runs"
    ),
    action="store_true",
)
ARG_RERUN_FAILED_TASKS = Arg(
    ("--rerun-failed-tasks",),
    help=(
        "if set, the backfill will auto-rerun "
        "all the failed tasks for the backfill date range "
        "instead of throwing exceptions"
    ),
    action="store_true",
)
ARG_CONTINUE_ON_FAILURES = Arg(
    ("--continue-on-failures",),
    help=("if set, the backfill will keep going even if some of the tasks failed"),
    action="store_true",
)
ARG_RUN_BACKWARDS = Arg(
    (
        "-B",
        "--run-backwards",
    ),
    help=(
        "if set, the backfill will run tasks from the most "
        "recent day first.  if there are tasks that depend_on_past "
        "this option will throw an exception"
    ),
    action="store_true",
)
# test_dag
ARG_SHOW_DAGRUN = Arg(
    ("--show-dagrun",),
    help=(
        "After completing the backfill, shows the diagram for current DAG Run.\n"
        "\n"
        "The diagram is in DOT language\n"
    ),
    action='store_true',
)
ARG_IMGCAT_DAGRUN = Arg(
    ("--imgcat-dagrun",),
    help=(
        "After completing the dag run, prints a diagram on the screen for the "
        "current DAG Run using the imgcat tool.\n"
    ),
    action='store_true',
)
ARG_SAVE_DAGRUN = Arg(
    ("--save-dagrun",),
    help="After completing the backfill, saves the diagram for current DAG Run to the indicated file.\n\n",
)

# list_tasks
ARG_TREE = Arg(("-t", "--tree"), help="Tree view", action="store_true")

# tasks_run
# This is a hidden option -- not meant for users to set or know about
ARG_SHUT_DOWN_LOGGING = Arg(
    ("--no-shut-down-logging",),
    help=argparse.SUPPRESS,
    dest="shut_down_logging",
    action="store_false",
    default=True,
)

# clear
ARG_UPSTREAM = Arg(("-u", "--upstream"), help="Include upstream tasks", action="store_true")
ARG_ONLY_FAILED = Arg(("-f", "--only-failed"), help="Only failed jobs", action="store_true")
ARG_ONLY_RUNNING = Arg(("-r", "--only-running"), help="Only running jobs", action="store_true")
ARG_DOWNSTREAM = Arg(("-d", "--downstream"), help="Include downstream tasks", action="store_true")
ARG_EXCLUDE_SUBDAGS = Arg(("-x", "--exclude-subdags"), help="Exclude subdags", action="store_true")
ARG_EXCLUDE_PARENTDAG = Arg(
    ("-X", "--exclude-parentdag"),
    help="Exclude ParentDAGS if the task cleared is a part of a SubDAG",
    action="store_true",
)
ARG_DAG_REGEX = Arg(
    ("-R", "--dag-regex"), help="Search dag_id as regex instead of exact string", action="store_true"
)

# show_dag
ARG_SAVE = Arg(("-s", "--save"), help="Saves the result to the indicated file.")

ARG_IMGCAT = Arg(("--imgcat",), help="Displays graph using the imgcat tool.", action='store_true')

# trigger_dag
ARG_RUN_ID = Arg(("-r", "--run-id"), help="Helps to identify this run")
ARG_CONF = Arg(('-c', '--conf'), help="JSON string that gets pickled into the DagRun's conf attribute")
ARG_EXEC_DATE = Arg(("-e", "--exec-date"), help="The execution date of the DAG", type=parsedate)

# db
ARG_DB_TABLES = Arg(
    ("-t", "--tables"),
    help=lazy_object_proxy.Proxy(
        lambda: f"Table names to perform maintenance on (use comma-separated list).\n"
                f"Options: {import_string('airflow.cli.commands.db_command.all_tables')}"
    ),
    type=string_list_type,
)
ARG_DB_CLEANUP_TIMESTAMP = Arg(
    ("--clean-before-timestamp",),
    help="The date or timestamp before which data should be purged.\n"
         "If no timezone info is supplied then dates are assumed to be in airflow default timezone.\n"
         "Example: '2022-01-01 00:00:00+01:00'",
    type=parsedate,
    required=True,
)
ARG_DB_DRY_RUN = Arg(
    ("--dry-run",),
    help="Perform a dry run",
    action="store_true",
)

# pool
ARG_POOL_NAME = Arg(("pool",), metavar='NAME', help="Pool name")
ARG_POOL_SLOTS = Arg(("slots",), type=int, help="Pool slots")
ARG_POOL_DESCRIPTION = Arg(("description",), help="Pool description")
ARG_POOL_IMPORT = Arg(
    ("file",),
    metavar="FILEPATH",
    help="Import pools from JSON file. Example format::\n"
         + textwrap.indent(
        textwrap.dedent(
            '''
            {
                "pool_1": {"slots": 5, "description": ""},
                "pool_2": {"slots": 10, "description": "test"}
            }'''
        ),
        " " * 4,
    ),
)

ARG_POOL_EXPORT = Arg(("file",), metavar="FILEPATH", help="Export all pools to JSON file")

# variables
ARG_VAR = Arg(("key",), help="Variable key")
ARG_VAR_VALUE = Arg(("value",), metavar='VALUE', help="Variable value")
ARG_DEFAULT = Arg(
    ("-d", "--default"), metavar="VAL", default=None, help="Default value returned if variable does not exist"
)
ARG_JSON = Arg(("-j", "--json"), help="Deserialize JSON variable", action="store_true")
ARG_VAR_IMPORT = Arg(("file",), help="Import variables from JSON file")
ARG_VAR_EXPORT = Arg(("file",), help="Export all variables to JSON file")

# kerberos
ARG_PRINCIPAL = Arg(("principal",), help="kerberos principal", nargs='?')
ARG_KEYTAB = Arg(("-k", "--keytab"), help="keytab", nargs='?', default=conf.get('kerberos', 'keytab'))
# run
ARG_INTERACTIVE = Arg(
    ('-N', '--interactive'),
    help='Do not capture standard output and error streams (useful for interactive debugging)',
    action='store_true',
)
# TODO(aoen): "force" is a poor choice of name here since it implies it overrides
# all dependencies (not just past success), e.g. the ignore_depends_on_past
# dependency. This flag should be deprecated and renamed to 'ignore_ti_state' and
# the "ignore_all_dependencies" command should be called the"force" command
# instead.
ARG_FORCE = Arg(
    ("-f", "--force"),
    help="Ignore previous task instance state, rerun regardless if task already succeeded/failed",
    action="store_true",
)
ARG_RAW = Arg(("-r", "--raw"), argparse.SUPPRESS, "store_true")
ARG_IGNORE_ALL_DEPENDENCIES = Arg(
    ("-A", "--ignore-all-dependencies"),
    help="Ignores all non-critical dependencies, including ignore_ti_state and ignore_task_deps",
    action="store_true",
)
# TODO(aoen): ignore_dependencies is a poor choice of name here because it is too
# vague (e.g. a task being in the appropriate state to be run is also a dependency
# but is not ignored by this flag), the name 'ignore_task_dependencies' is
# slightly better (as it ignores all dependencies that are specific to the task),
# so deprecate the old command name and use this instead.
ARG_IGNORE_DEPENDENCIES = Arg(
    ("-i", "--ignore-dependencies"),
    help="Ignore task-specific dependencies, e.g. upstream, depends_on_past, and retry delay dependencies",
    action="store_true",
)
ARG_IGNORE_DEPENDS_ON_PAST = Arg(
    ("-I", "--ignore-depends-on-past"),
    help="Ignore depends_on_past dependencies (but respect upstream dependencies)",
    action="store_true",
)
ARG_SHIP_DAG = Arg(
    ("--ship-dag",), help="Pickles (serializes) the DAG and ships it to the worker", action="store_true"
)
ARG_PICKLE = Arg(("-p", "--pickle"), help="Serialized pickle object of the entire dag (used internally)")
ARG_JOB_ID = Arg(("-j", "--job-id"), help=argparse.SUPPRESS)
ARG_CFG_PATH = Arg(("--cfg-path",), help="Path to config file to use instead of airflow.cfg")
ARG_MAP_INDEX = Arg(('--map-index',), type=int, default=-1, help="Mapped task index")

# database
ARG_MIGRATION_TIMEOUT = Arg(
    ("-t", "--migration-wait-timeout"),
    help="timeout to wait for db to migrate ",
    type=int,
    default=60,
)
ARG_DB_VERSION__UPGRADE = Arg(
    ("-n", "--to-version"),
    help=(
        "(Optional) The airflow version to upgrade to. Note: must provide either "
        "`--to-revision` or `--to-version`."
    ),
)
ARG_DB_REVISION__UPGRADE = Arg(
    ("-r", "--to-revision"),
    help="(Optional) If provided, only run migrations up to and including this Alembic revision.",
)
ARG_DB_VERSION__DOWNGRADE = Arg(
    ("-n", "--to-version"),
    help="(Optional) If provided, only run migrations up to this version.",
)
ARG_DB_FROM_VERSION = Arg(
    ("--from-version",),
    help="(Optional) If generating sql, may supply a *from* version",
)
ARG_DB_REVISION__DOWNGRADE = Arg(
    ("-r", "--to-revision"),
    help="The Alembic revision to downgrade to. Note: must provide either `--to-revision` or `--to-version`.",
)
ARG_DB_FROM_REVISION = Arg(
    ("--from-revision",),
    help="(Optional) If generating sql, may supply a *from* Alembic revision",
)
ARG_DB_SQL_ONLY = Arg(
    ("-s", "--show-sql-only"),
    help="Don't actually run migrations; just print out sql scripts for offline migration. "
         "Required if using either `--from-version` or `--from-version`.",
    action="store_true",
    default=False,
)
ARG_DB_SKIP_INIT = Arg(
    ("-s", "--skip-init"),
    help="Only remove tables; do not perform db init.",
    action="store_true",
    default=False,
)

# webserver
ARG_PORT = Arg(
    ("-p", "--port"),
    default=conf.get('webserver', 'WEB_SERVER_PORT'),
    type=int,
    help="The port on which to run the server",
)
ARG_SSL_CERT = Arg(
    ("--ssl-cert",),
    default=conf.get('webserver', 'WEB_SERVER_SSL_CERT'),
    help="Path to the SSL certificate for the webserver",
)
ARG_SSL_KEY = Arg(
    ("--ssl-key",),
    default=conf.get('webserver', 'WEB_SERVER_SSL_KEY'),
    help="Path to the key to use with the SSL certificate",
)
ARG_WORKERS = Arg(
    ("-w", "--workers"),
    default=conf.get('webserver', 'WORKERS'),
    type=int,
    help="Number of workers to run the webserver on",
)
ARG_WORKERCLASS = Arg(
    ("-k", "--workerclass"),
    default=conf.get('webserver', 'WORKER_CLASS'),
    choices=['sync', 'eventlet', 'gevent', 'tornado'],
    help="The worker class to use for Gunicorn",
)
ARG_WORKER_TIMEOUT = Arg(
    ("-t", "--worker-timeout"),
    default=conf.get('webserver', 'WEB_SERVER_WORKER_TIMEOUT'),
    type=int,
    help="The timeout for waiting on webserver workers",
)
ARG_HOSTNAME = Arg(
    ("-H", "--hostname"),
    default=conf.get('webserver', 'WEB_SERVER_HOST'),
    help="Set the hostname on which to run the web server",
)
ARG_DEBUG = Arg(
    ("-d", "--debug"), help="Use the server that ships with Flask in debug mode", action="store_true"
)
ARG_ACCESS_LOGFILE = Arg(
    ("-A", "--access-logfile"),
    default=conf.get('webserver', 'ACCESS_LOGFILE'),
    help="The logfile to store the webserver access log. Use '-' to print to stderr",
)
ARG_ERROR_LOGFILE = Arg(
    ("-E", "--error-logfile"),
    default=conf.get('webserver', 'ERROR_LOGFILE'),
    help="The logfile to store the webserver error log. Use '-' to print to stderr",
)
ARG_ACCESS_LOGFORMAT = Arg(
    ("-L", "--access-logformat"),
    default=conf.get('webserver', 'ACCESS_LOGFORMAT'),
    help="The access log format for gunicorn logs",
)

# scheduler
ARG_NUM_RUNS = Arg(
    ("-n", "--num-runs"),
    default=conf.getint('scheduler', 'num_runs'),
    type=int,
    help="Set the number of runs to execute before exiting",
)
ARG_DO_PICKLE = Arg(
    ("-p", "--do-pickle"),
    default=False,
    help=(
        "Attempt to pickle the DAG object to send over "
        "to the workers, instead of letting workers run their version "
        "of the code"
    ),
    action="store_true",
)

# worker
ARG_QUEUES = Arg(
    ("-q", "--queues"),
    help="Comma delimited list of queues to serve",
    default=conf.get('operators', 'DEFAULT_QUEUE'),
)
ARG_CONCURRENCY = Arg(
    ("-c", "--concurrency"),
    type=int,
    help="The number of worker processes",
    default=conf.get('celery', 'worker_concurrency'),
)
ARG_CELERY_HOSTNAME = Arg(
    ("-H", "--celery-hostname"),
    help="Set the hostname of celery worker if you have multiple workers on a single machine",
)
ARG_UMASK = Arg(
    ("-u", "--umask"),
    help="Set the umask of celery worker in daemon mode",
    default=conf.get('celery', 'worker_umask'),
)
ARG_WITHOUT_MINGLE = Arg(
    ("--without-mingle",),
    default=False,
    help="Don’t synchronize with other workers at start-up",
    action="store_true",
)
ARG_WITHOUT_GOSSIP = Arg(
    ("--without-gossip",),
    default=False,
    help="Don’t subscribe to other workers events",
    action="store_true",
)

# flower
ARG_BROKER_API = Arg(("-a", "--broker-api"), help="Broker API")
ARG_FLOWER_HOSTNAME = Arg(
    ("-H", "--hostname"),
    default=conf.get('celery', 'FLOWER_HOST'),
    help="Set the hostname on which to run the server",
)
ARG_FLOWER_PORT = Arg(
    ("-p", "--port"),
    default=conf.get('celery', 'FLOWER_PORT'),
    type=int,
    help="The port on which to run the server",
)
ARG_FLOWER_CONF = Arg(("-c", "--flower-conf"), help="Configuration file for flower")
ARG_FLOWER_URL_PREFIX = Arg(
    ("-u", "--url-prefix"), default=conf.get('celery', 'FLOWER_URL_PREFIX'), help="URL prefix for Flower"
)
ARG_FLOWER_BASIC_AUTH = Arg(
    ("-A", "--basic-auth"),
    default=conf.get('celery', 'FLOWER_BASIC_AUTH'),
    help=(
        "Securing Flower with Basic Authentication. "
        "Accepts user:password pairs separated by a comma. "
        "Example: flower_basic_auth = user1:password1,user2:password2"
    ),
)
ARG_TASK_PARAMS = Arg(("-t", "--task-params"), help="Sends a JSON params dict to the task")
ARG_POST_MORTEM = Arg(
    ("-m", "--post-mortem"), action="store_true", help="Open debugger on uncaught exception"
)
ARG_ENV_VARS = Arg(
    ("--env-vars",),
    help="Set env var in both parsing time and runtime for each of entry supplied in a JSON dict",
    type=json.loads,
)

# connections
ARG_CONN_ID = Arg(('conn_id',), help='Connection id, required to get/add/delete a connection', type=str)
ARG_CONN_ID_FILTER = Arg(
    ('--conn-id',), help='If passed, only items with the specified connection ID will be displayed', type=str
)
ARG_CONN_URI = Arg(
    ('--conn-uri',), help='Connection URI, required to add a connection without conn_type', type=str
)
ARG_CONN_JSON = Arg(
    ('--conn-json',), help='Connection JSON, required to add a connection using JSON representation', type=str
)
ARG_CONN_TYPE = Arg(
    ('--conn-type',), help='Connection type, required to add a connection without conn_uri', type=str
)
ARG_CONN_DESCRIPTION = Arg(
    ('--conn-description',), help='Connection description, optional when adding a connection', type=str
)
ARG_CONN_HOST = Arg(('--conn-host',), help='Connection host, optional when adding a connection', type=str)
ARG_CONN_LOGIN = Arg(('--conn-login',), help='Connection login, optional when adding a connection', type=str)
ARG_CONN_PASSWORD = Arg(
    ('--conn-password',), help='Connection password, optional when adding a connection', type=str
)
ARG_CONN_SCHEMA = Arg(
    ('--conn-schema',), help='Connection schema, optional when adding a connection', type=str
)
ARG_CONN_PORT = Arg(('--conn-port',), help='Connection port, optional when adding a connection', type=str)
ARG_CONN_EXTRA = Arg(
    ('--conn-extra',), help='Connection `Extra` field, optional when adding a connection', type=str
)
ARG_CONN_EXPORT = Arg(
    ('file',),
    help='Output file path for exporting the connections',
    type=argparse.FileType('w', encoding='UTF-8'),
)
ARG_CONN_EXPORT_FORMAT = Arg(
    ('--format',),
    help='Deprecated -- use `--file-format` instead. File format to use for the export.',
    type=str,
    choices=['json', 'yaml', 'env'],
)
ARG_CONN_EXPORT_FILE_FORMAT = Arg(
    ('--file-format',), help='File format for the export', type=str, choices=['json', 'yaml', 'env']
)
ARG_CONN_SERIALIZATION_FORMAT = Arg(
    ('--serialization-format',),
    help='When exporting as `.env` format, defines how connections should be serialized. Default is `uri`.',
    type=string_lower_type,
    choices=['json', 'uri'],
)
ARG_CONN_IMPORT = Arg(("file",), help="Import connections from a file")

# providers
ARG_PROVIDER_NAME = Arg(
    ('provider_name',), help='Provider name, required to get provider information', type=str
)
ARG_FULL = Arg(
    ('-f', '--full'),
    help='Full information about the provider, including documentation information.',
    required=False,
    action="store_true",
)

# users
ARG_USERNAME = Arg(('-u', '--username'), help='Username of the user', required=True, type=str)
ARG_USERNAME_OPTIONAL = Arg(('-u', '--username'), help='Username of the user', type=str)
ARG_FIRSTNAME = Arg(('-f', '--firstname'), help='First name of the user', required=True, type=str)
ARG_LASTNAME = Arg(('-l', '--lastname'), help='Last name of the user', required=True, type=str)
ARG_ROLE = Arg(
    ('-r', '--role'),
    help='Role of the user. Existing roles include Admin, User, Op, Viewer, and Public',
    required=True,
    type=str,
)
ARG_EMAIL = Arg(('-e', '--email'), help='Email of the user', required=True, type=str)
ARG_EMAIL_OPTIONAL = Arg(('-e', '--email'), help='Email of the user', type=str)
ARG_PASSWORD = Arg(
    ('-p', '--password'),
    help='Password of the user, required to create a user without --use-random-password',
    type=str,
)
ARG_USE_RANDOM_PASSWORD = Arg(
    ('--use-random-password',),
    help='Do not prompt for password. Use random string instead.'
         ' Required to create a user without --password ',
    default=False,
    action='store_true',
)
ARG_USER_IMPORT = Arg(
    ("import",),
    metavar="FILEPATH",
    help="Import users from JSON file. Example format::\n"
         + textwrap.indent(
        textwrap.dedent(
            '''
            [
                {
                    "email": "foo@bar.org",
                    "firstname": "Jon",
                    "lastname": "Doe",
                    "roles": ["Public"],
                    "username": "jondoe"
                }
            ]'''
        ),
        " " * 4,
    ),
)

# info
ARG_ANONYMIZE = Arg(
    ('--anonymize',),
    help='Minimize any personal identifiable information. Use it when sharing output with others.',
    action='store_true',
)
ARG_FILE_IO = Arg(
    ('--file-io',), help='Send output to file.io service and returns link.', action='store_true'
)

# config
ARG_SECTION = Arg(
    ("section",),
    help="The section name",
)
ARG_OPTION = Arg(
    ("option",),
    help="The option name",
)

ALTERNATIVE_CONN_SPECS_ARGS = [
    ARG_CONN_TYPE,
    ARG_CONN_DESCRIPTION,
    ARG_CONN_HOST,
    ARG_CONN_LOGIN,
    ARG_CONN_PASSWORD,
    ARG_CONN_SCHEMA,
    ARG_CONN_PORT,
]


class ActionCommand(NamedTuple):
    """Single CLI command"""

    name: str
    help: str
    func: Callable
    args: Iterable[Arg]
    description: Optional[str] = None
    epilog: Optional[str] = None


class GroupCommand(NamedTuple):
    """ClI command with subcommands"""

    name: str
    help: str
    subcommands: Iterable
    description: Optional[str] = None
    epilog: Optional[str] = None


CLICommand = Union[ActionCommand, GroupCommand]

CONFIG_COMMANDS = (
    ActionCommand(
        name='get-value',
        help='Print the value of the configuration',
        func=lazy_load_command('pythontool.conf.airflow.cli.commands.config_command.get_value'),
        args=(
            ARG_SECTION,
            ARG_OPTION,
        ),
    ),
    ActionCommand(
        name='list',
        help='List options for the configuration',
        func=lazy_load_command('pythontool.conf.airflow.cli.commands.config_command.show_config'),
        args=(ARG_COLOR,),
    ),
)

airflow_commands: List[CLICommand] = [
    GroupCommand(name="config", help='View configuration', subcommands=CONFIG_COMMANDS),
    ActionCommand(
        name='info',
        help='Show information about current Airflow and environment',
        func=lazy_load_command('pythontool.conf.airflow.cli.commands.info_command.show_info'),
        args=(
            ARG_ANONYMIZE,
            ARG_FILE_IO,
            ARG_VERBOSE,
            ARG_OUTPUT,
        ),
    ),
]
ALL_COMMANDS_DICT: Dict[str, CLICommand] = {sp.name: sp for sp in airflow_commands}


class AirflowHelpFormatter(argparse.HelpFormatter):
    """
    Custom help formatter to display help message.

    It displays simple commands and groups of commands in separate sections.
    """

    def _format_action(self, action: Action):
        if isinstance(action, argparse._SubParsersAction):

            parts = []
            action_header = self._format_action_invocation(action)
            action_header = '%*s%s\n' % (self._current_indent, '', action_header)
            parts.append(action_header)

            self._indent()
            subactions = action._get_subactions()
            action_subcommands, group_subcommands = partition(
                lambda d: isinstance(ALL_COMMANDS_DICT[d.dest], GroupCommand), subactions
            )
            parts.append("\n")
            parts.append('%*s%s:\n' % (self._current_indent, '', "Groups"))
            self._indent()
            for subaction in group_subcommands:
                parts.append(self._format_action(subaction))
            self._dedent()

            parts.append("\n")
            parts.append('%*s%s:\n' % (self._current_indent, '', "Commands"))
            self._indent()

            for subaction in action_subcommands:
                parts.append(self._format_action(subaction))
            self._dedent()
            self._dedent()

            # return a single string
            return self._join_parts(parts)

        return super()._format_action(action)


@lru_cache(maxsize=None)
def get_parser(dag_parser: bool = False) -> argparse.ArgumentParser:
    """Creates and returns command line argument parser"""
    parser = DefaultHelpParser(prog="airflow", formatter_class=AirflowHelpFormatter)
    subparsers = parser.add_subparsers(dest='subcommand', metavar="GROUP_OR_COMMAND")
    subparsers.required = True

    command_dict = ALL_COMMANDS_DICT
    subparser_list = command_dict.keys()
    sub_name: str
    for sub_name in sorted(subparser_list):
        sub: CLICommand = command_dict[sub_name]
        _add_command(subparsers, sub)
    return parser


def _sort_args(args: Iterable[Arg]) -> Iterable[Arg]:
    """Sort subcommand optional args, keep positional args"""

    def get_long_option(arg: Arg):
        """Get long option from Arg.flags"""
        return arg.flags[0] if len(arg.flags) == 1 else arg.flags[1]

    positional, optional = partition(lambda x: x.flags[0].startswith("-"), args)
    yield from positional
    yield from sorted(optional, key=lambda x: get_long_option(x).lower())

def _add_command(subparsers: argparse._SubParsersAction, sub: CLICommand) -> None:
    sub_proc = subparsers.add_parser(
        sub.name, help=sub.help, description=sub.description or sub.help, epilog=sub.epilog
    )
    sub_proc.formatter_class = RawTextHelpFormatter

    if isinstance(sub, GroupCommand):
        _add_group_command(sub, sub_proc)
    elif isinstance(sub, ActionCommand):
        _add_action_command(sub, sub_proc)
    else:
        raise AirflowException("Invalid command definition.")


def _add_action_command(sub: ActionCommand, sub_proc: argparse.ArgumentParser) -> None:
    for arg in _sort_args(sub.args):
        arg.add_to_parser(sub_proc)
    sub_proc.set_defaults(func=sub.func)


def _add_group_command(sub: GroupCommand, sub_proc: argparse.ArgumentParser) -> None:
    subcommands = sub.subcommands
    sub_subparsers = sub_proc.add_subparsers(dest="subcommand", metavar="COMMAND")
    sub_subparsers.required = True

    for command in sorted(subcommands, key=lambda x: x.name):
        _add_command(sub_subparsers, command)
