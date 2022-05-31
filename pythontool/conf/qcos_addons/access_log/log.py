import json
import sys
from typing import Callable, TypeVar, cast
from pythontool.conf.qcos_addons.access_log.constants import CUSTOM_LOG_FORMAT, CUSTOM_EVENT_NAME_MAP, \
    CUSTOM_PAGE_NAME_MAP
from datetime import datetime
import logging
from airflow.settings import TIMEZONE
from airflow.utils.session import create_session
import functools

T = TypeVar("T", bound=Callable)

_logger = logging.getLogger(__name__)


def access_log(event, page, msg):
    '''
    一个装饰器，用于将访问事件记录日志，供抓取分析，格式和参数对照见constants.py文件
    示例：
    @access_log('VIEW', 'CURVES', '查看曲线对比页面')
    '''

    def decorator(func: T) -> T:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _logger.info(repr(args))
            _logger.info(repr(kwargs))

            _logger.info("co_name:{} ".format(func.__code__.co_name))  # 返回函数名
            _logger.info("co_argcount:{} ".format(func.__code__.co_argcount))  # 返回函数的参数个数
            _logger.info("co_varnames:{} ".format(func.__code__.co_varnames))  # 返回函数的参数
            _logger.info("co_filename:{} ".format(func.__code__.co_filename))  # 返回文件绝对路径
            _logger.info("co_consts:{} ".format(func.__code__.co_consts))
            _logger.info("co_firstlineno:{} ".format(func.__code__.co_firstlineno))  # 返回函数行号
            _logger.info("co_kwonlyargcount:{} ".format(func.__code__.co_kwonlyargcount))  # 关键字参数
            _logger.info("co_nlocals:{} ".format(func.__code__.co_nlocals))  # 返回局部变量个数

            ret = func(*args, **kwargs)
            from flask_login import current_user  # noqa: F401
            full_msg = CUSTOM_LOG_FORMAT.format(
                datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d %H:%M:%S"),
                current_user if current_user and current_user.is_active else 'anonymous',
                getattr(current_user, 'last_name', '') if current_user and current_user.is_active else 'anonymous',
                CUSTOM_EVENT_NAME_MAP[event], CUSTOM_PAGE_NAME_MAP[page], msg
            )
            _logger.info(full_msg)
            return ret

        return cast(T, wrapper)

    return decorator


@access_log('LOGOUT', 'LOGOUT', '登出')
def logout(*args, **kwargs):
    print("hello world")


if __name__ == '__main__':
    print("rrr{}".format(sys.path))
    logout("hello", "world", a="ni", b="hao")
