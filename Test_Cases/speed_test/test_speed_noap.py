# -*- coding:utf-8 -*-
import logging
import re
import sys
import time
import csv
import allure
import pytest
import os

sys.path.extend(['/home/sensetime/python-project/parrots_new'])

from ExternalLib.get_config_info import GetConfigInfo
from Utils.implement_op import DownUploadFileNA, CommonFunction, Implement
from Utils.run_model import RunModel
from Utils.check_test import ThroughIndicators
from ExternalLib.speed_all_info import SpeedTest


log = logging.getLogger(__name__)
dlf = DownUploadFileNA()
gcf = GetConfigInfo()
cs = gcf.get_dic_two_info("/connect_file.ini", "speed_1984_machine")
ftpif = gcf.get_dic_two_info("/connect_file.ini", "slurm_1984_ftp")
log.info(ftpif["slurm_1984"])
ti = ThroughIndicators()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))


dummydataset_shell_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/shell_file/speed_dummydataset.sh"
benchmark_8_shell_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/shell_file/speed_benchmark_8.sh"
benchmark_16_shell_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/shell_file/speed_benchmark_16.sh"
shell_list = [dummydataset_shell_path, benchmark_8_shell_path, benchmark_16_shell_path]
machine_path = "/" + cs["local_path"] + cs["base_path"] + "{}/Data/".format(cs["case_name"])
slurm_1984 = {
            'hostname' : '??',
            'hostip': '??',
            'ftp_server': '??',
            'port': 21,
            'user': '??',
            'passwd': '??'
        }
run_model_file_ini_list = ["speed_model_noap.ini", "speed_model_noap.ini", "speed_model_noap.ini"]
export_run_model_list = ["export_run_dummydataset", "export_run_benchmark_8", "export_run_benchmark_16"]
run_model_file_ini_title_list = ["dummydataset_8_gpu_model", "benchmark_8_gpu_model", "benchmark_16_gpu_model"]
machine = [cs["machine"], cs["machine"], cs["machine_more"]]
dummydataset_info = ["speed_value.ini", "dummydataset_speed_value", "speed_yuzhi_env_info.ini", "yuzhi_env_info", "parrots", [], [], cs["source_envi"]]
benchmark_info = ["speed_value.ini", "benchmark_speed_value", "speed_yuzhi_env_info.ini", "yuzhi_env_info", "parrots", [], [], cs["source_envi"]]
speed_base_info = [cs["git_clone_command"], cs["no_ap_run_mode"], cs["issue_title"], cs["assignee"], cs["label"], cs["components"], cs["local_path"], cs["base_path"], cs["case_name"], cs["source_envi"], cs["partition"]]



class Test001SpeedRunModel():
     
    
    @staticmethod
    def setup_class():
        log.info("start time is {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        Implement().connect_slurm(cs["user"], cs["ip"])
        

    def teardown_class(self):
        Implement().close_connect()

    def test_001_run_model(self):
        RunModel().run_model_noap(cs["pwd"], cs["base_path"], cs["case_name"], cs["task_name"], cs["git_clone_command"], run_model_file_ini_list, export_run_model_list, run_model_file_ini_title_list, cs["partition"], cs["run_time"], "submodule_command.ini", "speed_submodule_command", cs["source_envi"], slurm_1984, shell_list, machine, "", 19000)



@allure.feature("TestbSpeedCheck")
class Test002SpeedCheck():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cs["user"], cs["ip"])

    def teardown_class(self):
        log.info("jira start is")
        jira_remote_file_list = ["/" + cs["pwd"] + cs["base_path"] + cs["case_name"] + "/parrots.test/jira/{}_jira{}".format(cs["case_name"], time_stamp)]
        jira_local_file_list = ["{}speed_jira{}{}".format(machine_path, cs["case_name"], time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        try:
            SpeedTest().speed_issue(slurm_1984, cs["vnip"], cs["vnuser"], cs["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, speed_base_info)
        except Exception as e:
            log.info("speed_issue e is {}".format(e))
        finally:
            Implement().close_connect()


    def test_001_alphatrion_mobilenet_v2_fp32_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "mobilenet_v2_fp32_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_002_alphatrion_mobilenet_v2_fp16_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "mobilenet_v2_fp16_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_003_alphatrion_se_resnet50_fp32_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "se_resnet50_fp32_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_004_alphatrion_se_resnet50_fp16_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "se_resnet50_fp16_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_005_alphatrion_resnet50_fp32_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "resnet50_fp32_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_006_alphatrion_resnet50_fp16_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "resnet50_fp16_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_007_alphatrion_resnet50_fp17_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "resnet101_fp32_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_008_alphatrion_resnet50_fp18_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "alphatrion", "resnet101_fp16_benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_009_seg_nas_resnet50_fp18_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "seg_nas", "single_path_oneshot", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_010_example_dpn92_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "dpn92_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_011_example_dpn92_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "dpn92.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_012_example_inception_v4_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_v4.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_013_example_inception_v4_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_v4_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_014_example_resnet50_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet50.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_015_example_resnet50_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet50_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_016_example_se_resnet50_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "se_resnet50.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_017_example_se_resnet50_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "se_resnet50_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_018_example_shuffle_v2_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "shuffle_v2.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_019_example_shuffle_v2_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "shuffle_v2_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_020_example_mobile_v2_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "mobile_v2.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_021_example_mobile_v2_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "mobile_v2_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_022_example_resnet18_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet18.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_023_example_resnet18_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet18_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_024_example_resnet101_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet101.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_025_example_resnet101_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet101_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_026_example_resnet152_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet152.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_027_example_resnet152_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "resnet152_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_028_example_inception_v2_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_v2.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_029_example_inception_v2_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_v2_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_030_example_inception_v3_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_v3.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_031_example_inception_v3_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_v3_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_032_example_inception_resnet_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_resnet.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)
    
    def test_033_example_inception_resnet_mix_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "example", "inception_resnet_mix.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", dummydataset_info)

# ########################################################benchmark###############################################################3
    def test_034_seg_mobilenet_v2_plus_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "seg", "mobilenet_v2_plus.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", benchmark_info)

    def test_035_seg_pspnet_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "seg", "pspnet.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", benchmark_info)

    def test_036_seg_deeplab_benchmark(self):
        ThroughIndicators().check_result(cs["pwd"], cs["base_path"], cs["case_name"], "seg", "deeplab.benchmark", ["speed","alloc","cached","pure_training_time","total_time"], "speed", benchmark_info)
    

class Test003XlxsFile():
    
    @staticmethod
    def setup_class():
        Implement().connect_slurm(cs["user"], cs["ip"])
        

    def teardown_class(self):
        Implement().close_connect()

    def test_001_xlxs_file(self):
        all_remote_model_file_list = ["/" + cs["pwd"] + cs["base_path"] + cs["case_name"] + "/parrots.test/all_result_model{}".format(time_stamp)]
        all_local_file_list = [machine_path + "all_model{}".format(time_stamp)]
        log.info("all_remote_model_file_list is {}".format(all_remote_model_file_list))
        DownUploadFileNA().slurm_ftp_download(slurm_1984, cs["vnip"], cs["vnuser"], cs["vnps"], machine_path, all_remote_model_file_list, all_local_file_list)
        xlsx_file = machine_path + "speed_all_model_result{}.xlsx".format(time_stamp)
        CommonFunction().handle_file(all_local_file_list[0], xlsx_file, [u"框架", u"模型", u"版本环境", u"阈值环境", u"阈值", u"速度", "alloc_result", "cached_result", "pure_training_time_result","total_time_result", "end_result", u"文件路径"])