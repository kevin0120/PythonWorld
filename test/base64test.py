import base64


def read_bin(file_name):
    """
    function: read a bin file, return the string of the content in file
    """
    with open(file_name, "rb") as f:
        f_content = f.read()
        content = str(base64.b64encode(f_content), 'utf-8')
    return content


if __name__ == "__main__":
    a = "hello world!!!!!!"
    b = str(base64.b64encode(bytes(a, encoding="utf8")), 'utf-8')
    c = str(base64.b64encode(bytes(b, encoding="utf8")), 'utf-8')
    e = str(base64.b64encode(bytes(c, encoding="utf8")), 'utf-8')

    # d1 = base64.b64decode(a)
    d2 = str(base64.b64decode(b), 'utf-8')
    d3 = str(base64.b64decode(c), 'utf-8')
