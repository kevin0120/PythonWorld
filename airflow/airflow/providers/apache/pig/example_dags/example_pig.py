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

"""Example DAG demonstrating the usage of the PigOperator."""
from datetime import datetime

from airflow import DAG
from airflow.providers.apache.pig.operators.pig import PigOperator

dag = DAG(
    dag_id='example_pig_operator',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
)

# [START create_pig]
run_this = PigOperator(
    task_id="run_example_pig_script",
    pig="ls /;",
    pig_opts="-x local",
    dag=dag,
)
# [END create_pig]
