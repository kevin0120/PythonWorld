import os


def get_usb_path():
    if os.name != 'nt':  # Windows系统
        # Linux系统
        with open('/proc/mounts', 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) > 2 and parts[2] == 'vfat':
                    if '/dev/sd' in parts[0] or '/dev/mmcblk' in parts[0]:
                        return parts[1]

    # 如果没有U盘挂载，则返回可执行文件所在目录
    return os.path.dirname(os.getcwd())


if __name__ == '__main__':
    usb_path = get_usb_path()
    download_path = os.path.join(usb_path, 'download')
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    filename = 'qqq1.txt'
    filepath = os.path.join(download_path, filename)
    with open(filepath, 'w') as f:
        f.write("this is a example")

    print('U盘路径为：', usb_path)
    print('U盘路径为：', download_path)
