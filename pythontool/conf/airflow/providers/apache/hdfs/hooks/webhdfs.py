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
"""Hook for Web HDFS"""
import logging
import socket
from typing import Any, Optional

import requests
from hdfs import HdfsError, InsecureClient

from pythontool.conf.airflow.configuration import conf
from pythontool.conf.airflow.exceptions import AirflowException
from pythontool.conf.airflow.hooks.base import BaseHook

log = logging.getLogger(__name__)

_kerberos_security_mode = conf.get("core", "security") == "kerberos"
if _kerberos_security_mode:
    try:
        from hdfs.ext.kerberos import KerberosClient
    except ImportError:
        log.error("Could not load the Kerberos extension for the WebHDFSHook.")
        raise


class AirflowWebHDFSHookException(AirflowException):
    """Exception specific for WebHDFS hook"""


class WebHDFSHook(BaseHook):
    """
    Interact with HDFS. This class is a wrapper around the hdfscli library.

    :param webhdfs_conn_id: The connection id for the webhdfs client to connect to.
    :param proxy_user: The user used to authenticate.
    """

    def __init__(self, webhdfs_conn_id: str = 'webhdfs_default', proxy_user: Optional[str] = None):
        super().__init__()
        self.webhdfs_conn_id = webhdfs_conn_id
        self.proxy_user = proxy_user

    def get_conn(self) -> Any:
        """
        Establishes a connection depending on the security mode set via config or environment variable.
        :return: a hdfscli InsecureClient or KerberosClient object.
        :rtype: hdfs.InsecureClient or hdfs.ext.kerberos.KerberosClient
        """
        connection = self._find_valid_server()
        if connection is None:
            raise AirflowWebHDFSHookException("Failed to locate the valid server.")
        return connection

    def _find_valid_server(self) -> Any:
        connection = self.get_connection(self.webhdfs_conn_id)
        namenodes = connection.host.split(',')
        for namenode in namenodes:
            host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.log.info("Trying to connect to %s:%s", namenode, connection.port)
            try:
                conn_check = host_socket.connect_ex((namenode, connection.port))
                if conn_check == 0:
                    self.log.info('Trying namenode %s', namenode)
                    client = self._get_client(
                        namenode, connection.port, connection.login, connection.extra_dejson
                    )
                    client.status('/')
                    self.log.info('Using namenode %s for hook', namenode)
                    host_socket.close()
                    return client
                else:
                    self.log.warning("Could not connect to %s:%s", namenode, connection.port)
            except HdfsError as hdfs_error:
                self.log.info('Read operation on namenode %s failed with error: %s', namenode, hdfs_error)
        return None

    def _get_client(self, namenode: str, port: int, login: str, extra_dejson: dict) -> Any:
        connection_str = f'http://{namenode}:{port}'
        session = requests.Session()

        if extra_dejson.get('use_ssl', False):
            connection_str = f'https://{namenode}:{port}'
            session.verify = extra_dejson.get('verify', True)

        if _kerberos_security_mode:
            client = KerberosClient(connection_str, session=session)
        else:
            proxy_user = self.proxy_user or login
            client = InsecureClient(connection_str, user=proxy_user, session=session)

        return client

    def check_for_path(self, hdfs_path: str) -> bool:
        """
        Check for the existence of a path in HDFS by querying FileStatus.

        :param hdfs_path: The path to check.
        :return: True if the path exists and False if not.
        :rtype: bool
        """
        conn = self.get_conn()

        status = conn.status(hdfs_path, strict=False)
        return bool(status)

    def load_file(
        self, source: str, destination: str, overwrite: bool = True, parallelism: int = 1, **kwargs: Any
    ) -> None:
        r"""
        Uploads a file to HDFS.

        :param source: Local path to file or folder.
            If it's a folder, all the files inside of it will be uploaded.
            .. note:: This implies that folders empty of files will not be created remotely.

        :param destination: PTarget HDFS path.
            If it already exists and is a directory, files will be uploaded inside.
        :param overwrite: Overwrite any existing file or directory.
        :param parallelism: Number of threads to use for parallelization.
            A value of `0` (or negative) uses as many threads as there are files.
        :param kwargs: Keyword arguments forwarded to :meth:`hdfs.client.Client.upload`.
        """
        conn = self.get_conn()

        conn.upload(
            hdfs_path=destination, local_path=source, overwrite=overwrite, n_threads=parallelism, **kwargs
        )
        self.log.debug("Uploaded file %s to %s", source, destination)
