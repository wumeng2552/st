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
from ExternalLib.pool_quality_info import QualityTest


log = logging.getLogger(__name__)
dlf = DownUploadFileNA()
gcf = GetConfigInfo()
cp = gcf.get_dic_two_info("/connect_file.ini", "pool_1984_machine")
ftpif = gcf.get_dic_two_info("/connect_file.ini", "slurm_1984_ftp")
log.info(ftpif["slurm_1984"])
ti = ThroughIndicators()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))

quality_shell_one = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/shell_file/quality_shell_one.sh"
quality_shell_two = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/shell_file/quality_shell_two.sh"
shell_path = [quality_shell_one, quality_shell_two]
machine_path = "/" + cp["local_path"] + cp["base_path"] + "{}/Data/".format(cp["case_name"])
slurm_1984 = {
            'hostname' : '??',
            'hostip': '??',
            'ftp_server': '??',
            'port': 21,
            'user': '??',
            'passwd': '??'
        }


class TestaQualityEveryModel():
     
    
    @staticmethod
    def setup_class():
        log.info("start time is{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        Implement().connect_slurm(cp["user"], cp["ip"])
        

    def teardown_class(self):
        Implement().close_connect()

    def test_001_run_model(self):
        RunModel().run_model_noap(cp["pwd"], cp["base_path"], cp["case_name"], cp["task_name"], cp["git_clone_command"], ["pool_model_noap.ini"], ["export_run_model"], ["quality_run_model"], cp["partition"], cp["run_time"], "submodule_command.ini", "pool_submodule_command", cp["source_envi"], slurm_1984, shell_path, [cp["machine"], cp["machine"]], "compile", 48560)          #, "compile", 48560


@allure.feature("mmdet")
class Test001mmdet():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        log.info("jira start is")
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmdet", time_stamp)]
        jira_local_file_list = ["{}mmdet_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        try:
            QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmdet")
        except Exception as e:
            log.info("quality_issue e is {}".format(e))
        finally:
            Implement().close_connect()



    def test_001_mmdet_mask_rcnn_x101_32x4d_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "mask_rcnn_x101_32x4d_fpn_1x_coco", ["speed"])

    def test_002_mmdet_faster_rcnn_r50_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "faster_rcnn_r50_fpn_1x_coco", ["speed"])

    def test_003_mmdet_retinanet_r50_fpn_fp16_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "retinanet_r50_fpn_fp16_1x_coco", ["speed"])
    
    def test_004_mmdet_mask_rcnn_r101_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "mask_rcnn_r101_fpn_1x_coco", ["speed"])
    
    def test_005_mmdet_cascade_mask_rcnn_r50_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "cascade_mask_rcnn_r50_fpn_1x_coco", ["speed"])
    
    def test_006_mmdet_mask_rcnn_r50_caffe_fpn_mstrain_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "mask_rcnn_r50_caffe_fpn_mstrain_1x_coco", ["speed"])
    
    def test_007_mmdet_mask_rcnn_r50_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "mask_rcnn_r50_fpn_1x_coco", ["speed"])
    
    def test_008_mmdet_cascade_rcnn_r50_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "cascade_rcnn_r50_fpn_1x_coco", ["speed"])
    
    def test_009_mmdet_mask_rcnn_r50_fpn_fp16_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "mask_rcnn_r50_fpn_fp16_1x_coco", ["speed"])
    
    def test_010_mmdet_retinanet_r50_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "retinanet_r50_fpn_1x_coco", ["speed"])
    def test_011_mmdet_ssd300_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "ssd300_coco", ["speed"])
    
    def test_012_mmdet_faster_rcnn_r50_fpn_fp16_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "faster_rcnn_r50_fpn_fp16_1x_coco", ["speed"])
    
    def test_013_mmdet_mask_rcnn_x101_64x4d_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "mask_rcnn_x101_64x4d_fpn_1x_coco", ["speed"])
    
    def test_014_mmdet_faster_rcnn_r50_fpn_dconv_c3c5_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "faster_rcnn_r50_fpn_dconv_c3-c5_1x_coco", ["speed"])
    
    def test_015_mmdet_fsaf_r50_fpn_1x_coco(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdet", "fsaf_r50_fpn_1x_coco", ["speed"])


@allure.feature("pod")
class Test002pod():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("pod", time_stamp)]
        jira_local_file_list = ["{}pod_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "pod")


    def test_001_pod_faster_rcnn_R50_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-R50-FPN-1x", ["speed"])
    

    def test_002_pod_faster_rcnn_R50_FPN_1x_mix (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-R50-FPN-1x_mix" , ["speed"])
    
    def test_003_pod_retinanet_R50_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "retinanet-R50-1x" , ["speed"])
    
    def test_004_pod_mask_rcnn_R50_FPN_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "mask-rcnn-R50-FPN-1x" , ["speed"])
    
    def test_005_pod_mask_rcnn_R50_FPN_1x_mix (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "mask-rcnn-R50-FPN-1x_mix" , ["speed"])
    
    def test_006_pod_keypoint_rcnn_R50_FPN_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "mask-rcnn-R50-FPN-1x_mix" , ["speed"])
    
    def test_007_pod_keypoint_rcnn_R50_FPN_1x_mix  (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "keypoint-rcnn-R50-FPN-1x_mix"  , ["speed"])
    
    def test_008_pod_rfcn_R101_ohem_deform_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "rfcn-R101-ohem-deform-1x" , ["speed"])
    
    def test_009_pod_cascade_rcnn_R50_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "cascade-rcnn-R50-FPN-1x", ["speed"])
    
    def test_010_pod_grid_rcnn_R50_FPN_2x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "grid-rcnn-R50-FPN-2x" , ["speed"])
    
    def test_011_pod_faster_rcnn_R50_NASFPN_1x_mix (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-R50-NASFPN-1x_mix" , ["speed"])
    def test_012_pod_faster_rcnn_mobilenet_FPN_1x  (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-mobilenet-FPN-1x"  , ["speed"])
    
    def test_013_pod_faster_rcnn_shufflenet_FPN_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-shufflenet-FPN-1x" , ["speed"])
    
    def test_014_pod_rfcn_mobilenet_1x  (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "rfcn-mobilenet-1x"  , ["speed"])
    
    def test_015_pod_rfcn_shufflenet_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "rfcn-shufflenet-1x" , ["speed"])
    
    def test_016_pod_retinanet_R50_ghm_1x (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "retinanet-R50-ghm-1x" , ["speed"])
    
    def test_017_pod_faster_rcnn_R50_FPN_1x_DCN_C3_C5(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-R50-FPN-1x-DCN@C3-C5", ["speed"])
    
    def test_018_pod_retinanet_R50_GN_FA (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "retinanet-R50-GN-FA" , ["speed"])
    
    def test_019_pod_faster_rcnn_R50_PAFPN_1x_mix(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod", "faster-rcnn-R50-PAFPN-1x_mix", ["speed"])
  

@allure.feature("alphatrion")
class Test003alphatrion():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("alphatrion", time_stamp)]
        jira_local_file_list = ["{}alphatrion_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "alphatrion")


    def test_001_alphatrion_mobilenet_v2_fp32_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "mobilenet_v2_fp32_benchmark", ["speed"])
    
    def test_002_alphatrion_mobilenet_v2_fp16_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "mobilenet_v2_fp16_benchmark", ["speed"])
    
    def test_003_alphatrion_se_resnet50_fp32_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "se_resnet50_fp32_benchmark", ["speed"])
    
    def test_004_alphatrion_se_resnet50_fp16_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "se_resnet50_fp16_benchmark", ["speed"])
    
    def test_005_alphatrion_resnet50_fp32_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "resnet50_fp32_benchmark", ["speed"])
    
    def test_006_alphatrion_resnet50_fp16_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "resnet50_fp16_benchmark", ["speed"])
    
    def test_007_alphatrion_resnet101_fp32_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "resnet101_fp32_benchmark", ["speed"])
    
    def test_008_alphatrion_resnet101_fp16_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion", "resnet101_fp16_benchmark", ["speed"])


