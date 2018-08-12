import sys
import re
import os
import os.path
import ftplib
from ftplib import FTP
import time
import platform

FTP_SERVER = "192.168.125.1"
FTP_USER = "liugefeng"
FTP_PASSWORD = "Liu131003"
PLATFORM = platform.system()

# =========================================================================
# className: ftpClient
# Comment  : ftp客户端, 负责文件的上传/下载和删除等功能
# =========================================================================
class ftpClient:
    def __init__(self, ftp_server, user, password):
        self.ftp_server = ftp_server
        self.user = user
        self.password = password

    # =====================================================================
    # 登陆ftp
    # =====================================================================
    def login(self):
        try:
            self.ftp = FTP(self.ftp_server)
        except(socket.error, socket.gaierror):
            print("Fail to connect ftp server " + self.ftp_server + "!")
            return False

        try:
            self.ftp.login(self.user, self.password)
            print(self.ftp.getwelcome())
            return True
        except(ftplib.error_perm):
            print("failed to login ftp server " + self.ftp_server + \
                    " with user name \"" + self.user + "\"")
            return False

    # =====================================================================
    # 判断给定目录是否为ftp上的目录
    # =====================================================================
    def is_directory(self, server_path):
        server_path = server_path.strip()

        if server_path == "/":
            return True

        cur_path = self.ftp.pwd()
        try:
            self.ftp.cwd(server_path)
        except(ftplib.error_perm):
            return False

        try:
            self.ftp.cwd(cur_path)
        except(ftplib.error_perm):
            return False

        return True

    # =====================================================================
    # 上传指定文件列表中的文件到指定目录
    # =====================================================================
    def upload(self, server_path, lst_files):
        # 列表为空
        if not len(lst_files):
            print("No file specified to upload!")
            return True

        # 列表中有文件不存在
        for item in lst_files:
            item = item.strip()
            if not os.path.exists(item):
                print("file " + item + " not exists!")
                return False

        # 切换服务器路径
        server_path = server_path.strip()
        if server_path:
            try:
                self.ftp.cwd(server_path)
            except(ftplib.error_perm):
                print("Failed to change ftp server path ftp " + server_path + "!")
                return False

        cur_local_path = os.getcwd()
        for item in lst_files:
            item = item.strip()

            # 切换本地，并上传文件
            lst_items = os.path.split(item)
            local_path = lst_items[0]
            local_file = lst_items[1]

            if local_path != "" and local_path != ".":
                os.chdir(local_path)

            # 上传文件
            file_handle = open(local_file, "rb")
            try:
                self.ftp.storbinary('STOR ' + local_file, file_handle, 1024)
            except(ftplib.error_perm):
                print("Failed to upload file \"" + item + "\" to server path \"" + \
                        server_path + "\"!")
                return False

            os.chdir(cur_local_path)

        print(str(len(lst_files)) + " files uploaded onto ftp server " + self.ftp_server + "!")
        return True

    # =====================================================================
    # 下载指定目录下的所有文件合目录
    # =====================================================================
    def download(self, server_path, lst_download_files):
        server_path = server_path.strip()

        # 切换服务器目录
        if server_path:
            self.ftp.cwd(server_path)

        download_num = 0
        for item in lst_download_files:
            file_handle = open(item, "wb")
            download_num += 1
            try:
                self.ftp.retrbinary("RETR " + item, file_handle.write, 1024)
            except(ftplib.error_perm):
                print("Failed to download file " + item + "!")
                continue
        print("All " + download_num + " files downloaded form ftp!")

    # =====================================================================
    # 在服务器上创建指定名称的目录
    # =====================================================================
    def mkdir(self, dir_name):
        # 如果目录存在，则直接返回
        if self.is_directory(dir_name):
            return True

        # 目录不存在，则创建目录
        try:
            self.ftp.mkd(dir_name)
        except(ftplib.error_perm):
            print("Error: Failed to mkdir " + dir_name + "!")
            return False

        return True

    # =====================================================================
    # 重命名指定文件
    # =====================================================================
    def rename(self, upload_path, lst_newest_files):
        file_prefix = getFilePrefix()

        if upload_path:
            try:
                self.ftp.cwd("/" + upload_path)
            except(ftplib.error_perm):
                print("Error: failed to change ftp server path to " + upload_path + "!")
                return False

        for item in lst_newest_files:
            self.ftp.rename(item, file_prefix + "_" + item)

        return True


    # =====================================================================
    # 退出ftp登陆
    # =====================================================================
    def quit(self):
        try:
            self.ftp.quit()
        except(ftplib.error_perm):
            print("Error: failed to quit from ftp server " + self.ftp_server + "!")
            return False

        print("Quit from ftp server " + self.ftp_server + "!")
        return True

# =====================================================================
# 根据当前日期生成文件要上传到服务器的目录名称(如：2018-08-11)
# =====================================================================
def getDirForToday():
    time_str = time.strftime("%Y-%m-%d", time.localtime())
    return time_str

# =====================================================================
# 根据当前提起生成服务器上文件的前缀名称
# =====================================================================
def getFilePrefix():
    time_str = time.strftime("%H-%M-%S", time.localtime())
    return time_str

if __name__ == "__main__":
    file_num = len(sys.argv[1:])
    if file_num <= 0:
        print("Error: no valie files need to upload.")
        exit()

    # find valid files need to upload
    lst_upload_files = []
    lst_newest_files = []
    for item in sys.argv[1:]:
        # check whether file exists
        if not os.path.exists(item):
            print("Warning: file " + item + " not exists!")
            continue

        lst_upload_files.append(item)
        cur_file = os.path.basename(item)
        lst_newest_files.append(cur_file)

    # no files need to upload
    if len(lst_upload_files) <= 0:
        print("Error: no valid files need to upload!")
        exit()

    # upload files
    print("upload files ...")
    upload_path = getDirForToday()

    ftp_client = ftpClient(FTP_SERVER, FTP_USER, FTP_PASSWORD)
    ftp_client.login()

    ftp_client.mkdir(upload_path)
    ftp_client.upload(upload_path, lst_upload_files)
    ftp_client.rename(upload_path, lst_newest_files)
    ftp_client.quit()
    print("upload finished.")
