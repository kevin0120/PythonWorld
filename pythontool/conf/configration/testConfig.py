from configparser import ConfigParser


def write():
    config = ConfigParser()
    # When adding sections or items, add them in the reverse order of
    # how you want them to be displayed in the actual file.
    # In addition, please note that using RawConfigParser's and the raw
    # mode of ConfigParser's respective set functions, you can assign
    # non-string values to keys internally, but will receive an error
    # when attempting to write to a file or when you get it in non-raw
    # mode. SafeConfigParser does not allow such assignments to take place.
    config.add_section('Section1')
    config.set('Section1', 'an_int', '15')
    config.set('Section1', 'a_bool', 'true')
    config.set('Section1', 'a_float', '3.1415')
    config.set('Section1', 'baz', 'fun')
    config.set('Section1', 'bar', 'Python')
    config.set('Section1', 'foo', '%(bar)s is %(baz)s!')

    # Writing our configuration file to 'example.cfg'
    with open('example.cfg', 'w') as configfile:
        config.write(configfile)


# def insert():
#     config = ConfigParser()
#     config.read('example.cfg')
#
#     # Set the third, optional argument of get to 1 if you wish to use raw mode.
#     print(config.get('Section1', 'foo', 0))  # -> "Python is fun!"
#     print(config.get('Section1', 'foo', 1))  # -> "%(bar)s is %(baz)s!"
#
#     # The optional fourth argument is a dict with members that will take
#     # precedence in interpolation.
#     print(config.get('Section1', 'foo', 0, {'bar': 'Documentation',
#                                             'baz': 'evil'}))


def read():
    config = ConfigParser()
    config.read('example.cfg')

    # getfloat() raises an exception if the value is not a float
    # getint() and getboolean() also do this for their respective types
    a_float = config.getfloat('Section1', 'a_float')
    an_int = config.getint('Section1', 'an_int')
    print(a_float + an_int)

    # Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
    # This is because we are using a RawConfigParser().
    if config.getboolean('Section1', 'a_bool'):
        print(config.get('Section1', 'foo'))


if __name__ == '__main__':
    print("#############write##########")
    write()
    print("#############read##########")
    read()
    # print("#############insert##########")
    # insert()
