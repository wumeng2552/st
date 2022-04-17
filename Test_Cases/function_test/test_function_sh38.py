import os
import re
import time


import pytest
import logging


import sys
#print('Python %s on %s' % (sys.version, sys.platform))
from ExternalLib.get_config_info import GetConfigInfo
import allure

sys.path.extend(['/home/sensetime/python-project/PARRORSTEST'])

from ExternalLib.inpublic_function import CommonFunctionNA, DownUploadFileNA,AutoMakeIssueNA, ThroughIndicators
from SSHLibrary.library import SSHLibrary as ssh

connect = ssh()
log = logging.getLogger(__name__)
cf = CommonFunctionNA()
gcf = GetConfigInfo()
dlf = DownUploadFileNA()
ct = gcf.get_dic_two_info("/connect_file.ini", "function_sh38_machine")
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))



def setup_function():
    cf.connect_machine("function_sh38")
    cf.cd_command(20, "mkdir -p {}".format(ct["base_path"]))


def teardown_function():
    cf.close_connect()

@allure.feature("1080Ti")
def test_01_1080Ti():
    case_name = "1080Ti"
    cf.create_directory(ct["base_path"] + case_name)
    cf.git_clone(ct["base_path"] + case_name, ct["git_clone_command"])
    run_result_file = "/" + ct["pwd"] + ct["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/parrots.example")
    env_result = cf.check_env(ct["source_envi"])
    log.info("run start")
    run_command = "SRUN_ARGS='-p {} -w {}' nohup sh runner/example/train.sh {} 8 dpn92_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1 > /{} 2>&1 &".format(
        ct["partition"], ct["machine"], ct["partition"], run_result_file)
    cf.run_and_extract_result("n", run_command, 7500, "")
    cat_file = "cat {}".format(run_result_file)
    keyword = "benchmark_mem_cached"
    result = cf.run_and_extract_result("y", cat_file, 20, keyword)
    actual_info = []
    if result:
        if "benchmark_mem_cached" not in result[0]:
            actual_info.append("没有找到模型训练成功标志：benchmark_mem_cached")
    else:
        actual_info.append("没有找到模型训练成功标志：benchmark_mem_cached")
    if actual_info:
        summary = "1080Ti机器模型训练失败"
        expect_info = "1080Ti机器模型训练成功"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望：  {}\n 实际：  {}\n   备注：{}\n".format(ct["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name.lower()), expect_info, actual_info, ct["note"])
        try:
            # original_compress = [run_result_file]
            # dlf.compress_file(original_compress)
            local_run_result_file = "/" + ct["local_path"] + ct[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function_sh38", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(ct["task_name"], summary, description, ct["assignee"])
            #a.submit_issue(issue_upload_file, ct["label"], ct["components"])
        except Exception as e:
            log.info(e)
    if result:
        assert "benchmark_mem_cached"  in result[0], "期望找到模型训练成功标志：benchmark_mem_cached，实际{}".format(result)
    else:
        assert False, "期望找到模型训练成功标志：benchmark_mem_cached，实际{}".format(result)



