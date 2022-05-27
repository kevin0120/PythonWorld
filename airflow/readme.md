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