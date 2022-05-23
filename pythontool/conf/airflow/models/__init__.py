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
"""Airflow models"""
from typing import Union

from pythontool.conf.airflow.models.base import ID_LEN, Base
from pythontool.conf.airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from pythontool.conf.airflow.models.connection import Connection
from pythontool.conf.airflow.models.dag import DAG, DagModel, DagTag
from pythontool.conf.airflow.models.dagbag import DagBag
from pythontool.conf.airflow.models.dagpickle import DagPickle
from pythontool.conf.airflow.models.dagrun import DagRun
from pythontool.conf.airflow.models.db_callback_request import DbCallbackRequest
from pythontool.conf.airflow.models.errors import ImportError
from pythontool.conf.airflow.models.log import Log
from pythontool.conf.airflow.models.mappedoperator import MappedOperator
from pythontool.conf.airflow.models.operator import Operator
from pythontool.conf.airflow.models.param import Param
from pythontool.conf.airflow.models.pool import Pool
from pythontool.conf.airflow.models.renderedtifields import RenderedTaskInstanceFields
from pythontool.conf.airflow.models.sensorinstance import SensorInstance
from pythontool.conf.airflow.models.skipmixin import SkipMixin
from pythontool.conf.airflow.models.slamiss import SlaMiss
from pythontool.conf.airflow.models.taskfail import TaskFail
from pythontool.conf.airflow.models.taskinstance import TaskInstance, clear_task_instances
from pythontool.conf.airflow.models.taskreschedule import TaskReschedule
from pythontool.conf.airflow.models.trigger import Trigger
from pythontool.conf.airflow.models.variable import Variable
from pythontool.conf.airflow.models.xcom import XCOM_RETURN_KEY, XCom

__all__ = [
    "DAG",
    "ID_LEN",
    "XCOM_RETURN_KEY",
    "Base",
    "BaseOperator",
    "BaseOperatorLink",
    "Connection",
    "DagBag",
    "DagModel",
    "DagPickle",
    "DagRun",
    "DagTag",
    "DbCallbackRequest",
    "ImportError",
    "Log",
    "MappedOperator",
    "Operator",
    "Param",
    "Pool",
    "RenderedTaskInstanceFields",
    "SensorInstance",
    "SkipMixin",
    "SlaMiss",
    "TaskFail",
    "TaskInstance",
    "TaskReschedule",
    "Trigger",
    "Variable",
    "XCom",
    "clear_task_instances",
]
