# -*- coding:utf-8 -*-

import json
import os
import re
import time
import logging
import datetime
import RequestsLibrary
import allure

from SSHLibrary.library import SSHLibrary as ssh
from FtpLibrary import FtpLibrary
from ExternalLib.get_config_info import GetConfigInfo
from ExternalLib.pool_quality_info import QualityTest
from Utils.implement_op import Implement, CommonFunction, DownUploadFileNA


log = logging.getLogger(__name__)
request = RequestsLibrary.RequestsLibrary()
connect = ssh()
gcf = GetConfigInfo()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))

class RunModel(Implement):

    # def __init__(self, user, ip):
    #     super().__init__(user, ip)

    def run_model_noap(self, pwd, base_path, case_name, task_name, git_clone_command, run_model_file_ini, export_run_model_list, run_model_file_ini_title, partition, run_time, submodule_ini_file, submodule_ini_title, env, ftp_param, shell_local_file, machine, compile=None, sleep_time=None):
        try:
            log.info("run_model_noap start")
            CommonFunction().create_directory(base_path + case_name)
            self.git_clone(base_path + case_name, git_clone_command)
            #CommonFunction().input("cd /mnt/lustre/parrots.tester.s.03/1102test/linshi/pool_sy/pool_sy0/quality_noap0/parrots.test")
            self.submodule(submodule_ini_file, submodule_ini_title)
            if compile:
                QualityTest().compile(partition)
            self.make_implement_shell_file(pwd, base_path, case_name, task_name, run_model_file_ini, export_run_model_list, run_model_file_ini_title, partition, run_time, env, ftp_param, shell_local_file, "jira", machine, sleep_time)
        except Exception as e:
            log.info("run_model_noap fail result is {}".format(e))


    def make_implement_shell_file(self, pwd, base_path, case_name, task_name, run_model_file_ini, export_run_model_list, run_model_file_ini_title, partition, run_time, env, ftp_param, shell_local_list, jira_folder=None, machine=None,sleep_time=None):
        CommonFunction().input("cd")
        CommonFunction().input("cd {}".format("/" + pwd + base_path + case_name + "/parrots.test"))
        shell_remote_list = []
        flag = True
        for i in range(len(shell_local_list)):
            shell_remote_file = "/" + pwd + base_path + case_name + "/parrots.test/{}shell{}.sh".format(i, time_stamp)
            shell_remote_list.append(shell_remote_file)
        DownUploadFileNA().slurm_ftp_upload(ftp_param, shell_local_list, shell_remote_list)
        for i in range(len(shell_local_list)):
            result = CommonFunction().input("ll | grep {}".format("{}shell{}.sh".format(i, time_stamp))).replace("ll | grep {}".format("{}shell{}.sh".format(i, time_stamp)), " ")
            log.info("shell_local_file result is {}".format(result))
            if "{}shell{}.sh".format(i, time_stamp) not in result:
                flag = False
                shell_remote_file = "/" + pwd + base_path + case_name + "/" + "parrots.test/" + case_name + "_" + task_name + time_stamp + str(i) + ".sh"
                shell_remote_list.append(shell_remote_file)
                log.info("shell_remote_file is {}".format(shell_remote_file))
                export = list(gcf.get_dic_two_info(run_model_file_ini[i], export_run_model_list[i]).values())
                for k in range(len(export)):
                    if k == 0:
                        export_sh = "echo  '{}' > {}".format(export[k], shell_remote_file)
                    else:
                        export_sh = "sed -i '$a " + export[k] + "'" + " " + shell_remote_file
                    log.info("export_sh is {}".format(export_sh))
                    CommonFunction().input(export_sh)
                run_model = gcf.get_dic_three_split_list_info(run_model_file_ini[i], run_model_file_ini_title[i], ",")
                for j in range(len(run_model)):
                    log_file = "/" + pwd + base_path + case_name + "/" + "log_file/" + run_model[j][0].strip(" ") + "_" + run_model[j][2].strip(" ")
                    run_command = "nohup sh runner/" + run_model[j][0].strip(" ")  + "/train.sh" + " " + partition + " " + \
                                    run_model[j][1] + " " + run_model[j][2] + " " + run_model[j][3] + " > " + log_file + " 2>&1 &"
                    log.info("run_command is {}".format(run_command))
                    sh_run = "sed -i '$a " + run_command + "'" + " " + shell_remote_file
                    log.info("sh_run is {}".format(sh_run))
                    CommonFunction().input(sh_run)
        CommonFunction().check_env(env)
        if jira_folder:
            CommonFunction().input("mkdir -p {}".format("/" + pwd + base_path + case_name + "/parrots.test/jira"))
        for i in range(len(shell_local_list)):
            if flag:
                if machine:
                    sh_run_command = "SRUN_ARGS='-p {} {} -t {}' sh {} {} {} {} {}".format(partition, machine[i], run_time, shell_remote_list[i], pwd, base_path, case_name, partition)
                else:
                    sh_run_command = "SRUN_ARGS='-p {} -t {}' sh {} {} {} {} {}".format(partition, run_time, shell_remote_list[i], pwd, base_path, case_name, partition)
            else:
                if machine:
                    sh_run_command = "SRUN_ARGS='-p {} {} -t {} ' sh {}".format(partition, machine[i], run_time, shell_remote_list[i])
                else:
                    sh_run_command = "SRUN_ARGS='-p {} -t {}' sh {}".format(partition, run_time, shell_remote_list[i])

            log.info("sh_run_command is {}".format(sh_run_command))
            CommonFunction().input(sh_run_command, 60)
        log.info("end time is {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        CommonFunction().input("squeue | grep {}".format(partition), sleep_time)
        
        
