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
"""This module is deprecated. Please use :mod:`airflow.providers.google.cloud.operators.mlengine`."""

import warnings

from pythontool.conf.airflow.providers.google.cloud.operators.mlengine import (
    MLEngineManageModelOperator,
    MLEngineManageVersionOperator,
    MLEngineStartBatchPredictionJobOperator,
    MLEngineStartTrainingJobOperator,
)

warnings.warn(
    "This module is deprecated. Please use `airflow.providers.google.cloud.operators.mlengine`.",
    DeprecationWarning,
    stacklevel=2,
)


class MLEngineBatchPredictionOperator(MLEngineStartBatchPredictionJobOperator):
    """
    This class is deprecated.
    Please use `airflow.providers.google.cloud.operators.mlengine.MLEngineStartBatchPredictionJobOperator`.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            """This class is deprecated.
            Please use
            `airflow.providers.google.cloud.operators.mlengine.MLEngineStartBatchPredictionJobOperator`.""",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class MLEngineModelOperator(MLEngineManageModelOperator):
    """
    This class is deprecated.
    Please use `airflow.providers.google.cloud.operators.mlengine.MLEngineManageModelOperator`.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            """This class is deprecated.
            Please use `airflow.providers.google.cloud.operators.mlengine.MLEngineManageModelOperator`.""",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class MLEngineTrainingOperator(MLEngineStartTrainingJobOperator):
    """
    This class is deprecated.
    Please use `airflow.providers.google.cloud.operators.mlengine.MLEngineStartTrainingJobOperator`.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            """This class is deprecated.
            Please use
            `airflow.providers.google.cloud.operators.mlengine.MLEngineStartTrainingJobOperator`.""",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class MLEngineVersionOperator(MLEngineManageVersionOperator):
    """
    This class is deprecated.
    Please use `airflow.providers.google.cloud.operators.mlengine.MLEngineManageVersionOperator`.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            """This class is deprecated.
            Please use
            `airflow.providers.google.cloud.operators.mlengine.MLEngineManageVersionOperator`.""",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
