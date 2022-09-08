import base64
import re


def read_bin(file_name):
    """
    function: read a bin file, return the string of the content in file
    """
    with open(file_name, "rb") as f:
        f_content = f.read()
        content = str(base64.b64encode(f_content), 'utf-8')
    return content


def is_base64_code(s):
    """Check s is Base64.b64encode"""
    if not isinstance(s, str) or not s:
        raise ValueError("params s not string or None")
    _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                    '2', '3', '4', '5', '6', '7', '8', '9', '+',
                    '/', '=']
    # Check base64 OR codeCheck % 4
    code_fail = [i for i in s if i not in _base64_code]
    if code_fail or len(s) % 4 != 0:
        return False
    return True


def isBase64(str):
    base64Pattern = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$";
    a = re.match(base64Pattern, str)
    return True if re.match(base64Pattern, str) else False


if __name__ == "__main__":
    a = "hello world!!!!!!"
    b = str(base64.b64encode(bytes(a, encoding="utf8")), 'utf-8')
    c = str(base64.b64encode(bytes(b, encoding="utf8")), 'utf-8')
    e = str(base64.b64encode(bytes(c, encoding="utf8")), 'utf-8')

    print(is_base64_code(b))
    print(isBase64(b))



    # d1 = base64.b64decode(a)
    d2 = str(base64.b64decode(b), 'utf-8')
    d3 = str(base64.b64decode(c), 'utf-8')
