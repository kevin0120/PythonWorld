参考文件
```bash
中文文档：
https://airflow.apachecn.org/#/zh/start
官方文档：
https://airflow.apache.org/docs/apache-airflow/stable/index.html
```

日志
```bash
日志格式：
{dag_id}/{task_id}/{execution_date}/{try_number}.log
```

import 路径逻辑
```bash
from pythontool.conf.configration.configuration import conf
1.每一层的init 文件 pythontool+conf+configration 执行
2.执行到from或者import则跳转到相应的模块中
```
打包
```bash
打包方式 setuptools

1.python setup.py sdist bdist_wheel 生成.whl 文件
2.该文件可以用pip install 的方式安装到python目录下
    a.package名称 airflow 原理 ./setup.cfg文件下files.packages= airflow
    b.pip install 后命令行可以直接运行airflow命令 原理./setup.cfg文件下
        options.entry_points.console_scripts= airflow=airflow.__main__:main
        这表示pip 可以在usr/local/bin 下生成airflow文件 可以直接在命令行运行
```

命令行 参数
```bash
1.再linux下 airflow 可以直接运行的原因:在/usr/local/bin 下有airflow文件
    以#!/usr/local/bin/python 开头 表示它可以直接用python 来运行airflow 文件
    https://blog.csdn.net/jackywgw/article/details/48847187
2. 参数 import argparse
        db init :

```

配置文件
```bash
from configparser import ConfigParser
1.先从airflow.config_templates.default_airflow.cfg文件读取默认配置
  从'# ----------------------- TEMPLATE BEGINS HERE -----------------------\n'开始读取
   字符串template

2. 将 字符串template中的变量变成真实的值 如 {AIRFLOW_HOME} 变成 C:\Users\admin
    使用 string.format 的方式
    all_vars = {k: v for d in [globals(), locals()] for k, v in d.items()}
    template.format(**all_vars)

3. 读取conf对象
        self.airflow_defaults = ConfigParser(*args, **kwargs)
        self.airflow_defaults.read_string(template)
4.判断os.path.isfile(AIRFLOW_CONFIG) 用户配置文件是否存在
    不存在则保存with open(AIRFLOW_CONFIG, 'w') as file:
                file.write(template)

5  从用户配置文件中再读一次conf 
    conf.read(AIRFLOW_CONFIG)
    此时的conf 其实与用户配置文件一致。


6.读取配置conf.get(section, key) 例如conf.get('core', 'FERNET_KEY')
    a.先查看改section ，key 有没有替代section1 key1
    b.先看环境变量里有没有 有的话 返回
        b1：AIRFLOW__{section.upper()}__{key.upper()} 有则返回
        b2：有几个特殊的参数还可以调用系统其他应用返回 位于：
            AIRFLOW__{section.upper()}__{key.upper()}_CMD
            AIRFLOW__{section.upper()}__{key.upper()}_SECRET

            ('database', 'sql_alchemy_conn'),
            ('core', 'fernet_key'),
            ('celery', 'broker_url'),
            ('celery', 'flower_basic_auth'),
            ('celery', 'result_backend'),
            ('atlas', 'password'),
            ('smtp', 'smtp_password'),
            ('webserver', 'secret_key'),
            # The following options are deprecated
            ('core', 'sql_alchemy_conn'),

     c.再看conf.airflow_defaults里有没有
        注意：
        # expand_env_var(os.environ.get('AIRFLOW_HOME', '~/airflow')):'C:\\Users\\admin/airflow'
        # expand_env_var(os.environ.get('AIRFLOW_HOME', '$GOPATH/airflow')):'C:\\Users\\admin\\go/airflow'


```
配置文件参数说明
```bash
expose_config = True  是否会在界面暴露config文件 Admin-Configration
dag_concurrency：每个 DAG 中允许并发运行的最大task instance数。
parallelism： 可以在 Airflow 中同时运行的最大任务实例数，跨scheduler和worker。
max_active_runs_per_dag：每个 DAG 运行的最大dag_run数。

```


