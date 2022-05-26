import 路径逻辑
```bash
from pythontool.conf.configration.configuration import conf
1.每一层的init 文件 pythontool+conf+configration 执行
2.执行到from或者import则跳转到相应的模块中
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



base
```bash
AIRFLOW_HOME：C:\Users\admin\airflow 
AIRFLOW_CONFIG：C:\Users\admin\airflow\airflow.cfg

```