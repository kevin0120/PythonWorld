import os
import zipfile
import datetime
import io
import csv
import subprocess


class ProcessDataHistory:

    @classmethod
    def get_usb_path(cls):
        if os.name != 'nt':  # Windows系统
            # Linux系统
            with open('/proc/mounts', 'r') as f:
                aaa = f.readlines()
                for line in aaa:
                    parts = line.strip().split()
                    if len(parts) > 3 and 'rw' in parts[3] and '/dev/sd' in parts[0]:
                        statvfs = os.statvfs(parts[1])
                        print(statvfs)
                        result = subprocess.run(['sudo', 'fdisk', '-l'], stdout=subprocess.PIPE)
                        out = result.stdout.decode('utf-8')
                        print(out)
                        return parts[1]

        # 如果没有U盘挂载，则返回可执行文件所在目录
        return os.path.dirname(os.getcwd())


if __name__ == '__main__':
    a1 = __file__
    a = os.path.abspath(__file__)

    b = os.path.dirname(a)
    c = os.path.dirname(b)
    v = ""
    if not v:
        print('d')
    usb_path = ProcessDataHistory.get_usb_path()
    download_path = os.path.join(usb_path, 'download')
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    # 指定要创建的zip文件名和路径
    result_name = 'result' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = result_name + '.zip'
    zip_path = os.path.join(download_path, zip_name)
    # 创建ZipFile对象，并打开zip文件以便写入内容
    with zipfile.ZipFile(zip_path, 'w') as myzip:
        with io.StringIO() as csv_buffer:
            writer = csv.writer(csv_buffer)
            # 写入头信息
            writer.writerow('head')
            # 写入数据
            writer.writerows('new_tesults_array')
            # 将CSV数据写入Zip文件中
            myzip.writestr(result_name + '.csv', csv_buffer.getvalue())
        myzip.close()
    with open(zip_path, 'a+') as f:
        f.flush()
        os.fsync(f)
        f.close()
        # os.sync()
    os.system("sync")
    print('U盘路径为：', usb_path)
    print('U盘路径为：', download_path)