环境变量
```bash
AIRFLOW_HOME：airflow的home路径   C:\Users\admin\airflow 
AIRFLOW_CONFIG：airflow的airflow.cfg文件路径  C:\Users\admin\airflow\airflow.cfg

AIRFLOW__{SECTION}__{KEY}：
    AIRFLOW__CORE__LOAD_EXAMPLES：  是否加载示例dags
    AIRFLOW__CORE__FERNET_KEY：在数据库中保存连接密码的密钥
    AIRFLOW__CORE__EXECUTOR： Airflow应使用的执行器类
    AIRFLOW__CORE__SQL_ALCHEMY_CONN：
        除了SequentialExecutor 使用默认配置的sqlite：
                sqlite:///{AIRFLOW_HOME}/airflow.db
        其他的Executor 都需要制定qlAlchemy connection string
            可以是这个环境变量 也可以是配置文件中的sql_alchemy_conn变量

        # qcos 环境变量
        # 是否通过消息队列发送拧紧结果，默认值: true
        ENV_PUBLISH_TIGHTENING_RESULT: "false"
        # 是否通过消息队列发送分析结果，默认值: true
        ENV_PUBLISH_ANALYSIS_RESULT: "false"
        # 是否通过消息队列发送二次确认结果，默认值: true
        ENV_PUBLISH_FINAL_RESULT: "false"
        # 是否通过消息队列发送曲线模板，默认值: true
        ENV_PUBLISH_CURVE_TEMPLATE: "false"
        # 是否通过消息队列发送曲线模板（批量），默认值: true
        ENV_PUBLISH_CURVE_TEMPLATE_DICT: "false"

```
DAG 参数说明
```bash
    :param dag_id: The id of the DAG; must consist exclusively of alphanumeric
        characters, dashes, dots and underscores (all ASCII)
    :type dag_id: str
    :param description: The description for the DAG to e.g. be shown on the webserver
    :type description: str
    :param schedule_interval: Defines how often that DAG runs, this
        timedelta object gets added to your latest task instance's
        execution_date to figure out the next schedule
    :type schedule_interval: datetime.timedelta or
        dateutil.relativedelta.relativedelta or str that acts as a cron
        expression
    :param start_date: The timestamp from which the scheduler will
        attempt to backfill
    :type start_date: datetime.datetime
    :param end_date: A date beyond which your DAG won't run, leave to None
        for open ended scheduling
    :type end_date: datetime.datetime
    :param template_searchpath: This list of folders (non relative)
        defines where jinja will look for your templates. Order matters.
        Note that jinja/airflow includes the path of your DAG file by
        default
    :type template_searchpath: str or list[str]
    :param template_undefined: Template undefined type.
    :type template_undefined: jinja2.StrictUndefined
    :param user_defined_macros: a dictionary of macros that will be exposed
        in your jinja templates. For example, passing ``dict(foo='bar')``
        to this argument allows you to ``{{ foo }}`` in all jinja
        templates related to this DAG. Note that you can pass any
        type of object here.
    :type user_defined_macros: dict
    :param user_defined_filters: a dictionary of filters that will be exposed
        in your jinja templates. For example, passing
        ``dict(hello=lambda name: 'Hello %s' % name)`` to this argument allows
        you to ``{{ 'world' | hello }}`` in all jinja templates related to
        this DAG.
    :type user_defined_filters: dict
    :param default_args: A dictionary of default parameters to be used
        as constructor keyword parameters when initialising operators.
        Note that operators have the same hook, and precede those defined
        here, meaning that if your dict contains `'depends_on_past': True`
        here and `'depends_on_past': False` in the operator's call
        `default_args`, the actual value will be `False`.
    :type default_args: dict
    :param params: a dictionary of DAG level parameters that are made
        accessible in templates, namespaced under `params`. These
        params can be overridden at the task level.
    :type params: dict
    :param concurrency: the number of task instances allowed to run
        concurrently
    :type concurrency: int
    :param max_active_runs: maximum number of active DAG runs, beyond this
        number of DAG runs in a running state, the scheduler won't create
        new active DAG runs
    :type max_active_runs: int
    :param dagrun_timeout: specify how long a DagRun should be up before
        timing out / failing, so that new DagRuns can be created. The timeout
        is only enforced for scheduled DagRuns.
    :type dagrun_timeout: datetime.timedelta
    :param sla_miss_callback: specify a function to call when reporting SLA
        timeouts.
    :type sla_miss_callback: types.FunctionType
    :param default_view: Specify DAG default view (tree, graph, duration,
                                                   gantt, landing_times), default tree
    :type default_view: str
    :param orientation: Specify DAG orientation in graph view (LR, TB, RL, BT), default LR
    :type orientation: str
    :param catchup: Perform scheduler catchup (or only run latest)? Defaults to True
    :type catchup: bool
    :param on_failure_callback: A function to be called when a DagRun of this dag fails.
        A context dictionary is passed as a single parameter to this function.
    :type on_failure_callback: callable
    :param on_success_callback: Much like the ``on_failure_callback`` except
        that it is executed when the dag succeeds.
    :type on_success_callback: callable
    :param access_control: Specify optional DAG-level permissions, e.g.,
        "{'role1': {'can_read'}, 'role2': {'can_read', 'can_edit'}}"
    :type access_control: dict
    :param is_paused_upon_creation: Specifies if the dag is paused when created for the first time.
        If the dag exists already, this flag will be ignored. If this optional parameter
        is not specified, the global config setting will be used.
    :type is_paused_upon_creation: bool or None
    :param jinja_environment_kwargs: additional configuration options to be passed to Jinja
        ``Environment`` for template rendering

        **Example**: to avoid Jinja from removing a trailing newline from template strings ::

            DAG(dag_id='my-dag',
                jinja_environment_kwargs={
                    'keep_trailing_newline': True,
                    # some other jinja2 Environment options here
                }
            )

        **See**: `Jinja Environment documentation
        <https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.Environment>`_

    :type jinja_environment_kwargs: dict
    :param tags: List of tags to help filtering DAGS in the UI.
    :type tags: List[str]


每天00：45
 schedule_interval='45 00 * * *'
每天08：01，09：01，10：01 到 22：01
schedule_interval='01 08-22/1 * * *'
每个周六的23：45
schedule_interval='45 23 * * 6'
每天01:00, 01:05, 01:10, 直到 03:55
schedule_interval='*/5 1,2,3 * * *'
schedule_interval='@hourly'


```
DAG example
```bash
example
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG("tutorial", default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)

t2.set_upstream(t1)
t3.set_upstream(t1)

```

