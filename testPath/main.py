import os
import subprocess
import sys
import win32api


def get_usb_path():
    if os.name == 'nt':  # Windows系统
        win32api.ShellExecute(0, 'open', 'calc.exe', '', '', 1)
        drive_list = win32api.GetLogicalDriveStrings().split("\x00")[:-1]
        win32api.GetDriveType('C:\\')
        for drive in drive_list:
            if win32api.GetDriveType(drive) == win32api.DRIVE_REMOVABLE:
                return drive
    else:  # Linux系统
        with open('/proc/mounts', 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) > 2 and parts[2] == 'vfat':
                    if '/dev/sd' in parts[0] or '/dev/mmcblk' in parts[0]:
                        return parts[1]

    # 如果没有U盘挂载，则返回可执行文件所在目录
    return os.path.dirname(os.path.abspath(sys.argv[0]))


if __name__ == '__main__':
    usb_path = get_usb_path()
    print('U盘路径为：', usb_path)