@allure.feature("seg_nas")
class Test004seg_nas():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("seg_nas", time_stamp)]
        jira_local_file_list = ["{}seg_nas_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "seg_nas")

    def test_001_seg_nas_single_path_oneshot(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "seg_nas", "single_path_oneshot", ["speed"])

@allure.feature("ssd")
class Test005ssd():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("ssd", time_stamp)]
        jira_local_file_list = ["{}ssd_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "ssd")

    def test_001_ssd_ssd_FSAF_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "ssd", "ssd_FSAF_benchmark", ["speed"])

    def test_002_ssd_ssd_Retina_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "ssd", "ssd_Retina_benchmark", ["speed"])

@allure.feature("alphatrion_nas")
class Test006alphatrion_nas():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("alphatrion_nas", time_stamp)]
        jira_local_file_list = ["{}alphatrion_nas_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "alphatrion_nas")

    def test_001_alphatrion_nas_super_resnet_range1_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion_nas", "super_resnet_range1_benchmark", ["speed"])

    def test_002_alphatrion_nas_super_resnet_range1_fp16_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "alphatrion_nas", "super_resnet_range1_fp16_benchmark", ["speed"])


@allure.feature("seg")
class Test007seg():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("seg", time_stamp)]
        jira_local_file_list = ["{}seg_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "seg")

    def test_001_seg_pspnet_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "seg", "pspnet.benchmark", ["speed"])

    def test_002_seg_deeplab_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "seg", "deeplab.benchmark", ["speed"])

    def test_003_seg_mobilenet_v2_plus_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "seg", "mobilenet_v2_plus.benchmark", ["speed"])

