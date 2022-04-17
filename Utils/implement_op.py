# -*- coding:utf-8 -*-

import json
import os
import re
import time
import logging
import datetime
import RequestsLibrary
import allure
import openpyxl

from SSHLibrary.library import SSHLibrary as ssh
from FtpLibrary import FtpLibrary
from ExternalLib.get_config_info import GetConfigInfo



log = logging.getLogger(__name__)
request = RequestsLibrary.RequestsLibrary()
connect = ssh()
gcf = GetConfigInfo()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))


class Implement:
    
    def connect_slurm(self, user, ip):
        connect.open_connection('??')
        login_result = connect.login('??', '??')
        log.info(login_result)
        CommonFunction().input("ssh {}@{}".format(user, ip))
        result_info = connect.read()
        log.info("ssh result_info {}".format(result_info))

    def close_connect(self):
        connect.close_connection()
        log.info("connection is close")


    @allure.step("git_clone")
    def git_clone(self, path, git_clone_command):
        log.info("path is {}".format(path))
        CommonFunction().input("cd" + " " + path)
        CommonFunction().input(git_clone_command, 120)
        log.info("git_clone_result:{}".format(git_clone_command))
        CommonFunction().input("mkdir log_file")
        CommonFunction().input("cd parrots.test")

    @allure.step("submodule start")
    def submodule(self, submodule_file, title, type=None):
        if type:
            init_command = list(gcf.get_dic_two_info(submodule_file, title).values())
            for i in range(len(init_command)):
                CommonFunction().input(init_command)
        else:
            init_command = list(gcf.get_dic_two_info(submodule_file, title).values())
            log.info("init_command is {}".format(init_command))
            for i in range(len(init_command)):
                CommonFunction().input(init_command[i])
    

    @allure.step("run command")
    def run_and_extract_result(self, need_end, run_command, delay_time, info):
        connect.write(run_command)
        log.info("will delay_time is {}s".format(delay_time))
        time.sleep(int(delay_time))
        if need_end == "y":
            if info:
                result_info = self.re_extract_result(info)
                if result_info:
                    log.info("result_info:{}".format(result_info))
                    return result_info
            else:
                result_info = connect.read()
                time.sleep(1)
                log.info("result_info is {}".format(result_info))
                return result_info
        elif need_end == "n":
            if info:
                result_info = self.re_extract_result(info)
                if result_info:
                    log.info("result_info:{}".format(result_info))
                    return result_info

    @staticmethod
    def re_extract_result(info):
        result_info = connect.read()
        time.sleep(2)
        p = re.compile(r"{}".format(info))
        result = re.findall(p, result_info)
        log.info("re_extract_result is {}".format(result))
        return result

class CommonFunction:

    @allure.step("input:")
    def input(self, input, wait_time=None):
        connect.write(input)
        if wait_time:
            time.sleep(wait_time)
        else:
            time.sleep(20)
        result_info = connect.read()
        log.info("connect result_info is {}".format(result_info))
        return result_info

    @allure.step("create_directory")
    def create_directory(self, path):
        input_path = os.path.split(path)
        CommonFunction().input("mkdir -p {}".format(input_path[0]))
        CommonFunction().input("cd" + " " + input_path[0])
        result = CommonFunction().input("ll | grep {}".format(input_path[1])).replace("rm -rf {}".format(input_path[1]), " ")
        log.info("input_path[1] is {}".format(input_path[1]))
        while input_path[1] in result:
            CommonFunction().input("rm -rf {} 2>&1 &".format(input_path[1]), 60)
            result = CommonFunction().input("ll | grep {}".format(input_path[1])).replace("rm -rf {}".format(input_path[1]), " ")
        CommonFunction().input("mkdir -p {}".format(input_path[1]))
        CommonFunction().input("cd")

    def check_env(self, env_ftype):
        self.input("source" + " " + env_ftype)
        env_result = CommonFunction().input("ll")
        if env_ftype == "pat_latest":
            env_key = re.compile(r"(pat\d+)")
            env = re.findall(env_key, env_result)
            log.info("env is {}".format(env_ftype))
            if env:
                env_enter = env[0]
            else:
                env_enter = env_ftype
        else:
            env_enter = env_ftype
        return env_enter

    def handle_file(self, file_path, xlsx_file, xlxs_tile):
        with open(file_path) as p:
            all_csv_list = list(p.readlines())
            log.info("all_csv_list is {}".format(all_csv_list))
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(xlxs_tile)
        for i in range(len(all_csv_list)):
            a = all_csv_list[i].split(" ")
            ws.append(a)
        wb.save(xlsx_file)
        self.input("exit")
    
   

class DownUploadFileNA:

    @staticmethod
    def connect_machine(ip0, user0, password0, machine_path=None):
        try:
            CommonFunction().input("ssh " + user0 + "@" + ip0)
            CommonFunction().input(password0)
            result_info = connect.read()
            log.info("machine result_info is {}".format(result_info))
            if machine_path:
                CommonFunction().input("mkdir -p {}".format(machine_path))
        except Exception as e:
            log.info("connect_machine is {}".format(e))
        finally:
            if "Are you sure you want to continue connecting" in result_info:
                CommonFunction().input("yes")
            return result_info

    def slurm_ftp_download(self, ftp_param, vnip, vnuser, vnps, machine_path, remote_file_list, local_file_list, bz=None):
        DownUploadFileNA.connect_machine(vnip, vnuser, vnps, machine_path)
        CommonFunction().input("exit")
        ftp = FtpLibrary()
        ftp.ftp_connect(host=ftp_param['ftp_server'],user=ftp_param['user'],password=ftp_param['passwd'],port=ftp_param['port'])
        for i in range(len(local_file_list)):
            if remote_file_list[i][0:4] == '/mnt':
                if bz:
                    remote_file = remote_file_list[i][4:] + '.bz2'
                else:
                    remote_file = remote_file_list[i][4:]
                local_file = local_file_list[i]
            try:
                ftp.download_file(remote_file, local_file)
            except Exception as e:
                log.info("ftp.download_file is {}".format(e))
        ftp.ftp_close()
         

    def slurm_ftp_upload(self, ftp_param, local_file_list, remote_file_list):
        ftp = FtpLibrary()
        ftp.ftp_connect(host=ftp_param['ftp_server'],user=ftp_param['user'],password=ftp_param['passwd'],port=ftp_param['port'])
        for i in range(len(local_file_list)):
            if remote_file_list[i][0:4] == '/mnt':
                remote_file = remote_file_list[i][4:]
                ftp.upload_file(local_file_list[i], remote_file)
        ftp.ftp_close()

    def compress_file(self, original):
        for i in range(len(original)):
            log_file = 'bzip2 -zkv ' + original[i]
            CommonFunction().input(log_file)

    def download_file(self, ip0, user0, password0, remote_list, local_list, machine_path=None, bz=None):
        self.connect_machine(ip0, user0, password0, machine_path)
        ftp = FtpLibrary()
        ftp.ftp_connect(ip0, user0, password0, port=21)
        for i in range(len(remote_list)):
            if bz:
                remote = remote_list[i].replace("/mnt", "") + "bz"
            else:
                remote = remote_list[i].replace("/mnt", "")
            log.info("remote is {}".format(remote))
            local = local_list[i]
            log.info("local is{}".format(local))
            try:
                ftp.download_file(remote, local)
            except Exception as e:
                log.info(e)
        ftp.ftp_close()
        log.info("ftp quit success")
        # connect.write("exit")
        # log.info("vndevice exit success")

    




