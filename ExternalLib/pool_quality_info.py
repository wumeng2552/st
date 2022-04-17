import os
from platform import machine
import re
import time
import allure
import logging
from SSHLibrary.library import SSHLibrary as ssh
from datetime import datetime

from ExternalLib.get_config_info import GetConfigInfo
from Utils.implement_op import CommonFunction, DownUploadFileNA
from Utils.make_jira import AutoMakeIssueNA

connect = ssh()
log = logging.getLogger(__name__)
gcf = GetConfigInfo()
cp = gcf.get_dic_two_info("/connect_file.ini", "pool_1984_machine")
dlf = DownUploadFileNA()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class QualityTest:

    def quality_issue(self, ftpinfo, vnip, vnuser, vnps, machine_path, jira_remote_file_list, jira_local_file_list, check_info, git_clone_command, no_ap_run_mode, issue_title, assignee, label, components, local_path, base_path, frame):
        try:
            env_result = "pat_latest"
            # ###env_result = CommonFunction().check_env(cp["source_envi"])
            # #CommonFunction().input("conda deactivate")
            jira_remote_file_list_result = CommonFunction().input("wc -l {}".format(jira_remote_file_list[0])).replace("{}".format(jira_remote_file_list[0]), " ").replace("wc:", " ")
            log.info("{}jira_remote_file_list_result is {}".format(frame, jira_remote_file_list_result))
            if "0" not in jira_remote_file_list_result[0] and "No such file or directory" not in jira_remote_file_list_result:
                DownUploadFileNA().slurm_ftp_download(ftpinfo, vnip, vnuser, vnps, machine_path, jira_remote_file_list, jira_local_file_list)
                jira_folder = machine_path + frame
                with open(jira_local_file_list[0]) as p:
                    info = list(p.readlines())
                    log.info("jira_local_file_list info is {}".format(info))
                    model = []
                    issue_remote_file = []
                    issue_local_file = []
                    for i in range(len(info)):
                        model.append(info[i].split(" ")[1])
                        issue_remote_file.append(info[i].split(" ")[3].replace("\n", ""))
                        issue_local_file.append(jira_folder  + "/" + frame + "_" + info[i].split(" ")[1] + time_stamp + ".bz2")
                original_compress = issue_remote_file
                dlf.compress_file(original_compress)
                DownUploadFileNA().slurm_ftp_download(ftpinfo, vnip, vnuser, vnps, jira_folder, issue_remote_file, issue_local_file, "bz2")
                summary = "框架{}有{}个模型跑失败".format(frame, len(model))
                expect_info = "框架{} 所有模型跑成功,输出{}信息".format(frame, check_info)
                actual_info = "框架{}中的{}模型跑失败".format(frame, model)
                description = "分支: {}\n  环境: {}\n  期望： {}\n  实际: {}\n 启动模式: {}\n".format(git_clone_command, env_result, expect_info, actual_info, no_ap_run_mode)
                AutoMakeIssueNA(issue_title, summary, description, assignee).submit_issue(issue_local_file, label, components)
                CommonFunction().input("exit")
        except Exception as e:
            log.info("quality_issue e is {}".format(e))
    
    def compile(self, partition):
        CommonFunction().input("cd models/RetinaUnet")
        CommonFunction().input("git checkout autotest")
        CommonFunction().input("srun -p {} --gres=gpu:1 pip install -v -e . --user > RetinaUnet_log 2>&1 &".format(partition))
        CommonFunction().input("cd ../../")
        CommonFunction().input("cd models/sr_v3.0/lib/_ext")
        CommonFunction().input("srun -p {} --gres=gpu:1 pip install -v -e . --user > sr_v3.0_log 2>&1 &".format(partition))
        CommonFunction().input("cd ../../../../")
        CommonFunction().input("cd models/deformable_detr/models/ops")
        CommonFunction().input("srun -p {} --gres=gpu:1 -n1 python setup.py build > deformable_detr_log 2>&1 &".format(partition))
        CommonFunction().input("cd ../../../../")
        CommonFunction().input("cd models/mmdetection3d")
        CommonFunction().input("srun -p {} -n1 --gres=gpu:1 python setup.py develop --user >mmdetection3d_log 2>&1 &".format(partition))
        CommonFunction().input("cd ../../")

            
    