@allure.feature("example")
class Test008example():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("example", time_stamp)]
        jira_local_file_list = ["{}example_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "example")

    def test_001_example_dpn92_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "dpn92_mix.benchmark", ["speed"])
    
    def test_002_example_dpn92_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "dpn92.benchmark", ["speed"])
    
    def test_003_example_inception_v4_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_v4.benchmark", ["speed"])
    
    def test_004_example_inception_v4_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_v4_mix.benchmark", ["speed"])
    
    def test_005_example_resnet50_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet50.benchmark", ["speed"])
    
    def test_006_example_resnet50_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet50_mix.benchmark", ["speed"])
    
    def test_007_example_se_resnet50_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "se_resnet50.benchmark", ["speed"])
    
    def test_008_example_se_resnet50_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "se_resnet50_mix.benchmark", ["speed"])
    
    def test_009_example_shuffle_v2_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "shuffle_v2.benchmark", ["speed"])
    
    def test_010_example_shuffle_v2_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "shuffle_v2_mix.benchmark", ["speed"])
    
    def test_011_example_mobile_v2_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "mobile_v2.benchmark", ["speed"])
    
    def test_012_example_mobile_v2_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "mobile_v2_mix.benchmark", ["speed"])
    
    def test_013_example_resnet18_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet18.benchmark", ["speed"])
    
    def test_014_example_resnet18_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet18_mix.benchmark", ["speed"])
    
    def test_015_example_resnet101_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet101.benchmark", ["speed"])
    
    def test_016_example_resnet101_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet101_mix.benchmark", ["speed"])
    
    def test_017_example_resnet152_benchmark (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet152.benchmark" , ["speed"])
    
    def test_018_example_resnet152_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "resnet152_mix.benchmark", ["speed"])
    
    def test_019_example_inception_v2_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_v2.benchmark", ["speed"])
    
    def test_020_example_inception_v2_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_v2_mix.benchmark", ["speed"])
    
    def test_021_example_inception_v3_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_v3.benchmark", ["speed"])
    
    def test_022_example_inception_v3_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_v3_mix.benchmark", ["speed"])
    
    def test_023_example_inception_resnet_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_resnet.benchmark", ["speed"])
    
    def test_024_example_inception_resnet_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "example", "inception_resnet_mix.benchmark", ["speed"])

@allure.feature("mouth")
class Test009mouth():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mouth", time_stamp)]
        jira_local_file_list = ["{}mouth_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mouth")

    def test_001_mouth_dpn92_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mouth", "v2", ["speed"])
    
