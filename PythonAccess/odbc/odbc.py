import pyodbc

if __name__ == '__main__':
    a = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
    b = pyodbc.drivers()
    print(a)