曲线项目dags
```bash
airflow_log_cleanup
定期清理任务日志
analysis_failure_handler
分析异常处理DAG，当mq_result_storage接收到的结果中没有分析结果时，会创建一个该dag，用于手动进行重试。（见架构图）
curve_template_upgrade
曲线模板升级DAG，订阅消息队列中由cas发布的新模板并保存。（见架构图）
curve_training_dag
模板训练DAG。用户在界面上点击二次确认按钮后，会自动触发一个该DAG，将二次确认的结果和训练需要的数据通过http发送到cas中进行训练。（见架构图）
data_retention_policy
自动清除一段时间之前的数据（包括DagRun, TaskFail, TaskInstance, TaskReschedule, XCom, Log），时间由环境变量DATA_STORAGE_DURATION控制，默认值为30（天）
load_all_curve_tmpls
模板加载DAG，将持久化的模板加载到redis中。（见架构图）
mq_result_storage
结果保存DAG，通过rabbitmq订阅结果并保存。（见架构图）
publish_result_dag
结果推送DAG，将结果通过rabbitmq推送到外部系统。
report
通过邮件发送日报（项目中未实际使用）。
report_analysis_timeout
通过邮件发送分析超时报警（项目中未实际使用）。
report_retry
通过邮件发送分析任务重试数量报警（项目中未实际使用）。

```


Airflow Operator
```bash
BashOperator - 执行 bash 命令
PythonOperator - 调用任意 Python 函数
EmailOperator - 发送电子邮件
SimpleHttpOperator - 发送 HTTP 请求
MySqlOperator，SqliteOperator，PostgresOperator，MsSqlOperator，OracleOperator，JdbcOperator等 - 执行 SQL 命令
Sensor - 等待一定时间，文件，数据库行，S3 键等...

除了这些基本构建块之外，还有许多特定的 Operator ： DockerOperator，HiveOperator，
S3FileTransformOperator，PrestoToMysqlOperator，SlackOperator......你会明白的！

airflow/contrib/目录包含更多由社区构建的 Operator 。这些运算符并不总是像主发行版中那样完整或经过良好测试，但允许用户更轻松地向平台添加新功能。

```