@allure.feature("light_nas")
class Test010light_nas():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("light_nas", time_stamp)]
        jira_local_file_list = ["{}light_nas_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "light_nas")

    def test_001_light_nas_dpn92_mix_benchmark(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "light_nas", "single_path_oneshot_search", ["speed"])

@allure.feature("pod_v3.1.0")
class Test011pod_v3_1_0():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("pod_v3.1.0", time_stamp)]
        jira_local_file_list = ["{}pod_v3.1.0_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "pod_v3.1.0")


    def test_001_pod_v3_1_0_faster_rcnn_R50_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "faster-rcnn-R50-FPN-1x", ["speed"])

    def test_002_pod_v3_1_0_mask_rcnn_R50_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "mask-rcnn-R50-FPN-1x" , ["speed"])
    
    def test_003_pod_v3_1_0_cascade_rcnn_R50_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "cascade-rcnn-R50-FPN-1x", ["speed"])
    
    def test_004_pod_v3_1_0_fcos_R50_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "fcos-R50-1x", ["speed"])
    
    def test_005_pod_v3_1_0_effnetd0_bifpn_retina_32epoch(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "effnetd0-bifpn-retina-32epoch", ["speed"])
    
    def test_006_pod_v3_1_0_faster_rcnn_R50_FPN_1x_ms_test_aug(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "faster-rcnn-R50-FPN-1x-ms-test-aug", ["speed"])
    
    def test_007_pod_v3_1_0_grid_rcnn_R50_FPN_2x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "grid-rcnn-R50-FPN-2x", ["speed"])
    
    def test_008_pod_v3_1_0_keypoint_rcnn_R50_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "keypoint-rcnn-R50-FPN-1x", ["speed"])
    
    def test_009_pod_v3_1_0_mask_rcnn_R50_FPN_2x_lvis(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "mask-rcnn-R50-FPN-2x-lvis", ["speed"])
    
    def test_010_pod_v3_1_0_retinanet_R50_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "retinanet-R50-1x", ["speed"])
    
    def test_011_pod_v3_1_0_faster_rcnn_R50_FPN_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "faster-rcnn-R50-FPN-cityscapes", ["speed"])
    
    def test_012_pod_v3_1_0_faster_rcnn_R50_FPN_openimages(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "faster-rcnn-R50-FPN-openimages", ["speed"])
    
    def test_013_pod_v3_1_0_faster_rcnn_mobilenet_FPN_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "faster-rcnn-mobilenet-FPN-1x", ["speed"])
    
    def test_014_pod_v3_1_0_rfcn_R101_ohem_deform_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "rfcn-R101-ohem-deform-1x", ["speed"])
    
    def test_015_pod_v3_1_0_rfcn_shufflenet_1x(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "rfcn-shufflenet-1x", ["speed"])
    
    def test_016_pod_v3_1_0_centernetkp511_R101_60epoch(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.1.0", "centernetkp511-R101-60epoch", ["speed"])

@allure.feature("mmaction")
class Test012mmaction():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmaction", time_stamp)]
        jira_local_file_list = ["{}mmaction_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmaction")

    def test_001_mmaction_i3d_r50_video_32x2x1_100e_kinetics400_rgb(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "i3d_r50_video_32x2x1_100e_kinetics400_rgb", ["speed"])
    
    def test_002_mmaction_r2plus1d_r34_video_8x8x1_180e_kinetics400_rgb(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "r2plus1d_r34_video_8x8x1_180e_kinetics400_rgb", ["speed"])
    
    def test_003_mmaction_slowfast_r50_video_4x16x1_256e_kinetics400_rgb(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "slowfast_r50_video_4x16x1_256e_kinetics400_rgb", ["speed"])
    
    def test_004_mmaction_slowonly_r50_video_4x16x1_256e_kinetics400_rgb(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "slowonly_r50_video_4x16x1_256e_kinetics400_rgb", ["speed"])
    
    def test_005_mmaction_tsm_r50_video_1x1x8_100e_kinetics400_rgb(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "tsm_r50_video_1x1x8_100e_kinetics400_rgb", ["speed"])
    
    def test_006_mmaction_tsn_r50_video_1x1x8_100e_kinetics400_rgb(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "tsn_r50_video_1x1x8_100e_kinetics400_rgb", ["speed"])
    
    def test_007_mmaction_bmn_400x100_2x8_9e_activitynet_feature(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmaction", "bmn_400x100_2x8_9e_activitynet_feature", ["speed"])

@allure.feature("mmseg")
class Test013mmseg():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmseg", time_stamp)]
        jira_local_file_list = ["{}mmseg_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmseg")

    def test_001_mmseg_fcn_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "fcn_r101-d8_512x1024_40k_cityscapes", ["speed"])
   
    def test_002_mmseg_fcn_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "fcn_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_003_mmseg_ann_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "ann_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_004_mmseg_ann_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "ann_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_005_mmseg_ccnet_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "ccnet_r101-d8_512x1024_40k_cityscapes", ["speed"])
    def test_006_mmseg_ccnet_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "ccnet_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_007_mmseg_deeplabv3plus_r101_d8_512x1024_40k_cityscapes (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "deeplabv3plus_r101-d8_512x1024_40k_cityscapes" , ["speed"])
    
    def test_008_mmseg_deeplabv3plus_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "deeplabv3plus_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_009_mmseg_deeplabv3_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "deeplabv3_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_010_mmseg_deeplabv3_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "deeplabv3_r50-d8_512x1024_40k_cityscapes", ["speed"])
    def test_011_mmseg_encnet_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "encnet_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_012_mmseg_encnet_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "encnet_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_013_mmseg_fcn_hr18s_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "fcn_hr18s_512x1024_40k_cityscapes", ["speed"])
    
    def test_014_mmseg_fcn_hr18_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "fcn_hr18_512x1024_40k_cityscapes", ["speed"])
    def test_015_mmseg_gcnet_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "gcnet_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_016_mmseg_gcnet_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "gcnet_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_017_mmseg_nonlocal_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "nonlocal_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_018_mmseg_nonlocal_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "nonlocal_r50-d8_512x1024_40k_cityscapes", ["speed"])
    def test_019_mmseg_ocrnet_hr18s_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "ocrnet_hr18s_512x1024_40k_cityscapes", ["speed"])
    
    def test_020_mmseg_ocrnet_hr18_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "ocrnet_hr18_512x1024_40k_cityscapes", ["speed"])
    
    def test_021_mmseg_psanet_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "psanet_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_022_mmseg_psanet_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "psanet_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_023_mmseg_pspnet_r101_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "pspnet_r101-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_024_mmseg_pspnet_r50_d8_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "pspnet_r50-d8_512x1024_40k_cityscapes", ["speed"])
    
    def test_025_mmseg_upernet_r101_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "upernet_r101_512x1024_40k_cityscapes", ["speed"])
    
    def test_026_mmseg_upernet_r50_512x1024_40k_cityscapes(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmseg", "upernet_r50_512x1024_40k_cityscapes", ["speed"])

@allure.feature("mmediting")
class Test014mmediting():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmediting", time_stamp)]
        jira_local_file_list = ["{}mmediting_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmediting")

    def test_001_mmediting_cyclegan_lsgan_id0_resnet_in_1x1_246200_summer2winter(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "cyclegan_lsgan_id0_resnet_in_1x1_246200_summer2winter", ["speed"])
    
    def test_002_mmediting_deepfillv2_256x256_8x2_celeba(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "deepfillv2_256x256_8x2_celeba", ["speed"])
    
    def test_003_mmediting_dim_stage2_v16_pln_1x1_1000k_comp1k(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "dim_stage2_v16_pln_1x1_1000k_comp1k", ["speed"])
    
    def test_004_mmediting_edsr_x2c64b16_g1_300k_div2k(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "edsr_x2c64b16_g1_300k_div2k", ["speed"])
    
    def test_005_mmediting_esrgan_psnr_x4c64b23g32_g1_1000k_div2k(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "esrgan_psnr_x4c64b23g32_g1_1000k_div2k", ["speed"])
    
    def test_006_mmediting_gl_256x256_8x12_celeba(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "gl_256x256_8x12_celeba", ["speed"])
    
    def test_007_mmediting_indexnet_mobv2_1x16_78k_comp1k (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "indexnet_mobv2_1x16_78k_comp1k" , ["speed"])
    
    def test_008_mmediting_msrresnet_x4c64b16_g1_1000k_div2k(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "msrresnet_x4c64b16_g1_1000k_div2k", ["speed"])
    
    def test_009_mmediting_pconv_256x256_stage1_8x1_celeba(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "pconv_256x256_stage1_8x1_celeba", ["speed"])
    
    def test_010_mmediting_pix2pix_vanilla_unet_bn_1x1_80k_facades(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "pix2pix_vanilla_unet_bn_1x1_80k_facades", ["speed"])
    
    def test_011_mmediting_srcnn_x4k915_g1_1000k_div2k(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmediting", "srcnn_x4k915_g1_1000k_div2k", ["speed"])

@allure.feature("TextRecog")
class Test015TextRecog():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("TextRecog", time_stamp)]
        jira_local_file_list = ["{}TextRecog_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "TextRecog")

    def test_001_TextRecog_print_Middle(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "TextRecog", "print_Middle", ["speed"])
    
    def test_002_TextRecog_print_Big(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "TextRecog", "print_Big", ["speed"])
    
    def test_003_TextRecog_print_MiddleV2(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "TextRecog", "print_MiddleV2", ["speed"])
    
    def test_004_TextRecog_crnn(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "TextRecog", "crnn", ["speed"])


@allure.feature("mmpose")
class Test016mmpose():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmpose", time_stamp)]
        jira_local_file_list = ["{}mmpose_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmpose")

    def test_001_mmpose_bottomup_hrnet(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "bottomup_hrnet", ["speed"])
    
    def test_002_mmpose_topdown_alexnet  (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_alexnet"  , ["speed"])
    
    def test_003_mmpose_topdown_darkpose (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_darkpose" , ["speed"])
    
    def test_004_mmpose_topdown_hourglass(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_hourglass", ["speed"])
    
    def test_005_mmpose_topdown_hrnet(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_hrnet", ["speed"])
    
    def test_006_mmpose_topdown_mobilev2(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_mobilev2", ["speed"])
    
    def test_007_mmpose_topdown_res50(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_res50", ["speed"])
    
    def test_008_mmpose_topdown_resnetv1d(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_resnetv1d", ["speed"])
    
    def test_009_mmpose_topdown_resnext (self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_resnext" , ["speed"])
    
    def test_010_mmpose_topdown_scnet(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_scnet", ["speed"])
    
    def test_011_mmpose_topdown_senet50(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_senet50", ["speed"])
    
    def test_012_mmpose_topdown_shufflev1(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmpose", "topdown_shufflev1", ["speed"])

@allure.feature("sketch")
class Test017sketch():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("sketch", time_stamp)]
        jira_local_file_list = ["{}sketch_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "sketch")

    def test_001_sketch_vgg1_4_3(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "sketch", "vgg1.4.3", ["speed"])
    
    def test_002_sketch_mobilenet1_0_0(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "sketch", "mobilenet1.0.0", ["speed"])
    
    def test_003_sketch_vggfusion(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "sketch", "vggfusion", ["speed"])

@allure.feature("mmtrack")
class Test018mmtrack():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmtrack", time_stamp)]
        jira_local_file_list = ["{}mmtrack_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmtrack")

    def test_001_mmtrack_config13ms_bn1(self):ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmtrack", "config13ms_bn1", ["speed"])
    
    def test_002_mmtrack_config1ms_lr(self):ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmtrack", "config1ms_lr", ["speed"])
    
    def test_003_mmtrack_siamrpnpp(self):ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmtrack", "siamrpnpp", ["speed"])

@allure.feature("RetinaUnet")
class Test019RetinaUnet():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("RetinaUnet", time_stamp)]
        jira_local_file_list = ["{}RetinaUnet_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "RetinaUnet")

    def test_001_RetinaUnet_2d_runet_infer(self):ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "RetinaUnet", "2d_runet_infer", ["speed"])

@allure.feature("pod_v2.3.0")
class Test020pod_v2_3_0():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("pod_v2.3.0", time_stamp)]
        jira_local_file_list = ["{}pod_v2.3.0_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "pod_v2.3.0")

    def test_001_pod_v2_3_0_retinanet_v11_18w(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v2.3.0", "retinanet-v11-18w", ["speed"])

    def test_002_pod_v2_3_0_fcos_v11_80w_stride4(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v2.3.0", "fcos-v11-80w-stride4", ["speed"])

@allure.feature("pod_v3.0")
class Test021pod_v3_0():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("pod_v3.0", time_stamp)]
        jira_local_file_list = ["{}pod_v3.0_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "pod_v3.0")

    def test_001_pod_v3_0_mask_rcnn_R152_FPN_1x_h(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pod_v3.0", "mask-rcnn-R152-FPN-1x-h", ["speed"])


@allure.feature("prototype")
class Test022prototype():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("prototype", time_stamp)]
        jira_local_file_list = ["{}prototype_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "prototype")

    def test_001_prototype_resnet50(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "prototype", "resnet50", ["speed"])

    def test_002_prototype_shufflev2(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "prototype", "shufflev2", ["speed"])

@allure.feature("encoder")
class Test023encoder():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("encoder", time_stamp)]
        jira_local_file_list = ["{}encoder_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "encoder")

    def test_001_encoder_benign(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "encoder", "benign", ["speed"])

@allure.feature("sensemedical")
class Test024sensemedical():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("sensemedical", time_stamp)]
        jira_local_file_list = ["{}sensemedical_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "sensemedical")

    def test_001_sensemedical_Task01_BrainTumour(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "sensemedical", "Task01_BrainTumour", ["speed"])

@allure.feature("Pattern")
class Test025Pattern():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("Pattern", time_stamp)]
        jira_local_file_list = ["{}Pattern_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "Pattern")

    def test_001_Pattern_attribute_config(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Pattern", "attribute_config", ["speed"])
    
    def test_002_Pattern_eye_best_config_parrots(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Pattern", "eye_best_config_parrots", ["speed"])
    
    def test_003_Pattern_example_fusion_small_pytorch(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Pattern", "example_fusion_small_pytorch", ["speed"])

    def test_004_Pattern_gaze_example(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Pattern", "gaze_example", ["speed"])

@allure.feature("instance_seg")
class Test026instance_seg():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("instance_seg", time_stamp)]
        jira_local_file_list = ["{}instance_seg_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "instance_seg")

    def test_001_instance_seg_yolact_mobilenetv2_concat_32_coco_config(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "instance_seg", "yolact_mobilenetv2_concat_32_coco_config", ["speed"])

@allure.feature("detr")
class Test027detr():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("detr", time_stamp)]
        jira_local_file_list = ["{}detr_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "detr")

    def test_001_detr_detr(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "detr", "detr", ["speed"])


@allure.feature("sr_v3.0_0")
class Test028sr_v3_0_0():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("sr_v3.0_0", time_stamp)]
        jira_local_file_list = ["{}sr_v3.0_0_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "sr_v3.0_0")

    def test_001_sr_v3_0_0_F4_0_300(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "sr_v3.0_0", "F4_0_300", ["speed"])


@allure.feature("heart_seg")
class Test029heart_seg():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("heart_seg", time_stamp)]
        jira_local_file_list = ["{}heart_seg_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "heart_seg")

    def test_001_heart_seg_resvnet(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "heart_seg", "resvnet", ["speed"])

@allure.feature("coronary_seg")
class Test030coronary_seg():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("coronary_seg", time_stamp)]
        jira_local_file_list = ["{}coronary_seg_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "coronary_seg")

    def test_001_coronary_seg_resvnet(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "coronary_seg", "resvnet", ["speed"])


@allure.feature("mmdetection3d")
class Test031mmdetection3d():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmdetection3d", time_stamp)]
        jira_local_file_list = ["{}mmdetection3d_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmdetection3d")

    def test_001_mmdetection3d_votenet_16x8_sunrgbd_3d_10class(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "votenet_16x8_sunrgbd-3d-10class", ["speed"])
    
    def test_002_mmdetection3d_votenet_8x8_scannet_3d_18class(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "votenet_8x8_scannet-3d-18class", ["speed"])
    
    def test_003_mmdetection3d_hv_second_secfpn_6x8_80e_kitti_3d_3class(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "hv_second_secfpn_6x8_80e_kitti-3d-3class", ["speed"])
    
    def test_004_mmdetection3d_hv_second_secfpn_6x8_80e_kitti_3d_car(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "hv_second_secfpn_6x8_80e_kitti-3d-car", ["speed"])
    
    def test_005_mmdetection3d_hv_PartA2_secfpn_2x8_cyclic_80e_kitti_3d_3class(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "hv_PartA2_secfpn_2x8_cyclic_80e_kitti-3d-3class", ["speed"])
    
    def test_006_mmdetection3d_hv_PartA2_secfpn_2x8_cyclic_80e_kitti_3d_car(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "hv_PartA2_secfpn_2x8_cyclic_80e_kitti-3d-car", ["speed"])
    
    def test_007_mmdetection3d_hv_pointpillars_secfpn_6x8_160e_kitti_3d_3class(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class", ["speed"])
    
    def test_008_mmdetection3d_hv_pointpillars_secfpn_6x8_160e_kitti_3_car(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmdetection3d", "hv_pointpillars_secfpn_6x8_160e_kitti-3d-car", ["speed"])

@allure.feature("deformable_detr")
class Test032deformable_detr():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("deformable_detr", time_stamp)]
        jira_local_file_list = ["{}deformable_detr_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "deformable_detr")

    def test_001_deformable_detr_r50_deformable_detr_plus_iterative_bbox_refinement_plus_plus_two_stage(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "deformable_detr", "r50_deformable_detr_plus_iterative_bbox_refinement_plus_plus_two_stage", ["speed"])

@allure.feature("pattern_v2_5_sp")
class Test033pattern_v2_5_sp():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("deformable_detr", time_stamp)]
        jira_local_file_list = ["{}pattern_v2_5_sp_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "pattern_v2_5_sp")

    def test_001_pattern_v2_5_sp_V2_6_sp_cos_pretrain_honda(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "pattern_v2_5_sp", "V2_6_sp_cos_pretrain_honda", ["speed"])
       
@allure.feature("PAR")
class Test034PAR():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("PAR", time_stamp)]
        jira_local_file_list = ["{}PAR_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "PAR")

    def test_001_PAR_res101(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "PAR", "res101", ["speed"])
    
@allure.feature("Multi_organ_seg_HR")
class Test035Multi_organ_seg_HR():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("PSPNet", time_stamp)]
        jira_local_file_list = ["{}Multi_organ_seg_HR_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "PSPNet")

    def test_001_Multi_organ_seg_HR_PSPNet(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Multi_organ_seg_HR", "PSPNet", ["speed"])

@allure.feature("mmocr")
class Test036mmocr():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("PSPNet", time_stamp)]
        jira_local_file_list = ["{}mmocr_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "PSPNet")

    def test_001_mmocr_panet_r18_fpem_ffm_sbn_1x_ctw1500(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmocr", "panet_r18_fpem_ffm_sbn_1x_ctw1500", ["speed"])
    
    def test_002_mmocr_panet_r18_fpem_ffm_sbn_1x_icdar2015(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmocr", "panet_r18_fpem_ffm_sbn_1x_icdar2015", ["speed"])
    
    def test_003_mmocr_psenet_r50_fpnf_sbn_1x_icdar2015(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmocr", "psenet_r50_fpnf_sbn_1x_icdar2015", ["speed"])
    
    def test_004_mmocr_psenet_r50_fpnf_sbn_1x_ctw1500(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmocr", "psenet_r50_fpnf_sbn_1x_ctw1500", ["speed"])

@allure.feature("Crowd")
class Test037Crowd():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("PSPNet", time_stamp)]
        jira_local_file_list = ["{}Crowd_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "PSPNet")

    def test_001_Crowd_vgg_csr(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Crowd", "vgg_csr", ["speed"])

    def test_002_Crowd_vgg_sfa(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "Crowd", "vgg_sfa", ["speed"])


@allure.feature("SenseStar")
class Test038SenseStar():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("PSPNet", time_stamp)]
        jira_local_file_list = ["{}SenseStar_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "PSPNet")

    def test_001_SenseStar_sensestar(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "SenseStar", "sensestar", ["speed"])
    
@allure.feature("springce_psot")
class Test039springce_psot():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("PSPNet", time_stamp)]
        jira_local_file_list = ["{}springce_psot_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "PSPNet")

    def test_001_springce_psot_vot_non_siam(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "springce_psot", "vot_non_siam", ["speed"])
    
    def test_002_springce_psot_vot_res50_dilation_multirpn(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "springce_psot", "vot_res50-dilation-multirpn", ["speed"])
    
    def test_003_springce_psot_vot_res50_interp_multirpn_focal_loss(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "springce_psot", "vot_res50-interp-multirpn-focal_loss", ["speed"])
    
    def test_004_springce_psot_vot_res50_interp_multirpn_focal_loss_atss(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "springce_psot", "vot_res50-interp-multirpn-focal_loss-atss", ["speed"])
    
    def test_005_springce_psot_vot_res50_interp_multirpn_focal_loss_atss_smoothl1(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "springce_psot", "vot_res50-interp-multirpn-focal_loss-atss-smoothl1", ["speed"])
    
    def test_006_springce_psot_vot_res50_interp_multirpn_focal_loss_topk(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "springce_psot", "vot_res50-interp-multirpn-focal_loss-topk", ["speed"])

@pytest.mark.flaky(reruns=2, reruns_delay=4)
@allure.feature("mmocr_ctc")
class Test040mmocr_ctc():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("mmocr_ctc", time_stamp)]
        jira_local_file_list = ["{}mmocr_ctc_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "mmocr_ctc")

    @pytest.mark.flaky(reruns=2, reruns_delay=1260)
    def test_001_mmocr_ctc_icdar2013_ctc(self):
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "mmocr_ctc", "icdar2013_ctc", ["speed"])


@allure.feature("vision_transformer")
class Test041vision_transformer():

    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])

    def teardown_class(self):
        jira_remote_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/jira/{}_jira{}".format("vision_transformer", time_stamp)]
        jira_local_file_list = ["{}vision_transformer_jira{}".format(machine_path, time_stamp)]
        log.info("jira_remote_file_list is {}".format(jira_remote_file_list))
        QualityTest().quality_issue(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], machine_path, jira_remote_file_list, jira_local_file_list, "speed", cp["git_clone_command"], cp["no_ap_run_mode"], cp["issue_title"], cp["assignee"], cp["label"], cp["components"], cp["local_path"], cp["base_path"], "vision_transformer")
        Implement().close_connect()

    @pytest.mark.flaky(reruns=2, reruns_delay=1260)
    def test_001_vision_transformer_b16(self):
        log.info("test_001_vision_transformer_b16 is rerun")
        ThroughIndicators().check_result(cp["pwd"], cp["base_path"], cp["case_name"], "vision_transformer", "b16", ["speed"])


class TestXlxsFile():
    
    @staticmethod
    def setup_class():
        Implement().connect_slurm(cp["user"], cp["ip"])
        

    def teardown_class(self):
        Implement().close_connect()

    def test_001_xlxs_file(self):
        all_remote_model_file_list = ["/" + cp["pwd"] + cp["base_path"] + cp["case_name"] + "/parrots.test/all_result_model{}".format(time_stamp)]
        all_local_file_list = [machine_path + "all_model{}".format(time_stamp)]
        log.info("all_remote_model_file_list is {}".format(all_remote_model_file_list))
        DownUploadFileNA().slurm_ftp_download(slurm_1984, cp["vnip"], cp["vnuser"], cp["vnps"], "", all_remote_model_file_list, all_local_file_list)
        xlsx_file = machine_path + "all_model{}.xlsx".format(time_stamp)
        CommonFunction().handle_file(all_local_file_list[0], xlsx_file, [u"框架", u"模型", u"速度"])


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_quality_noap_every_model.py'])