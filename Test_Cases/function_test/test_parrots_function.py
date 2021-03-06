import os
import csv
import re
import time
import unicodecsv as ucsv


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
cn = gcf.get_dic_two_info("/connect_file.ini", "function_1984_machine")
ti = ThroughIndicators()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))


def setup_function():
    cf.connect_machine("function")
    cf.cd_command(20, "mkdir -p {}".format(cn["base_path"]))


def teardown_function():
    cf.close_connect()

function_csv_list = []

parame_dataloader_s = [("nohup sh dataloader_test.sh dfe s ", 300, "dfe s"),
                     ("nohup sh dataloader_test.sh afe s ", 300, "afe s"),
                     ("nohup sh dataloader_test.sh ase s ", 300, "ase s"),
                     ("nohup sh dataloader_test.sh aae s ", 300, "aae s"),
                     ("nohup sh dataloader_test.sh as s ", 300, "as s"),
                     ("nohup sh dataloader_test.sh sar s ", 300, "sar s"),
                     ("nohup sh dataloader_test.sh drw s ", 300, "drw s")]
ids_s = ["dfe s", "afe s", "ase s", "aae s", "as s", "sar s", "drw s"]
parame_dataloader_m = [("sh dataloader_test.sh dfe m ", 400, "dfe m"),
                     ("nohup sh dataloader_test.sh afe m ", 400, "afe m"),
                     ("nohup sh dataloader_test.sh ase m ", 400, "ase m"),
                     ("nohup sh dataloader_test.sh aae m ", 400, "aae m"),
                     ("nohup sh dataloader_test.sh as m ", 400, "as m"),
                     ("nohup sh dataloader_test.sh sar m ", 400, "sar m"),
                     ("nohup sh dataloader_test.sh drw m ", 400, "drw m")]
ids_m = ["dfe m", "afe m", "ase m", "aae m", "as m", "sar m", "drw m"]


@pytest.mark.parametrize("run_type, delay_time, type", parame_dataloader_s, ids=ids_s)
@allure.feature("dataloader_single")
def test_01_dataloader_single(run_type, delay_time, type):
    type_name = ("_").join(type.split(" "))
    case_name = "dataloader_single_{}".format(type_name)
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/dataloader")
    env_result = cf.check_env(cn["source_envi"])
    keyword = "Test Passed"
    run_commad = run_type + cn["partition"] + "  >>  " + "/" + run_result_file + " " + "2>&1 &"
    cf.run_and_extract_result("n", run_commad, delay_time, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y", cat_file, 10, keyword)
    actual_info = []
    if result:
        if "Test Passed" not in result[0]:
            actual_info.append("dataloader {} ????????????, ?????????Test Passed".format(type))
    else:
        actual_info.append("dataloader {} ????????????, ?????????Test Passed".format(result))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dataloader {} ????????????".format(type)
        expect_info = "dataloader {} ????????????".format(type)
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:   {}\n  ??????: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
        try:
            # original_compress = [run_result_file]
            # dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global function_csv_list
    csv_list = [u"python???_dataloader", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "Test Passed" in result[0], "????????????Test Passed!??????,????????????{}".format(result[0])
    else:
        assert False, "????????????Test Passed!??????,????????????"


@pytest.mark.parametrize("run_type, delay_time, type", parame_dataloader_m, ids=ids_m)
@allure.feature("dataloader_multi")
def test_02_dataloader_multi(run_type, delay_time, type):
    type_name = ("_").join(type.split(" "))
    case_name = "dataloader_multi_{}".format(type_name)
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/dataloader")
    env_result = cf.check_env(cn["source_envi"])
    keyword = "Test Passed"
    run_commad = run_type + cn["partition"] + "  >>  " + "/" + run_result_file + " " + "2>&1 &"
    cf.run_and_extract_result("n", run_commad, delay_time, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y", cat_file, 10, keyword)
    actual_info = []
    if result:
        if len(result) == 2:
            for i in range(len(result)):
                if "Test Passed" not in result[i]:
                    actual_info.append("dataloader {} ????????????????????????Test Passed".format(type))
        else:
            actual_info.append("dataloader {} ??????????????????????????????Test Passed".format(type))
    else:
        actual_info.append("dataloader {} ????????????, ???????????????Test Passed".format(result))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dataloader {} ????????????".format(type)
        expect_info = ["dataloader {} ????????????".format(type)]
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:   {}\n  ??????: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
        try:
            # original_compress = [run_result_file]
            # dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global function_csv_list
    csv_list = [u"python???_dataloader", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        if len(result) == 2:
            for i in range(len(result)):
                assert "Test Passed" in result[i], "????????????Test Passed!??????,????????????{}".format(result[i])
        else:
            assert False, "??????????????????Test Passed!??????,????????????{}".format(result)

    else:
        assert False, "??????????????????Test Passed!??????,????????????{}".format(result)


@allure.feature("dish_pybind11")
@pytest.mark.pybind11
def test_03_dish_pybind11():
    case_name = "dish_pybind11"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, "")
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    keyword = "mmcv/__init__"
    run_command = "srun -p {} --gres=gpu:1 python -c 'import mmcv; print(mmcv.__file__)'  >> /{}".format(
        cn["partition"], run_result_file)
    cf.run_and_extract_result("n", run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y", cat_file, 20, keyword)
    actual_info = []
    if result:
        if "mmcv/__init__" not in result[0]:
            actual_info.append("import mmcv?????????")
    else:
        actual_info.append("import mmcv?????????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dish_pybind11????????????"
        expect_info = "????????????mmcv??????????????????import"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:   {}\n  ??????: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
        try:
            # original_compress = [run_result_file]
            # dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global function_csv_list
    csv_list = [u"python???_dataloader", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "mmcv/__init__" in result[0], "????????????import mmcv????????????'mmcv/__init__',????????????{}".format(result[0])
    else:
        assert False, "????????????import mmcv????????????'mmcv/__init__',????????????"


@allure.feature("serialization")
def test_04_serialization():
    case_name = "serialization"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/serialization")
    env_result = cf.check_env(cn["source_envi"])
    run_parrots_command = "nohup sh test_serialization.sh  {} /mnt/cache/share/polaris/env/pt1.6s1  >> /{} 2>&1 &".format(
        cn["source_envi"], run_result_file)
    cf.run_and_extract_result("n", run_parrots_command, 320, "")
    cat_file = "cat /{}".format(run_result_file)
    keyword_0 = "Save successfully"
    parrots_0 = cf.run_and_extract_result("y", cat_file, 80, keyword_0)
    actual_info = []
    if parrots_0:
        if len(parrots_0) == 1:
            for i in range(1):
                if "Save successfully" not in parrots_0[i]:
                    actual_info.append("????????????:Save successfully!")
        else:
            actual_info.append("????????????1???Save successfully!")
    else:
        actual_info.append("parrots ??????save???????????????:Save successfully!")
    keyword_1 = "Load and check successfully"
    parrots_1 = cf.run_and_extract_result("y", cat_file, 80, keyword_1)
    if parrots_1:
        if len(parrots_1) == 2:
            for i in range(2):
                if "Load and check successfully" not in parrots_1[i]:
                    actual_info.append("pytorch load???????????????:Load and check successfully!")
        else:
            actual_info.append("??????????????????:Load and check successfully!")
    else:
        actual_info.append("??????????????????:Load and check successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ?????????????????????"
        expect_info = [
            "??????parrots ??????save ???????????????:Save successfully! ?????? pytorch load ????????? ??????:Load and check successfully! ?????? parrots load ?????????????????????:Load and check successfully! "]
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:   {}\n  ??????: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
        try:
            # original_compress = [run_result_file]
            # dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global function_csv_list
    csv_list = [u"???????????????????????????????????????", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if parrots_0:
        if len(parrots_0) == 1:
            for i in range(1):
                assert "Save successfully" in parrots_0[i], "????????????Save successfully?????????{}".format(parrots_0[i])
        else:
            assert False, "????????????1???Save successfully!, ??????{}".format(parrots_0)
    else:
        assert False, "????????????1???Save successfully!, ??????{}".format(parrots_0)
    if parrots_1:
        if len(parrots_1) == 2:
            for i in range(2):
                assert "Load and check successfully" in parrots_1[i], "????????????Load and check successfully, ??????{}".format(
                    parrots_1[i])
        else:
            assert False, "??????????????????:Load and check successfully!, ??????{}".format(parrots_1)
    else:
        assert False, "??????????????????:Load and check successfully!, ??????{}".format(parrots_1)


@allure.feature("host2cuda")
def test_05_host2cuda():
    case_name = "host2cuda"
    cf.create_directory(cn["base_path"] + case_name)
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    cf.conda_deactivate()
    cf.git_clone(cn["base_path"] + case_name, "")
    env_result = cf.check_env(cn["source_envi"])
    cf.run_and_extract_result("y", "python", 20, "")
    cf.run_and_extract_result("y", "import torch", 20, "")
    cf.run_and_extract_result("y", "x = torch.ones(2)", 20, "")
    info = "RuntimeError"
    x_result = cf.run_and_extract_result("y", "x.cuda()", 60, info)
    actual_info = []
    if x_result:
        if "RuntimeError" not in x_result:
            actual_info.append("????????????RuntimeError")
    else:
        actual_info.append("????????????RuntimeError")
    info_ten = "tensor\(\[2. 2.\]\)"
    result_end = cf.run_and_extract_result("y", "x + 1", 60, info_ten)
    if result_end:
        if "tensor([2. 2.])" not in result_end:
            actual_info.append("????????????tensor([2. 2.])")
    else:
        actual_info.append("????????????tensor([2. 2.])")
    cf.cd_command(20, "exit()")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "host2cuda????????????????????????"
        expect_info = ["????????????RuntimeError", "????????????tensor([2. 2.])"]

        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:   {}\n  ??????: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
        try:
            # original_compress = [run_result_file]
            # dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global function_csv_list
    csv_list = [u"host2cuda??????????????????", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if x_result:
        assert "RuntimeError" in x_result, "????????????RuntimeError,????????????{}".format(x_result)
    else:
        assert False, "????????????RuntimeError,????????????{}".format(x_result)
    if result_end:
        assert "tensor([2. 2.])" in result_end, "????????????tensor([2. 2.]),????????????{}".format(result_end)
    else:
        assert False, "????????????tensor([2. 2.]),????????????{}".format(result_end)


@allure.feature("datareader")
def test_06_datareader():
    case_name = "datareader"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    run_result_file1 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "1.txt"
    run_result_file2 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "2.txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/ssd")
    run_command = "PARROTS_BENCHMARK=1 nohup sh runner/ssd/train.sh {} 8 ssd_FSAF_benchmark --DATA_READER CephReader --SEED 1024  >> /{} 2>&1 &".format(
        cn["partition"], run_result_file)
    run_command1 = "PARROTS_BENCHMARK=1 nohup sh runner/ssd/train.sh {} 8 ssd_FSAF_benchmark --DATA_READER MemcachedReader --SEED 1024  >> /{} 2>&1 &".format(
        cn["partition"], run_result_file1)
    run_command2 = "PARROTS_BENCHMARK=1 nohup sh runner/ssd/train.sh {} 8 ssd_FSAF_benchmark --DATA_READER DirectReader --SEED 1024  >> /{} 2>&1 &".format(
        cn["partition"], run_result_file2)
    cf.cd_command(20, run_command)
    cf.cd_command(20, run_command1)
    cf.cd_command(20, run_command2)
    time.sleep(3600)
    run_result = [run_result_file, run_result_file1, run_result_file2]
    kind = ["CephReader", "MemcachedReader", "DirectReader"]
    actual_info = []
    for i in range(len(run_result)):
        log.info("run_result is {}".format(run_result[i]))
        cat_commade = "cat {} | grep 'benchmark_avg_iter_time'".format(run_result[i])
        cat_result = cf.cd_command(10, cat_commade)
        if cat_result:
            if 'benchmark_avg_iter_time' not in cat_result:
                actual_info.append("{}?????????????????????log????????????????????????????????????'benchmark_avg_iter_time'".format(kind[i]))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots datareader????????????"
        expect_info = "CephReader,MemcachedReader,DirectReader?????????????????????log??????????????????benchmark_avg_iter_time??????"

        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????: {}\n ??????: {}\n  ??????: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            original_compress = run_result
            # dlf.compress_file(original_compress)
            local_run_result_list = []
            original_list = []
            for i in range(3):
                local_run_result_file = "/" + cn["local_path"] + cn[
                    "base_path"] + case_name + "/" + case_name + time_stamp + str(i) + ".txt"
                local_run_result_list.append(local_run_result_file)
                original_list.append(run_result[i].replace("mnt", ""))
            later_list = local_run_result_list
            original = original_list
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global function_csv_list
    csv_list = [u"Parrots datareader??????", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        for i in range(len(run_result)):
            cat_commade = "cat {} ".format(run_result[i])
            cat_result = cf.cd_command(10, cat_commade)
            if cat_result:
                assert 'benchmark_avg_iter_time' in cat_result
            else:
                assert False
    else:
        assert False


@allure.feature("timy_ops")
def test_07_timy_ops():
    case_name = "timy_ops"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd  parrots.test/tests/scheduler/tiny_ops/")
    env_result = cf.check_env(cn["source_envi"])
    keyword = "(\d+[.]{1}\d{8,20})"
    run_command = "nohup sh run.sh {} >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 600, "")
    cat_file = "tail -n1 /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 80, keyword)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if cn["ip"] == "10.5.38.31" or cn["ip"] == "10.5.36.31":
            if float(result[0]) > 2.1:
                actual_info.append("??????????????????:{} > 2.1".format(float(result[0])))

        else:
            if float(result[0]) > 1.6:
                actual_info.append("??????????????????:{} > 1.6".format(float(result[0])))

    else:
        actual_info.append("??????????????????")
    flag = "success"
    if actual_info:
        flag = "fail"
        if cn["ip"] == "10.5.38.31" or cn["ip"] == "10.5.36.31":
            expect_info = "??????????????????:{} < 2.1".format(float(result[0]))
        else:
            expect_info = "??????????????????:{} < 1.6".format(float(result[0]))

        summary = "Parrots ???op??????(timy ops)????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ???op??????(timy ops)", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if cn["ip"] == "10.5.38.31" or cn["ip"] == "10.5.36.31":
        if result:
            assert float(2.1) > float(result[0]), "???SH36????????????????????????2.1s',????????????{} > 2.1".format(float(result[0]))
        else:
            assert False, "??????????????????"
    else:
        if result:
            log.info("result[0] type is {}".format(type(result[0])))
            assert float(1.6) > float(result[0]), "???SH1984??????,??????????????????1.6s',????????????{} > 1.6".format(float(result[0]))
        else:
            assert False, "??????????????????"



@allure.feature("exec_mode_sync")
def test_08_exec_mode_sync():
    case_name = "exec_mode_sync"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file_sync is {}".format(run_result_file))
    cf.cd_command(20, "cd  parrots.test")
    cf.submodule("git submodule update --init models/parrots.example")
    env_result = cf.check_env(cn["source_envi"])
    keyword = "(Epoch(.*)1\/1(.*)5000/5005\])"
    log.info("SYNC MODE start:")
    sync_run_command = "nohup sh runner/example/train.sh {} 8 resnet50_sync.short.dummy_data >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  sync_run_command, 3000, "")
    cat_file = "cat /{}".format(run_result_file)
    sync_result = cf.run_and_extract_result("y",  cat_file, 80, keyword)
    log.info("sync_result is {}".format(sync_result))
    actual_info = []
    if sync_result:
        if "Epoch: [1/1][5000/5005]" not in sync_result[0]:
            actual_info.append("SYNC MODE ??????????????????????????????Epoch: [1/1][5000/5005]")
    else:
        actual_info.append("SYNC MODE ??????????????????????????????Epoch: [1/1][5000/5005]")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ???????????????exec_mode???-SYNC MODE ????????????"
        expect_info = ["SYNC MODE ????????? 1 ??? epoch ????????????"]
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ???????????????exec_mode_sync?????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if sync_result:
        assert "Epoch: [1/1][5000/5005]" in sync_result[0], "??????SYNC MODE ????????? 1 ??? epoch ????????????, ??????????????????????????????Epoch: [1/1][5000/5005]"
    else:
        assert False, "??????SYNC MODE ????????? 1 ??? epoch ????????????, ??????????????????????????????Epoch: [1/1][5000/5005]"


@allure.feature("exec_mode_async")
def test_09_exec_mode_async():  
    case_name = "exec_mode_async"
    cf.create_directory(cn["base_path"] + case_name)
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file_async is {}".format(run_result_file))
    cf.cd_command(20, "cd  parrots.test")
    cf.submodule("git submodule update --init models/parrots.example")
    env_result = cf.check_env(cn["source_envi"])
    keyword = "(Epoch(.*)1\/1(.*)5000/5005\])"
    actual_info = []
    log.info("ASYNC MODE start:")
    async_run_command = "nohup sh runner/example/train.sh {} 8 resnet50.short.dummy_data  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("y",  async_run_command, 3000, "")
    cat_file = "cat /{}".format(run_result_file)
    async_result = cf.run_and_extract_result("y",  cat_file, 60, keyword)
    log.info("async_result is {}".format(async_result))
    if async_result:
        if "Epoch: [1/1][5000/5005]" not in async_result[0]:
            actual_info.append("ASYNC MODE ??????????????????????????????Epoch: [1/1][5000/5005]")
    else:
        actual_info.append("ASYNC MODEE ??????????????????????????????Epoch: [1/1][5000/5005]")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ???????????????exec_mode???-ASYNC MODE ????????????"
        expect_info = ["Epoch: [1/1][5000/5005]"]
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ???????????????exec_mode_async?????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if async_result:
        assert "Epoch: [1/1][5000/5005]" in async_result[0], "??????SYNC MODE ????????? 1 ??? epoch ????????????, ??????????????????????????????Epoch: [1/1][5000/5005]"
    else:
        assert False, "??????SYNC MODE ????????? 1 ??? epoch ????????????, ??????????????????????????????Epoch: [1/1][5000/5005]"



@allure.feature("overlap")
def test_10_overlap():  
    case_name = "overlap"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file_no = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "no.txt"
    log.info("run_result_file_no is {}".format(run_result_file_no))
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/parrots.example")
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd tests/scheduler/overlap")
    info = "Benchmark.*(199\/200).*Time.*( .*)"
    nonoverlap_run_command = "nohup sh run.sh {} 16 nonoverlap >> /{} 2>&1 &".format(cn["partition"], run_result_file_no)
    cf.run_and_extract_result("n",  nonoverlap_run_command, 2520, "")
    overlap_run_command = "nohup sh run.sh {} 16 overlap >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n", overlap_run_command, 2820, "")
    # read nooverlap result
    cat_file = "cat /{}".format(run_result_file_no)
    nonover  = cf.run_and_extract_result("y",  cat_file, 80, info)
    actual_info = []
    if nonover:
        nonoverlap_time = nonover[0][1].split(")")[0]
        log.info("nonoverlap_time is {}".format(nonoverlap_time))
        if "199/200" not in nonover[0]:
            actual_info.append("nonoverlap ??????????????????????????????Benchmark: [199/200]?????????????????????")
    else:
        actual_info.append("nonoverlap ??????????????????????????????Benchmark: [199/200]?????????????????????")
        nonoverlap_time = 0
    # read overlap result
    cat_file = "cat /{}".format(run_result_file)
    over = cf.run_and_extract_result("y", cat_file, 80, info)
    if over:
        overlap_time = over[0][1].split(")")[0]
        log.info("overlap_time is {}".format(overlap_time))
        if "199/200" not in over[0]:
            actual_info.append("overlap ??????????????????????????????Benchmark: [199/200]?????????????????????")

    else:
        actual_info.append("overlap ??????????????????????????????Benchmark: [199/200]?????????????????????")
        overlap_time = 0
    if overlap_time:
        if nonoverlap_time:
            if float(overlap_time) > float(nonoverlap_time):
                actual_info.append("overlap ?????????:{}????????? nonoverlap?????????: {}???".format(overlap_time, nonoverlap_time))
        else:
            actual_info.append("??????nonoverlap time")
    else:
        actual_info.append("??????overlap time")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ?????????????????????overlap???????????????"
        expect_info = "overlap???nonoverlap?????????????????????overlap ???????????? nonoverlap ????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            original_compress = [run_result_file_no, run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file_no = "/" + cn["local_path"] + cn[
            "base_path"] + case_name + "/" + case_name + time_stamp + "no.txt"
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file_no, local_run_result_file]
            original = [run_result_file_no.replace("mnt", ""),run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ?????????????????????overlap???", case_name, env_result, flag, [run_result_file, run_result_file_no], gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if nonover:
        assert "199/200" in nonover[0], "??????nonoverlap????????????????????????Benchmark: [199/200], ????????????{}".format(nonover[0])
    else:
        assert False, "??????nonoverlap????????????????????????Benchmark: [199/200], ????????????{}".format(nonover)
    if over:
        assert "199/200" in over[0], "??????overlap????????????????????????Benchmark: [199/200], ????????????{}".format(over[0])
    else:
        assert False, "??????overlap????????????????????????Benchmark: [199/200], ????????????{}".format(over)
    if overlap_time:
        if nonoverlap_time:
            assert float(nonoverlap_time) > float(
                overlap_time), "??????overlap ???????????? nonoverlap ????????????, ??????overlap ?????????{} > nonoverlap ?????????{}".format(
                float(overlap_time), float(nonoverlap_time))
        else:
            assert False
    else:
        assert False



@allure.feature("cuda_random")
def test_11_cuda_random():
    case_name = "cuda_random"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    run_result_file_5 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "5.txt"
    log.info("run_result_file_5 is {}".format(run_result_file_5))
    cf.cd_command(20, "cd parrots.test/tests/performance_optimize/cudarandom/")
    env_result = cf.check_env(cn["source_envi"])
    run_command = "nohup sh cudarandom_test.sh {} 5000 50000  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    keyword = "cost (\d+.\d+) us"
    cf.run_and_extract_result("n",  run_command, 800, "")
    cat_file = "cat /{}".format(run_result_file)
    rusult_now = cf.run_and_extract_result("y",  cat_file, 60, keyword)
    log.info("rusult_now is {}".format(rusult_now))
    cf.conda_deactivate() 
    cf.source_env("source pat0.5.0rc0")
    cd_command_5 = "nohup sh cudarandom_test.sh {} 5000 50000  >> /{} 2>&1 &".format(cn["partition"], run_result_file_5)
    cf.run_and_extract_result("n",  cd_command_5, 800, "")
    cat_file = "cat /{}".format(run_result_file_5)
    rusult_5 = cf.run_and_extract_result("y",  cat_file, 60, keyword)
    log.info("rusult_5 is {}".format(rusult_5))
    actual_info = []
    types = ["rand", "randn", "randperm", "randint", "bernoulli_", "cauchy_", "random_"]
    if rusult_now:
        if rusult_5:
            if len(rusult_now) == 7:
                if len(rusult_5) == 7:
                    for i in range(len(rusult_now)):
                        log.info("rusult_now[{}] is {}".format(i, rusult_now[i]))
                        log.info("rusult_5[{}] is {}".format(i, rusult_5[i]))
                        if float(rusult_now[i]) > float(rusult_5[i]):
                            actual_info.append("parrots{} ??? {} time ?????? parrots0.5 ???{} time".format(cn["source_envi"], types[i], types[i]))
                else:
                    actual_info.append("????????????parrots0.5???7???????????????")
            else:
                actual_info.append("????????????parrots{}???7???????????????".format(cn["source_envi"]))
        else:
            actual_info.append("????????????parrots0.5???7???????????????")
    else:
        actual_info.append("????????????parrots{}???7???????????????".format(cn["source_envi"]))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots CUDA random??????????????????????????????"
        expect_info = "???parrots0.5???????????????:parrots {} ??? ['rand', 'randn', 'randperm', 'randint', 'bernoulli_', 'cauchy_', 'random_']?????? ?????? parrots0.5 ['rand', 'randn', 'randperm', 'randint', 'bernoulli_', 'cauchy_', 'random_']??????".format(cn["source_envi"])
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            original_compress = [run_result_file, run_result_file_5]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file_5 = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "5.txt"
            later_list = [local_run_result_file, local_run_result_file_5]
            original = [run_result_file.replace("mnt", ""), run_result_file_5.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots CUDA random??????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if rusult_now:
        if rusult_5:
            if len(rusult_now) == 7:
                if len(rusult_5) == 7:
                    for i in range(len(rusult_now)):
                        assert float(rusult_now[i]) < float(rusult_5[i]), "??????parrots {} ??? {} time ?????? parrots0.5 ???{} time, ??????parrots{} ??? {} time: {} > parrots0.5 ???{} time: {}".format(cn["source_envi"], types[i], types[i], cn["source_envi"], types[i], float(rusult_now[i]), types[i], float(rusult_5[i]))
                else:
                    assert False, "????????????parrots0.5???7???????????????"
            else:
                assert False, "????????????parrots{}???7???????????????".format(cn["source_envi"])
        else:
            assert False, "????????????parrots0.5???7???????????????"
    else:
        assert False, "????????????parrots{}???7???????????????".format(cn["source_envi"])


@allure.feature("convert_multiple")
def test_12_convert_multiple():  
    case_name = "convert_multiple"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/deploy/convert")
    env_result = cf.check_env(cn["source_envi"])
    info = "All tests successfully\!"
    run_command = "srun -p {} --gres=gpu:1 python test_convert_multiple.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 1000, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if result:
        if "All tests successfully!" not in result:
            actual_info.append("????????????:All tests successfully!")
    else:
        actual_info.append("????????????:All tests successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????Parrots???????????????????????????????????????????????????"
        expect_info = "????????????:All tests successfully!"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots?????????????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "All tests successfully!" in result, "????????????All tests successfully!,????????????{}".format(result)
    else:
        assert False, "????????????All tests successfully!,????????????{}".format(result)

@allure.feature("multiple")
def test_13_multiple():  
    case_name = "multiple"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    cf.cd_command(20, "git submodule update --init tests/deploy/quantization/Famicom")
    time.sleep(10)
    env_result = cf.check_env(cn["source_envi"]) 
    cf.cd_command(20, "cd tests/deploy/quantization/Famicom/")
    cf.cd_command(20, "export PYTHONPATH=$PWD:$PYTHONPATH") 
    cf.cd_command(20, "cd srdemo") 
    info = "Validation\#\#\#\[epoch 24 iter 1500\]: mean psnr: (\d+.\d+)"
    run_command = "srun -p {} --gres=gpu:1 python test_multiple.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 2620, "")
    cat_file = "cat /{}".format(run_result_file)
    valiation_result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if valiation_result:
        if 26 > float(valiation_result[-1]):
            actual_info.append("validation???psnr?????????26")
    else:
        actual_info.append("validation???psnr??????????????????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????Parrots?????????????????????????????????????????????????????????"
        expect_info = "validation???psnr????????????26"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots???????????????????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if valiation_result:
        assert float(valiation_result[-1]) > 26, "??????validation???psnr?????????26,??????validation???psnr?????????26"
    else:
        assert False, "validation???psnr??????????????????"



@pytest.mark.passed
@allure.feature("cancel")
def test_14_cancel():
    case_name = "cancel"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init tests/deploy/quantization/Famicom")
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd tests/deploy/quantization/Famicom/")
    cf.cd_command(20, "export PYTHONPATH=$PWD:$PYTHONPATH") 
    cf.cd_command(20, "cd srdemo") 
    info = "Close Successfully\!"
    run_command = "srun -p {} --gres=gpu:1 python test_cancel.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 1220, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if result:
        if "Close Successfully!" not in result[0]:
            actual_info.append("???????????? 'Close Successfully!'")
    else:
        actual_info.append("???????????? 'Close Successfully!'")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????Parrots???????????????????????????????????????????????????????????????????????????"
        expect_info = "?????????????????????????????????????????????Close Successfully!"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots?????????????????????????????????????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "Close Successfully!" in result[0], "????????????????????????????????????????????????Close Successfully!, ????????????{}".format(result[0])
    else:
        assert False, "????????????????????????????????????????????????Close Successfully!, ????????????{}".format(result)


@allure.feature("visualization")
def test_15_visualization():
    case_name = "visualization"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd  parrots.test/tests/deploy/graph_json")
    env_result = cf.check_env(cn["source_envi"])
    graph_json_command = "srun -p {} --gres=gpu:1 python graph_json.py >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("y",  graph_json_command, 520, "") 
    info = "Upload Successfully"
    python_upload_json_file = "python upload_json.py --user {} --password {} >> /{} 2>&1 &".format(cn["user"], cn["password"], run_result_file)
    cf.run_and_extract_result("y",  python_upload_json_file, 260, "")
    cat_file = "cat /{}".format(run_result_file)
    upload_result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("upload_result is {}".format(upload_result))
    actual_info = []
    if upload_result:
        if "Upload Successfully" not in upload_result[0]:
            actual_info.append("???????????? 'Upload Successfully' ")
    else:
        actual_info.append("???????????? 'Upload Successfully'")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????Parrots?????????????????????????????????????????????"
        expect_info = "Upload Successfully"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots???????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if upload_result:
        assert "Upload Successfully" in upload_result[0], "????????????Upload Successfully,????????????{}".format(upload_result[0])
    else:
        assert False, "????????????Upload Successfully,????????????{}".format(upload_result)


@pytest.mark.passed
@allure.feature("cancel_convert")
def test_16_cancel_convert():
    case_name = "cancel_convert"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/deploy/convert")
    env_result = cf.check_env(cn["source_envi"])
    cancel_info = "Close Successfully\!"
    run_command_cancel = "srun -p {} --gres=gpu:1 python test_cancel.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command_cancel, 860, "")
    cat_file = "cat /{}".format(run_result_file)
    cancel_result = cf.run_and_extract_result("y",  cat_file, 60, cancel_info)
    actual_info = []
    if cancel_result:
        if "Close Successfully!" not in cancel_result:
            actual_info.append("???????????????????????????????????????????????????:Close Successfully!")
    else:
        actual_info.append("???????????????????????????????????????????????????:Close Successfully!")
    convert_info = "Test Successfully\!"
    run_command_convert = "srun -p {} --gres=gpu:1 python test_convert.py  >> /{}".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("y",  run_command_convert, 860, "")
    cat_file = "cat /{}".format(run_result_file)
    convert_result = cf.run_and_extract_result("y",  cat_file, 60, convert_info)
    if convert_result:
        if "Test Successfully!" not in convert_result:
            actual_info.append("???????????????????????????????????????:Test Successfully!")
    else:
        actual_info.append("???????????????????????????????????????:Test Successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????Parrots?????????????????????????????????????????????????????????????????????"
        expect_info = ["???????????????????????????????????????????????????????????????:Close Successfully!", "????????????????????????????????????????????????:Test Successfully!"]
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots???????????????????????????????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if cancel_result:
        assert "Close Successfully!" in cancel_result, "????????????Close Successfully!,????????????{}".format(cancel_result)
    else:
        assert False, "????????????Close Successfully!,????????????{}".format(cancel_result)
    if convert_result:
        assert "Test Successfully!" in convert_result, "????????????Test Successfully!,????????????{}".format(convert_result)
    else:
        assert False, "????????????Test Successfully!,????????????{}".format(convert_result)


@allure.feature("torchvision")
def test_17_torchvision():
    case_name = "torchvision"
    cf.create_directory(cn["base_path"] + case_name)
    git_clone_command = "git clone git@gitlab.bj.sensetime.com:luopeichao/parrots.torchvision.git -b v0.4.0-parrots"
    cf.git_clone(cn["base_path"] + case_name, git_clone_command)
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.torchvision")
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "pip install --user mock")
    info = "test_save_image_single_pixel(.*)"
    run_command = "srun -p {} --gres=gpu:1 python -m pytest test_vision/ -vx  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 1220, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("torchvision result is {}".format(result))
    actual_info = []
    if result:
        if "PASSED   [100%]" not in result[0]:
            actual_info.append("pytest??????")
    else:
        actual_info.append("pytest??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ??????????????????/torchvision??????????????????"
        expect_info = "pytest???????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ??????????????????/torchvision????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "PASSED   [100%]" in result[0], "????????????pytest??????????????????PASSED   [100%],????????????{}".format(result[0])
    else:
        assert False, "????????????pytest??????????????????PASSED   [100%],????????????{}".format(result)



@allure.feature("debug")
def test_18_debug():  
    case_name = "debug"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, "")
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    run_result_file1 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "1.txt"
    env_result = cf.check_env(cn["source_envi"])
    info_nodebug = "MCA parameter"
    python_nodebug_command = 'python -c "import torch" >> {} 2>&1 &'.format(run_result_file)
    cf.run_and_extract_result("n",  python_nodebug_command, 800, "")
    cat_file = "cat /{}".format(run_result_file)
    nodebug_result = cf.run_and_extract_result("y",  cat_file, 10, info_nodebug)
    actual_info = []
    try:
        if nodebug_result:
            if "MCA parameter" not in nodebug_result[0]:
                actual_info.append("????????????debug????????????")
        else:
            actual_info.append("????????????debug????????????")
    except Exception as e:
        log.info(e)
    debug_info = "AssertionError"
    python_debug_command = 'PARROTS_USER_UPLOAD_DEBUG=1 python -c "import torch" >> {} 2>&1 &'.format(run_result_file1)
    cf.run_and_extract_result("n",  python_debug_command, 800, "")
    cat_file = "cat /{}".format(run_result_file1)
    debug_result = cf.run_and_extract_result("y",  cat_file, 10, debug_info)
    if debug_result:
        if "AssertionError" not in debug_result[0]:
            actual_info.append("??????debug??????????????????")
    else:
        actual_info.append("??????debug??????????????????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "parrots0.8.0 ????????????debug??????????????????"
        expect_info = "????????????debug?????????????????????????????????parrots????????????????????????,??????debug???????????????????????????????????????parrots??????????????????AssertionErro"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            original_compress = [run_result_file, run_result_file1]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file1 = "/" + cn["local_path"] + cn[
            "base_path"] + case_name + "/" + case_name + time_stamp + "1.txt"
            later_list = [local_run_result_file, local_run_result_file1]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"????????????debug????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if nodebug_result:
        assert "MCA parameter" in nodebug_result[0], "??????debug????????????????????????parrots??????????????????, ????????????????????????????????????MCA parameter"
    else:
        assert False, "??????debug????????????????????????parrots??????????????????, ????????????????????????????????????MCA parameter"
    if debug_result:
        assert "AssertionError" in debug_result[0], "??????debug???????????????????????????parrots????????????AssertionError, ??????????????????AssertionError"
    else:
        assert False, "??????debug???????????????????????????parrots????????????AssertionError, ??????????????????AssertionError"


@allure.feature("nodump")
def test_19_nodump():
    case_name = "nodump"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/dump/")
    env_result = cf.check_env(cn["source_envi"])
    no_dump_info = "Segmentation fault"
    run_command_no_dump = "nohup sh no_dump.sh {}  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command_no_dump, 860, "")
    cat_file = "cat /{}".format(run_result_file)
    no_dump_sesult = cf.run_and_extract_result("y",  cat_file, 60, no_dump_info)
    actual_info = []
    if no_dump_sesult:
        if "Segmentation fault" not in no_dump_sesult:
            actual_info.append("??????no_dump.sh???????????????'Segmentation fault'??????")
    else:
        actual_info.append("??????no_dump.sh???????????????'Segmentation fault'??????")
    file_list = cf.cd_command(20, "ll")
    no_core = re.compile("core.\d+")
    no_core_result = re.findall(no_core, file_list)
    if no_core_result:
        actual_info.append("??????no_dump.sh????????????????????????core.<pid>" )
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots noDump????????????"
        expect_info = "??????no_dump.sh?????????????????????????????????????????????????????????segmentation fault?????????????????????????????????core.<pid>"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots noDump??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info
       


@allure.feature("dump")
def test_20_dump():
    case_name = "dump"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/dump/")
    env_result = cf.check_env(cn["source_envi"])
    actual_info = []
    dump_info = "Segmentation fault"
    run_command_dump = "nohup sh dump.sh {}  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command_dump, 1060, "")
    cat_file = "cat /{}".format(run_result_file)
    dump_result = cf.run_and_extract_result("y",  cat_file, 60, dump_info)
    if dump_result:
        if "Segmentation fault" not in dump_result[0]:
            actual_info.append("??????dump.sh????????? ??????'Segmentation fault'??????")
    else:
        actual_info.append("??????dump.sh????????? ??????'Segmentation fault'??????")
    core = "ll >> /{}".format(run_result_file)
    cf.run_and_extract_result("n",  core, 1, "")
    cat_file = "cat /{}".format(run_result_file)
    core_result = cf.run_and_extract_result("y",  cat_file, 60, "core.\d+")
    if core_result:
        if "core" not in core_result[0]:
            actual_info.append("??????dump.sh?????????????????????core.<pid>")
    else:
        actual_info.append("??????dump.sh?????????????????????core.<pid>")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots Dump????????????"
        expect_info = "??????dump.sh?????????????????????core.<pid>?????????pid?????????????????????????????????????????????????????????????????????????????????segmentation fault????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots Dump??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
       assert False, actual_info 

@allure.feature("log_exception")
def test_21_log_exception():
    case_name = "log_exception"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/logs/")
    env_result = cf.check_env(cn["source_envi"])
    info = "invalid broadcast bcast"
    run_command = "srun -p {} --gres=gpu:1 python test_log_exception.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 1200, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if result:
        if "invalid broadcast bcast" not in result[0]:
            actual_info.append("?????????????????? 'invalid broadcast bcast' ??????")
    else:
        actual_info.append("?????????????????? 'invalid broadcast bcast' ??????")
    find_file = cf.run_and_extract_result("y",  "ll", 10, "log_exception.txt")
    if find_file:
        file_info = cf.run_and_extract_result("y",  "cat log_exception.txt", 20, info)
        if file_info:
            if "invalid broadcast bcast" not in file_info[0]:
                actual_info.append("??????log_exception.txt ?????? 'invalid broadcast bcast' ??????")
        else:
            actual_info.append(" ?????? log_exception.txt ?????? 'invalid broadcast bcast' ??????")
    else:
        actual_info.append("????????????log_exception.txt??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ????????????????????????????????????"
        expect_info = "????????????invalid broadcast bcast???????????????????????????????????????????????????log_exception.txt???????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ??????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("log_level")
def test_22_log_level():  
    case_name = "log_level"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    cf.cd_command(20, "cd parrots.test/tests/log_utils/logs/")
    env_result = cf.check_env(cn["source_envi"])
    keyword = "\(P(.*)T(.*)\) (.*)"
    run_command = "srun -p {} --gres=gpu:1 python test_log_level.py >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 900, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 10, keyword)
    result_list = []
    for i in range(len(result)):
        list_info = str(result[i]).split(",")[2].split(")")[0]
        result_list.append(list_info)
        log.info("result_list is {}".format(result_list))
    expect_result = ["[I] info 1", "[W] warn 1", "[D] debug 2", "[I] info 2", "[W] warn 2", "[I] info 3", "[W] warn 3",
                     "[I] info 7", "[W] warn 7", "[D] debug 8", "[I] info 8", "[W] warn 8", "[I] info 9", "[W] warn 9"]
    actual_info = []
    for i in range(len(result_list)):
        log.info("result_list[{}] is {}".format(i, result_list[i]))
        log.info("expect_result[{}] is {}".format(i, expect_result[i]))
        if expect_result[i] not in result_list[i]:
            actual_info.append("no {}".format(expect_result[i]))
    find_file = cf.run_and_extract_result("y",  "ll", 10, "log_level.txt")
    if find_file:
        file_result = cf.cd_command(20, "cat log_level.txt")
        p = re.compile(r"{}".format(keyword))
        result = re.findall(p, file_result)
        log.info("file_result is {}".format(result))
        file_result_list = []
        for i in range(len(result)):
            list_info = str(result[i]).split(",")[2].split(")")[0]
            file_result_list.append(list_info)
        file_expect_result = ["[I] info 4", "[W] warn 4", "[D] debug 5", "[I] info 5", "[W] warn 5", "[I] info 6",
                              "[W] warn 6", "[I] info 7", "[W] warn 7", "[D] debug 8", "[I] info 8", "[W] warn 8",
                              "[I] info 9", "[W] warn 9"]
        for i in range(len(file_result_list)):
            log.info("file_result_list[{}] is {}".format(i, file_result_list[i]))
            log.info("file_expect_result[{}] is {}".format(i, file_expect_result[i]))
            if file_expect_result[i] not in file_result_list[i]:
                actual_info.append("file ?????? {}".format(file_expect_result[i]))
    else:
        actual_info.append("????????????log_level.txt??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ??????????????????????????????"
        expect_info = "????????????[I] info 1???[W] warn 1....????????????????????????????????????????????????????????????log_level.txt?????????????????????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("log_limit")
def test_23_log_limit():  
    case_name = "log_limit"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    cf.cd_command(20, "cd parrots.test/tests/log_utils/logs/")
    env_result = cf.check_env(cn["source_envi"])
    info = r"(\(P(.*).T(.*)\) (.*))"
    run_command = "srun -p {} --gres=gpu:1  python test_log_limit.py >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("y",  run_command, 1000, "")
    actual_info = []
    find_file = cf.run_and_extract_result("y",  "ll", 10, "log_limit.txt")
    if find_file:
        result = cf.cd_command(20, "cat log_limit.txt")
        if result:
            if "message is here!" not in result:
                actual_info.append("log_limit.txt ?????? message")
        else:
            actual_info.append("log_limit.txt ?????? message")
    else:
        actual_info.append("????????????log_limit.txt??????")
    find_file1 = cf.run_and_extract_result("y",  "ll", 10, "log_limit.1.txt")
    if find_file1:
        result1 = cf.cd_command(20, "cat log_limit.1.txt")
        log.info("result1 is {}".format(result1))
        if result1:
            if "message is here!" not in result1:
                actual_info.append("log_limit.1.txt ?????? message")
        else:
            actual_info.append("log_limit.1.txt ?????? message")
    else:
        actual_info.append("????????????log_limit.1.txt??????")
    find_file2 = cf.run_and_extract_result("y",  "ll", 10, "log_limit.2.txt")
    if find_file2:
        result2 = cf.cd_command(20, "cat log_limit.2.txt")
        log.info("file_result is {}".format(result2))
        if result2:
            if "message is here!" not in result2:
                actual_info.append("log_limit.2.txt ?????? message")
        else:
            actual_info.append("log_limit.2.txt ?????? message")
    else:
        actual_info.append("????????????log_limit.2.txt??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        log.info("result is {}".format(result))
        summary = "Parrots ???????????????????????????????????????"
        expect_info = "????????????????????? log_limit.txt??? log_limit.1.txt??? log_limit.2.txt???????????????????????????message is here!"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            limit_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + "parrots.test/tests/log_utils/logs/" + "log_limit.txt"
            limit_file_1 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + "parrots.test/tests/log_utils/logs/" + "log_limit.1.txt"
            limit_file_2 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + "parrots.test/tests/log_utils/logs/" + "log_limit.2.txt"
            original_compress = [limit_file, limit_file_1, limit_file_2]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file_1 = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "1.txt"
            local_run_result_file_2 = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "2.txt"
            later_list = [local_run_result_file, local_run_result_file_1, local_run_result_file_2]
            original = [limit_file.replace("mnt", ""), limit_file_1.replace("mnt", ""), limit_file_2.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ?????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("log_model")
def test_24_log_model():  
    case_name = "log_model"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/logs/")
    env_result = cf.check_env(cn["source_envi"])
    info = "gpu id: 3"
    run_command = "mpirun -np 4 python test_log_model.py  >> /{} 2>&1 &".format(run_result_file)
    cf.run_and_extract_result("n",  run_command, 1200, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "gpu id: 3" not in result[0]:
            actual_info.append("??????????????????gpu id: 3????????????")
    else:
        actual_info.append("??????????????????gpu id: 3????????????")
    log.info("find result_file is:")
    time.sleep(2)
    # file = cf.cd_command(20, "ll")
    keyword = "log_model.*txt"
    # cat_file = "cat /{}".format(run_result_file)
    log_file_find = cf.run_and_extract_result("y",  "ll", 10, keyword)
    if len(log_file_find) == 4:
        log.info("log_file_find is {}".format(log_file_find))
        file_info = ["gpu id: 0", "gpu id: 1", "gpu id: 2", "gpu id: 3"]
        log.info("cat result_file is:")
        for i in range(4):
            log.info("cat file is {}".format(log_file_find[i]))
            result_file_end = cf.cd_command(20, 'cat {}'.format(log_file_find[i]))
            time.sleep(1)
            log.info("result_file_end is {}".format(result_file_end))
            if file_info[i] not in result_file_end:
                actual_info.append("{} ???????????????,???????????????:{}".format(log_file_find[i], result_file_end))
    else:
        actual_info.append("??????{}???log_model??????".format(len(log_file_find)))
        log.info("log_file_find is {}".format(log_file_find))
        file_info = ["gpu id: 0", "gpu id: 1", "gpu id: 2", "gpu id: 3"]
        log.info("cat result_file is:")
        for i in range(len(log_file_find)):
            log.info("cat file is {}".format(log_file_find[i]))
            result_file_end = cf.cd_command(20, 'cat {}'.format(log_file_find[i]))
            time.sleep(1)
            log.info("result_file_end is {}".format(result_file_end))
            if file_info[i] not in result_file_end:
                actual_info.append("{} ???????????????, ???????????????:{}".format(log_file_find[i], result_file_end))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ?????????????????????????????????????????????"
        expect_info = "????????????model name??????????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ???????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@pytest.mark.pyc
@allure.feature("pyc")
def test_25_pyc():
    case_name = "pyc"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd  parrots.test/tests/environment/pyc_test/")
    env_result = cf.check_env(cn["source_envi"])
    end_info = "Total pycfile 0"
    sh_pyc_command = "nohup sh pyc_test.sh parrots-{}-py36-none-linux_x86_64  >> /{} 2>&1 &".format(env_result, run_result_file)
    cf.run_and_extract_result("n",  sh_pyc_command, 1100, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, end_info)
    end_info_2 = "dist-info/RECORD"
    result_2 = cf.run_and_extract_result("y", cat_file, 60, end_info_2)
    actual_info = []
    if result:
        if "Total pycfile 0" not in result[0]:
            actual_info.append("????????????????????????Total pycfile 0")
    else:
        actual_info.append("????????????????????????Total pycfile 0")
    if result_2:
        if "dist-info/RECORD" not in result_2[0]:
            actual_info.append("???????????????????????????dist-info/RECORD")
    else:
        actual_info.append("???????????????????????????dist-info/RECORD")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ????????????pyc??????????????????"
        expect_info = "?????????????????????dist-info/RECORD,??????????????????Total pycfile 0"        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ????????????pyc????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("dataloader_prefetch")
def test_26_dataloader_prefetch():
    case_name = "dataloader_prefetch"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/dataloader")
    env_result = cf.check_env(cn["source_envi"])
    log.info("run start")
    keyword = "Test for dataloader prefetch_remain passed"
    run_command = "python dataloader_test_prefetch.py  >> /{} 2>&1 &".format(run_result_file)
    cf.run_and_extract_result("n",  run_command, 300, "")
    cat_file = "cat {}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 10, keyword)
    actual_info = []
    if result:
        if "Test for dataloader prefetch_remain passed" not in result[0]:
            actual_info.append("dataloader prefetch 2 at origin????????????, ?????????Test for dataloader prefetch_remain passed".format(result))
    else:
        actual_info.append("dataloader prefetch 2 at origin????????????, ?????????Test for dataloader prefetch_remain passed".format(result))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dataloader_prefetch ????????????"
        expect_info = "??????Test for dataloader prefetch_remain passed??????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"dataloader_prefetch ??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info



@allure.feature("extension")
def test_27_extension():
    case_name = "extension"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/ext_based_pytorch")
    before_gen_result_info = ["gelu_ext.yaml", "gelu_src", "gen.py", "test_gelu.py"]
    before_gen_file = cf.cd_command(20, "ll")
    log.info("before_gen_file is {}".format(before_gen_file))
    # for i in range(4):
    #     assert before_gen_result_info[i] in before_gen_file
    gelu_src_result = cf.cd_command(20, "cd gelu_src")
    before_gen_gelu_src = ["gelu_kernel.cu", "gelu_pytorch.cpp", "gelu_pytorch.hpp"]
    gelu_src_file_result = cf.cd_command(20, "ll")
    log.info("gelu_src_result is {}".format(gelu_src_result))
    # for i in range(3):
    #     assert before_gen_gelu_src[i] in gelu_src_file_result
    cf.cd_command(20, "cd ../")    # ????????ext_based_pytorch
    env_result = cf.check_env(cn["source_envi"])
    cf.run_and_extract_result("y",  "python gen.py > python_gen.log 2>&1 &", 700, "")
    after_gun_file = ["gelu_ext.yaml", "gelu_src", "gen.py", "setup.py", "test_gelu.py"]
    after_gun_file_result = cf.cd_command(20, "ll")
    log.info("after_gun_file_result is {}".format(after_gun_file_result))
    # for j in range(5):
    #     assert after_gun_file[j] in after_gun_file_result
    cf.cd_command(20, "cd gelu_src")
    after_gen_gelu_src = ["gelu_kernel.cu", "gelu_parrots.cpp", "gelu_parrots.py", "gelu_pytorch.cpp", "gelu_pytorch.hpp"]
    after_gelu_src_file_result = cf.cd_command(20, "ll")
    log.info("after_gelu_src_file_result is {}".format(after_gelu_src_file_result))
    # for k in range(5):
    #     assert after_gen_gelu_src[k] in after_gelu_src_file_result
    cf.cd_command(20, "cd ../")  
    clean_result = cf.run_and_extract_result("y",  "python setup.py clean > python_setup.log 2>&1 &", 700, "")
    log.info("clean result is {}".format(clean_result))
    build_command = "srun -p {} --gres gpu:1 -n 1 python setup.py build > python_setup1.log 2>&1 &".format(cn["partition"])
    build_result = cf.run_and_extract_result("y",  build_command, 700, "")
    log.info("build_result is {}".format(build_result))
    info = "(test_gelu.*PASSED)"
    run_commad = "srun -p {} --gres gpu:1 -n 1 pytest -vxs test_gelu.py  >> /{}".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_commad, 700, "")
    cat_file = "cat /{}".format(run_result_file)
    srun_result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("srun_result is {}".format(srun_result))
    actual_info = []
    if srun_result:
        if "test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED" not in srun_result:
            actual_info.append("????????????test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED??????")
        if "test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED" not in srun_result:
            actual_info.append("????????????test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED??????")
    else:
        actual_info.append("????????????test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED, test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots extension????????????"
        expect_info = "??????test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED, test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED??????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots extension??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("error_log")
def test_28_error_log():
    case_name = "error_log"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/logs/")
    env_result = cf.check_env(cn["source_envi"])
    run_command = "python test_log_error.py  >> /{} 2>&1 &".format(run_result_file)
    keyword = "test successfully"
    cf.run_and_extract_result("n",  run_command, 300, "")
    cat_file = "cat /{}".format(run_result_file)
    rusult_now = cf.run_and_extract_result("y",  cat_file, 60, keyword)
    log.info("rusult_now is {}".format(rusult_now))
    actual_info = []
    if rusult_now:
        if "test successfully" not in rusult_now[0]:
            actual_info.append("????????????test successfully!?????????????????????????????????")
    else:
        actual_info.append("????????????test successfully!?????????????????????????????????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots????????????????????????????????????"
        expect_info = "Parrots????????????????????????????????????, ??????:test successfully"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots??????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info

@allure.feature("config_env")
def test_29_config_env():
    case_name = "config_env"
    cf.cd_command(20, "cd")
    cf.cd_command(20, "ls -a")
    cf.cd_command(20, "rm -rf .parrots/")
    check = cf.cd_command(20, "ls -a")
    log.info("check .parrots is {}".format(check))
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/configs")
    env_result = cf.check_env(cn["source_envi"])
    run_command = "python test_config_env.py  >> /{} 2>&1 &".format(run_result_file)
    keyword = "successfully"
    cf.run_and_extract_result("n",  run_command, 300, "")
    cat_file = "cat /{}".format(run_result_file)
    rusult_now = cf.run_and_extract_result("y",  cat_file, 60, keyword)
    log.info("rusult_now is {}".format(rusult_now))
    actual_info = []
    if rusult_now:
        if "successfully" not in rusult_now[0]:
            actual_info.append("?????????????????? test_config_env.py ??????????????????, ???????????????????????????")
    else:
        actual_info.append("?????????????????? test_config_env.py ??????????????????, ???????????????????????????")
    cf.cd_command(20, "cd")
    cf.cd_command(20, "cat ~/.parrots/config.yaml")
    off_on = "sed -i" + " " + '"{}'.format("s/PARROTS_OPBENCHMARK: ") + "'{}'".format("OFF") + "/PARROTS_OPBENCHMARK: " + "'{}'".format("ON") + '{}"'.format("/") + " " + "~/.parrots/config.yaml"
    log.info("off_on is {}".format(off_on))
    cf.cd_command(20, off_on)
    cf.cd_command(20, "cat ~/.parrots/config.yaml")
    cf.cd_command(20, "python")
    cf.cd_command(20, "import torch")
    cf.cd_command(20, "import os")
    result = cf.cd_command(20, "os.getenv('PARROTS_OPBENCHMARK') == 'ON'")
    cf.cd_command(20, "exit()")
    if result:
        if "True" not in result:
            actual_info.append("??????python???????????????????????????????????????True")
    else:
        actual_info.append("??????python???????????????????????????????????????True")
    on_off = "sed -i" + " " + '"{}'.format("s/PARROTS_OPBENCHMARK: ") + "'{}'".format(
        "ON") + "/PARROTS_OPBENCHMARK: " + "'{}'".format("OFF") + '{}"'.format("/") + " " + "~/.parrots/config.yaml"
    log.info("off_on is {}".format(off_on))
    cf.cd_command(20, on_off)
    cf.cd_command(20, "cat ~/.parrots/config.yaml")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots????????????????????????????????????????????????"
        expect_info = "?????????????????? test_config_env.py ????????????????????????, ??????python????????????????????????????????????True"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots??????????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info

@allure.feature("benchmark")
def test_30_benchmark():
    case_name = "benchmark"
    cf.create_directory(cn["base_path"] + case_name)
    git_clone_command = "git clone git@gitlab.bj.sensetime.com:lizhouyang/tiny_ops.git"
    cf.git_clone(cn["base_path"] + case_name, git_clone_command)
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd tiny_ops")
    env_result = cf.check_env(cn["source_envi"])
    run_command = "srun -p {} --gres=gpu:1 python jit_example/delta2bbox.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 300, "")
    cat_file = "cat /{}".format(run_result_file)
    keyword = "time costing origin"
    keyword_0 = "time costing coderized"
    rusult_now = cf.run_and_extract_result("y",  cat_file, 60, keyword)
    rusult_now_1 = cf.run_and_extract_result("y", cat_file, 60, keyword_0)
    log.info("rusult_now is {}".format(rusult_now))
    actual_info = []
    if rusult_now:
        if "time costing origin" not in rusult_now[0]:
            actual_info.append("????????????????????????time costing origin??????")
    else:
        actual_info.append("????????????????????????time costing origin??????")
    if rusult_now_1:
        if "time costing coderized" not in rusult_now_1[0]:
            actual_info.append("????????????????????????time costing coderized??????")
    else:
        actual_info.append("????????????????????????time costing coderized??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "????????????benchmark??????????????????"
        expect_info = "??????????????????????????????time costing origin: XXXX,time costing coderized: XXXX"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"????????????benchmark????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info



@allure.feature("cuda10_environment")
def test_31_cuda10_environment():
    case_name = "cuda10_environment"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/mmdet")
    env_result = cf.check_env(cn["source_envi"])
    env_result = env_result + "_cuda10"
    log.info("env_result is {}".format(env_result))
    log.info("run start")
    run_command = "nohup sh runner/mmdet/train.sh {} 8 mask_rcnn_x101_32x4d_fpn_1x_coco  --seed 1024 --max-step 1 > /{} 2>&1 &".format(
        cn["partition"],  run_result_file)
    cf.run_and_extract_result("n", run_command, 6500, "")
    cat_file = "cat {}".format(run_result_file)
    keyword = "benchmark_mem_cached"
    result = cf.run_and_extract_result("y", cat_file, 20, keyword)
    actual_info = []
    if result:
        if "benchmark_mem_cached" not in result[0]:
            actual_info.append("????????????????????????????????????:benchmark_mem_cached")
    else:
        actual_info.append("????????????????????????????????????:benchmark_mem_cached")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "cuda10????????????????????????"
        expect_info = "cuda10????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"cuda10??????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("no_gpu_parrots")
def test_32_no_gpu_parrots():
    case_name = "no_gpu_parrots"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, "")
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    result_gpu = cf.cd_command(20, "swatch -n SH-IDC1-10-198-4-31 nv")
    log.info("result is {}".format(result_gpu))
    env_result = cf.check_env(cn["source_envi"])
    run_command = "python -c 'import parrots'  > /{} 2>&1 &".format(run_result_file)
    cf.run_and_extract_result("n", run_command, 500, "")
    cat_file = "cat {}".format(run_result_file)
    keyword = "successfully"
    result = cf.run_and_extract_result("y", cat_file, 20, keyword)
    actual_info = []
    if result:
        if "successfully" not in result[0]:
            actual_info.append("???????????????GPU??????parrots????????????:successfully")
    else:
        actual_info.append("???????????????GPU??????parrots????????????:successfully")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "???GPU??????parrots????????????"
        expect_info = "???GPU??????parrots????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"???GPU??????parrots??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info





@allure.feature("parrots_stack")
def test_33_parrots_stack():
    case_name = "parrots_stack"
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test/tests/performance_optimize/cudastack/")
    info = "Test successfully"
    run_command = "nohup sh cudastack_test.sh  {}  pt1.3v1  {}  >> /{} 2>&1 &".format(cn["source_envi"], cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    run_result = cf.run_and_extract_result("y",  cat_file, 30, info)
    log.info("run_result is {}".format(run_result))
    actual_info = []
    if run_result:
        if "Test successfully" not in run_result[0]:
            actual_info.append("????????????:Test successfully!")
    else:
        actual_info.append("????????????:Test successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "parrots stack ??????????????????"
        expect_info = "parrots stack ??????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"parrots stack ????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info



@pytest.mark.import_torchvision
@allure.feature("import_torchvision")
def test_34_import_torchvision():
    case_name = "import_torchvision"
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test/tests/python_layer/torchvision")
    info = "Import Torchvision Successfully"
    run_command = "python test_torchvision.py  >> /{} 2>&1 &".format(run_result_file)
    cf.run_and_extract_result("n",  run_command, 300, "")
    cat_file = "cat /{}".format(run_result_file)
    run_result = cf.run_and_extract_result("y",  cat_file, 30, info)
    log.info("run_result is {}".format(run_result))
    actual_info = []
    if run_result:
        if "Import Torchvision Successfully" not in run_result[0]:
            actual_info.append("????????????:Import Torchvision Successfully!")
    else:
        actual_info.append("????????????:Import Torchvision Successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots??????torchvision????????????"
        expect_info = "Parrots??????torchvision????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots??????torchvision??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("log_one")
def test_35_log_one():
    case_name = "log_one"
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "export PARROTS_DEFAULT_LOGGER=FALSE")
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/mmdet")
    info = "\[100\/7330\]"
    run_command = "nohup sh runner/mmdet/train.sh {} 8 mask_rcnn_r50_fpn_1x_coco --max-step 1  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 1500, "")
    cat_file = "cat /{}".format(run_result_file)
    run_result = cf.run_and_extract_result("y",  cat_file, 30, info)
    log.info("run_result is {}".format(run_result))
    actual_info = []
    if run_result:
        if len(run_result) > 1:
            actual_info.append("??????????????????[100/7330]")
        else:
            if "[100/7330]" not in run_result[0]:
                actual_info.append("????????????:[100/7330]")
    else:
        actual_info.append("????????????:[100/7330]")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????mmdet?????????log????????????????????????"
        expect_info = "??????mmdet?????????log????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"??????mmdet?????????log??????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, actual_info


@allure.feature("timeline_fn_op")
def test_36_timeline_fn_op():
    case_name = "timeline_fn_op"
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    export_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("export_result_file is {}".format(export_result_file))
    unset_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "unset.txt"
    log.info("unset_result_file is {}".format(unset_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test")
    cf.cd_command(10, "export PARROTS_PROFILE_FUNCTION=OFF")
    cf.cd_command(10, "export PARROTS_PROFILE_ATTRS=OFF")
    info = "timeline.json"
    run_command = "srun -p {} --gres=gpu:1 python tests/log_utils/logs/test_timeline_log.py --export=True  >> /{} 2>&1 &".format(cn["partition"], export_result_file)
    cf.run_and_extract_result("n",  run_command, 300, "")
    cf.cd_command(20, "profile2timeline --profile_path profile.txt --timeline_path timeline.json.gz")
    cf.cd_command(10, "ll")
    cf.cd_command(20, "gunzip timeline.json.gz")
    cf.cd_command(10, "ll")
    cf.cd_command(10, "ll >> /{}".format(export_result_file))
    cat_file = "cat /{}".format(export_result_file)
    run_result = cf.run_and_extract_result("y", cat_file, 30, info)
    log.info("run_result is {}".format(run_result))
    actual_info = []
    if run_result:
        if "timeline.json" not in run_result[0]:
            actual_info.append("????????????timeline.json??????")
    else:
        actual_info.append("????????????timeline.json??????")
    ConvForward = "grep -ws " + "'{}' timeline.json -A 3  >> /{}".format('"name": "ConvForward",', export_result_file)
    log.info("ConvForward is {}".format(ConvForward))
    cf.cd_command(60, ConvForward)
    ConvForward_info = "ConvForward"
    ConvForward_result = cf.run_and_extract_result("y", cat_file, 20, ConvForward_info)
    log.info("ConvForward_result is {}".format(ConvForward_result))
    if ConvForward_result:
        if len(ConvForward_result) != 6:
            actual_info.append("timeline.json????????????6???ConvForward??????")
    else:
        actual_info.append("timeline.json????????????6???ConvForward??????")
    # unset
    cf.cd_command(10, "unset PARROTS_PROFILE_FUNCTION")
    cf.cd_command(10, "unset PARROTS_PROFILE_ATTRS")
    unset_run_command = "srun -p {} --gres=gpu:1 python tests/log_utils/logs/test_timeline_log.py  >> /{} 2>&1 &".format(cn["partition"], unset_result_file)
    cf.run_and_extract_result("n", unset_run_command, 300, "")
    cf.cd_command(20, "profile2timeline --profile_path profile.txt --timeline_path time.json.gz")
    cf.cd_command(10, "ll")
    cf.cd_command(20, "gunzip time.json.gz")
    cf.cd_command(10, "ll")
    cf.cd_command(10, "ll >> /{}".format(unset_result_file))
    unset_cat_file = "cat /{}".format(unset_result_file)
    unset_info = "time.json"
    unset_run_result = cf.run_and_extract_result("y", unset_cat_file, 30, unset_info)
    log.info("run_result is {}".format(run_result))
    if unset_run_result:
        if "time.json" not in unset_run_result[0]:
            actual_info.append("????????????time.json??????")
    else:
        actual_info.append("????????????time.json??????")
    unset_ConvForward = "grep -ws " + "'{}' time.json -A 3  >> /{}".format('"name": "ConvForward",', unset_result_file)
    log.info("unset_ConvForward is {}".format(unset_ConvForward))
    cf.cd_command(60, unset_ConvForward)
    unset_ConvForward_info = "ConvForward"
    unset_ConvForward_result = cf.run_and_extract_result("y", unset_cat_file, 30, unset_ConvForward_info)
    log.info("unset_ConvForward_result is {}".format(unset_ConvForward_result))
    if unset_ConvForward_result:
        if len(unset_ConvForward_result) != 6:
            actual_info.append("time.json????????????6???ConvForward??????")
    else:
        actual_info.append("time.json????????????6???ConvForward??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots??????timeline??????fn???op??????????????????"
        expect_info = "Parrots??????timeline??????fn???op??????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            original_compress = [export_result_file, unset_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file_unset = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "unset.txt"
            later_list = [local_run_result_file, local_run_result_file_unset]
            original = [export_result_file.replace("mnt", ""), unset_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots??????timeline??????fn???op????????????", case_name, env_result, flag, [export_result_file, unset_result_file], gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        assert "timeline.json" in run_result[0], "????????????timeline.json???????????????{}".format(run_result)
    else:
        assert False, "????????????timeline.json???????????????{}".format(run_result)
    if unset_run_result:
        assert "time.json" in unset_run_result[0], "????????????time.json???????????????{}".format(unset_run_result)
    else:
        assert False, "????????????time.json???????????????{}".format(unset_run_result)
    if ConvForward_result:
        assert len(ConvForward_result) == 6, "??????timeline.json??????6???ConvForward???????????????{}".format(ConvForward_result)
    else:
        assert False, "??????timeline.json??????6???ConvForward???????????????{}".format(ConvForward_result)
    if unset_ConvForward_result:
        assert len(unset_ConvForward_result) == 6, "??????time.json??????6???ConvForward???????????????{}".format(unset_ConvForward_result)
    else:
        assert False, "??????time.json??????6???ConvForward???????????????{}".format(unset_ConvForward_result)


@pytest.mark.fork_dataloader
@allure.feature("fork_dataloader")
def test_37_fork_dataloader():
    case_name = "fork_dataloader"
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test/tests/python_layer/dataloader")
    info = "All tests passed"
    run_command = "srun -p {} python forkargs_test.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 300, "")
    run_command_info = "cat /{}".format(run_result_file)
    run_result = cf.run_and_extract_result("y",  run_command_info, 30, info)
    actual_info = []
    if run_result:
        if "All tests passed" not in run_result[0]:
            actual_info.append("????????????All tests passed??????")
    else:
        actual_info.append("????????????All tests passed??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "fork dataloader?????????????????????/??????/??????????????????????????????"
        expect_info = "fork dataloader?????????????????????/??????/??????????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"fork dataloader?????????????????????/??????/??????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        assert "All tests passed" in run_result[0], "????????????All tests passed???????????????{}".format(run_result)
    else:
        assert False, "????????????All tests passed???????????????{}".format(run_result)


@allure.feature("caffe")
def test_38_caffe():
    case_name = "caffe"
    cf.create_directory(cn["base_path"] + case_name)
    git_clone_command = "git clone git@gitlab.bj.sensetime.com:liupei1/pointcloud3ddettestcase.git"
    cf.git_clone(cn["base_path"] + case_name, git_clone_command)
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(10, "cd pointcloud3ddettestcase")
    info = "rpn_final.caffemodel"
    run_command = "bash to_caffe.sh  {}>> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cf.cd_command(10, "cd FPNv2_caffe")
    cf.cd_command(20, "ll >>/{}".format(run_result_file))
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if result:
        if "rpn_final.caffemodel" not in result[0]:
            actual_info.append("????????????'rpn_final.caffemodel' ??????")
    else:
        actual_info.append("????????????'rpn_final.caffemodel' ??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ??????Pointcloud3ddet???parrots?????????caffe??????????????????"
        expect_info = "Parrots ??????Pointcloud3ddet???parrots?????????caffe????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ??????Pointcloud3ddet???parrots?????????caffe????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "rpn_final.caffemodel" in result[0], "???????????????FPNv2_caffe?????????????????????rpn_final.caffemodel?????????,????????????{}".format(result[0])
    else:
        assert False, "???????????????FPNv2_caffe?????????????????????rpn_final.caffemodel?????????,????????????"


@allure.feature("config_yaml")
def test_39_config_yaml():
    case_name = "config_yaml"
    cf.cd_command(20, "cd")
    cf.cd_command(20, "rm -rf .parrots")
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/parrots.example/")
    info = "Parameter Group 0"
    run_command = "nohup sh runner/example/train.sh  {} 8 resnet50   >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 700, "")
    cat_file = "cat /{}".format(run_result_file)
    run_result = cf.run_and_extract_result("y",  cat_file, 30, info)
    log.info("run_result is {}".format(run_result))
    actual_info = []
    if run_result:
        if "Parameter Group 0" not in run_result[0]:
            actual_info.append("??????????????????Parameter Group 0")
    else:
        actual_info.append("??????????????????Parameter Group 0")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ?????????????????????????????????????????????"
        expect_info = "Parrots ???????????????????????????????????????????????????"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ???????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        assert "Parameter Group 0" in run_result[0], "?????????????????????????????????????????????{}".format(run_result)
    else:
        assert False, "?????????????????????????????????????????????{}".format(run_result)

@allure.feature("basicConfig")
def test_40_basicConfig():
    case_name = "basicConfig"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd tests/log_utils/logs")
    info = "test successfully"
    run_command = "python test_log_basicConfig.py  >> /{}".format(run_result_file)
    cf.run_and_extract_result("n",  run_command, 620, "")
    cat_file = "cat /{}".format(run_result_file)
    valiation_result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if valiation_result:
        if "test successfully" not in valiation_result[0]:
            actual_info.append("???????????????????????? test successfully!")
    else:
        actual_info.append("???????????????????????? test successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots ??????basicConfig??????????????????"
        expect_info = "??????????????????????????? test successfully!"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name.lower()), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ??????basicConfig????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name.lower())]
    function_csv_list.append(csv_list)
    if valiation_result:
        assert "test successfully" in valiation_result[0], "??????????????????????????? test successfully!"
    else:
        assert False, "???????????????????????? test successfully!"

@allure.feature("initialization")
def test_41_initialization():
    case_name = "initialization"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/initialization")
    env_result = cf.check_env(cn["source_envi"])
    info = "Congratulations! Test pass!"
    run_command = "sh ./test.sh  >> /{} 2>&1 &".format(run_result_file)
    cf.run_and_extract_result("n",  run_command, 320, "")
    cat_file = "cat /{}".format(run_result_file)
    valiation_result = cf.run_and_extract_result("y",  cat_file, 60, info)
    actual_info = []
    if valiation_result:
        if "Congratulations! Test pass!" not in valiation_result[0]:
            actual_info.append("???????????????????????? Congratulations! Test pass!")
    else:
        actual_info.append("???????????????????????? Congratulations! Test pass!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Initilization????????????"
        expect_info = "??????????????????????????? Congratulations! Test pass!"
        
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Initilization??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if valiation_result:
        assert "Congratulations! Test pass!" in valiation_result[0], "??????????????????????????? Congratulations! Test pass!"
    else:
        assert False, "???????????????????????? Congratulations! Test pass!"


@allure.feature("parrots_pavi2")
def test_42_parrots_pavi2():
    case_name = "parrots_pavi2"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test")
    cf.submodule("git submodule update --init models/parrots.example")
    env_result = cf.check_env(cn["source_envi"])
    p = re.compile("Version.*(\d+[.]\d+[.]\d+)")
    pavi_result = cf.cd_command(20, "pip show pavi")
    log.info("pavi_result is {}".format(pavi_result))
    version = re.findall(p, pavi_result)
    if version:
        pavi_version = version[0].split(".")[0]
        if pavi_version == "2":
            run_command = "PARROTS_BENCHMARK=1 nohup sh runner/example/train.sh {} 8 resnet18_mix.short --pavi --pavi-project parrots_test --data_reader CephReader --max_step 1 > /{} 2>&1 &".format(
                cn["partition"], run_result_file)
            cf.run_and_extract_result("n", run_command, 6500, "")
            cat_file = "cat {}".format(run_result_file)
            keyword = "benchmark_avg_iter_time"
            result = cf.run_and_extract_result("y", cat_file, 20, keyword)
            actual_info = []
            if result:
                if "benchmark_avg_iter_time" not in result[0]:
                    actual_info.append("????????????????????????????????????:benchmark_avg_iter_time")
            else:
                actual_info.append("????????????????????????????????????:benchmark_avg_iter_time")
            flag = "success"
    if actual_info:
        flag = "fail"
        summary = "????????????pavi2 + parrots ??????????????????"
        expect_info = "????????????pavi2 + parrots ??????????????????????????????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"????????????pavi2 + parrots ????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if version:
        assert pavi_version == "2"
        if result:
            assert "benchmark_avg_iter_time" in result[0], "????????????????????????????????????:benchmark_avg_iter_time?????????{}".format(result)
        else:
            assert False, "????????????????????????????????????:benchmark_avg_iter_time?????????{}".format(result)


@allure.feature("dummy_pool_dataloader")
def test_043_dummy_pool_dataloader():
    case_name = "dummy_pool_dataloader"
    cf.create_directory(cn["base_path"]+case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, "cd parrots.test/tests/python_layer/dataloader")
    run_command = 'PARROTS_DATALOADER_MODE="DUMMY"  python  dummy_dataloader.py  >> /{} 2>&1 &'.format(run_result_file)
    keyword = "All tests passed"
    cf.run_and_extract_result("n",  run_command, 360, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 10, keyword)
    actual_info = []
    if result:
        if "All tests passed" not in result[0]:
            actual_info.append("??????dummydataloader???pooldataloader??????????????????, ?????????All tests passed")
    else:
        actual_info.append("??????dummydataloader???pooldataloader??????????????????, ?????????All tests passed")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????dummydataloader???pooldataloader??????????????????, ?????????All tests passed????????????"
        expect_info = "??????dummydataloader???pooldataloader??????????????????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"??????dummydataloader???pooldataloader????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "All tests passed" in result[0], "????????????All tests passed??????,????????????{}".format(result[0])
    else:
        assert False, "????????????All tests passed??????,????????????"

@allure.feature("modules_floatfunctional")
def test_044_modules_floatfunctional():
    case_name = "modules_floatfunctional"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/modules/")
    env_result = cf.check_env(cn["source_envi"])
    info_one = ".*PASSED.*Forward Error Test"
    info_two = ".*PASSED.*Compute Result Test.*cpu"
    info_three = ".*PASSED.*Compute Result Test.*cuda"
    info_four = ".*PASSED.*FloatFunctional Test"
    run_command = "srun --partition={} --gres=gpu:1 python floatfunctional_test.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result_one = cf.run_and_extract_result("y",  cat_file, 60, info_one)
    result_two = cf.run_and_extract_result("y",  cat_file, 60, info_two)
    result_three = cf.run_and_extract_result("y",  cat_file, 60, info_three)
    result_four = cf.run_and_extract_result("y",  cat_file, 60, info_four)
    actual_info = []
    if result_one:
        if "[PASSED] Forward Error Test" not in result_one[0]:
            actual_info.append("????????????[PASSED] Forward Error Test??????")
    else:
        actual_info.append("????????????[PASSED] Forward Error Test??????")

    if result_two:
        if "[PASSED] Compute Result Test: cpu" not in result_two[0]:
            actual_info.append("????????????[PASSED] Compute Result Test: cpu??????")
    else:
        actual_info.append("????????????[PASSED] Compute Result Test: cpu??????")

    if result_three:
        if "[PASSED] Compute Result Test: cuda" not in result_three[0]:
            actual_info.append("????????????[PASSED] Compute Result Test: cuda??????")
    else:
        actual_info.append("????????????[PASSED] Compute Result Test: cuda??????")

    if result_four:
        if "[PASSED] FloatFunctional Test" not in result_four[0]:
            actual_info.append("????????????[PASSED] FloatFunctional Test??????")
    else:
        actual_info.append("????????????[PASSED] FloatFunctional Test??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "modules FloatFunctional????????????"
        expect_info = "Forward Error Test??????,Compute Result Test??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"modules FloatFunctional??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result_one:
        assert "[PASSED] Forward Error Test" in result_one[0], "??????????????????[PASSED] Forward Error Test, ????????????{}".format(result_one)
    else:
        assert False, "??????????????????[PASSED] Forward Error Test, ????????????{}".format(result_one)
    if result_two:
        assert "[PASSED] Compute Result Test: cpu" in result_two[0], "??????????????????[PASSED] Compute Result Test: cpu, ????????????{}".format(result_two)
    else:
        assert False, "??????????????????[PASSED] Compute Result Test: cpu, ????????????{}".format(result_two)
    if result_three:
        assert "[PASSED] Compute Result Test: cuda" in result_three[0], "??????????????????[PASSED] Compute Result Test: cuda, ????????????{}".format(result_three)
    else:
        assert False, "??????????????????[PASSED] Compute Result Test: cuda, ????????????{}".format(result_three)
    if result_four:
        assert "[PASSED] FloatFunctional Test" in result_four[0], "??????????????????[PASSED] Compute Result Test: cuda, ????????????{}".format(result_four)
    else:
        assert False, "??????????????????[PASSED] FloatFunctional Test, ????????????{}".format(result_four)



@allure.feature("communication")
def test_045_communication():
    case_name = "communication"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/communication/")
    env_result = cf.check_env(cn["source_envi"])
    info = ".*PASSED.*Communication Test"
    run_command = "PARROTS_ALIGN_TORCH=1 srun --partition={} -N 1 --ntasks-per-node=4 --gres=gpu:4 python comm_align_pt.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "[PASSED] Communication Test" not in result[0]:
            actual_info.append("??????????????????[PASSED] Communication Test??????")
    else:
        actual_info.append("??????????????????[PASSED] Communication Test??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "??????????????????Pytorch????????????"
        expect_info = "??????????????????Pytorch?????????????????????PASSED??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            #original_compress = [run_result_file]
            #dlf.compress_file(original_compress)
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"??????????????????Pytorch??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "[PASSED] Communication Test" in result[0]
    else:
        assert False, "????????????????????????'[PASSED] Communication Test', ????????????{}".format(result)

# @pytest.mark.skip(reason="????????????")
@allure.feature("parrots_config_path")
def test_046_parrots_config_path():
    case_name = "parrots_config_path"
    cf.cd_command(20, "rm -rf .parrots")
    cf.cd_command(20, "source pat0.13.0rc0")
    cf.cd_command(20, 'python -c "import torch"')
    cf.cd_command(20, "sed -i '/PARROTS_DEBUG_MODE: None/d' .parrots/config.yaml")
    cf.cd_command(20, "sed -i '/PARROTS_DEBUG_MODE: None/d' .parrots/config.yaml")
    cf.cd_command(20, 'python -c "import torch"')
    result = cf.cd_command(20, 'cat .parrots/config.yaml | grep "PARROTS_DEBUG_MODE: None"')
    actual_info = []
    if result:
        if "PARROTS_DEBUG_MODE: None" in result:
            actual_info.append("????????????parrots?????? pat0.13.0rc0???config.yaml??????????????????????????????")
    cf.cd_command(20, 'conda deactivate')
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, 'python -c "import torch"')
    result = cf.cd_command(20, 'cat .parrots/config.yaml | grep "PARROTS_DEBUG_MODE: None"')
    if result:
        if "PARROTS_DEBUG_MODE: None" not in result:
            actual_info.append("????????????parrots??????{}???config.yaml?????????????????????????????????".format(env_result))
    flag = "success"
    if len(actual_info) > 0:
        flag = "fail"
        summary = "Parrots ?????????????????????????????????????????????????????????????????????????????????????????????"
        expect_info = "Parrots ????????????????????????????????????????????????????????????????????????????????????????????????????????????parrots??????{}???config.yaml?????????????????????????????????".format(env_result)
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            run_result_file = "/mnt/lustre/parrots.tester.s.03/.parrots/config.yaml"
            local_run_result_file = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"Parrots ???????????????????????????????????????????????????????????????????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if len(actual_info) > 0:
       assert False

@allure.feature("init_pytorch")
def test_047_init_pytorch():
    case_name = "init_pytorch"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/communication/")
    env_result = cf.check_env(cn["source_envi"])
    info = "SUCCESS"
    run_command = "nohup sh init_comm_align_pt.sh {}  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "SUCCESS" not in result[0]:
            actual_info.append("??????????????????SUCCESS??????")
    else:
        actual_info.append("??????????????????SUCCESS??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "?????????????????????Pytorch????????????"
        expect_info = "?????????????????????Pytorch?????????????????????SUCCESS??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            #a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"?????????????????????Pytorch??????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "SUCCESS" in result[0]
    else:
        assert False, "????????????????????????'SUCCESS', ????????????{}".format(result)


@allure.feature("exception_log")
def test_048_exception_log():
    case_name = "exception_log"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/log_utils/logs")
    env_result = cf.check_env(cn["source_envi"])
    info = "SUCCESS"
    run_command = "srun -p {} python test_log_bt_with_catch.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "SUCCESS" not in result[0]:
            actual_info.append("??????????????????SUCCESS??????")
    else:
        actual_info.append("??????????????????SUCCESS??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "???????????????????????????????????????log?????????????????????????????????"
        expect_info = "???????????????????????????????????????log??????????????????????????????????????????SUCCESS??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            local_run_result_file = "/" + cn["local_path"] + cn[
                "base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            later_list = [local_run_result_file]
            original = [run_result_file.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"???????????????????????????????????????log???????????????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "SUCCESS" in result[0]
    else:
        assert False, "????????????????????????'SUCCESS', ????????????{}".format(result)


@allure.feature("ddp_find_unused_parameters")
def test_049_ddp_find_unused_parameters():
    case_name = "ddp_find_unused_parameters"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    run_result_file_two = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "two.txt"
    cf.cd_command(20, "cd parrots.test/tests/python_layer/modules")
    env_result = cf.check_env(cn["source_envi"])
    info = "test successfully"
    run_command = "srun -p {} --gres=gpu:1 python ddp_unused.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "test successfully" not in result[0]:
            actual_info.append("??????????????????test successfully??????")
    else:
        actual_info.append("??????????????????test successfully??????")
    run_command_two = "srun -p {} --gres=gpu:1 python ddp_twice_used.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file_two)
    cf.run_and_extract_result("n",  run_command_two, 500, "")
    cat_file = "cat /{}".format(run_result_file_two)
    result_two = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result_two is {}".format(result_two))
    actual_info = []
    if result_two:
        if "test successfully" not in result_two[0]:
            actual_info.append("??????????????????test successfully??????")
    else:
        actual_info.append("??????????????????test successfully??????")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "DDP find_unused_parameters??????????????????"
        expect_info = "??????test successfully??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            local_run_result_file = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file_two = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "two.txt"
            later_list = [local_run_result_file, local_run_result_file_two]
            original = [run_result_file.replace("mnt", ""), run_result_file_two.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"DDP find_unused_parameters????????????", case_name, env_result, flag, [run_result_file, run_result_file_two], gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, "????????????????????????'test successfully', ????????????{}".format(actual_info)

@allure.feature("conv3d_shape")
def test_050_conv3d_shape():
    case_name = "conv3d_shape"
    cf.create_directory(cn["base_path"] + case_name)
    cf.git_clone(cn["base_path"] + case_name, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    cf.cd_command(20, "cd parrots.test/tests/python_layer/modules")
    env_result = cf.check_env(cn["source_envi"])
    info = "test_conv3d_large_shape PASSED"
    run_command = "srun -p {} --gres=gpu:1 pytest -vx conv3d_big_shape.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "test_conv3d_large_shape PASSED" not in result[0]:
            actual_info.append("??????????????????test_conv3d_large_shape PASSED??????")
    else:
        actual_info.append("??????????????????test_conv3d_large_shape PASSED??????")
    actual_info = []
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "conv3d?????????shape????????????????????????"
        expect_info = "??????test_conv3d_large_shape PASSED??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            local_run_result_file = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file_two = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "two.txt"
            later_list = [local_run_result_file, local_run_result_file_two]
            original = [run_result_file.replace("mnt", ""), run_result_file_two.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"conv3d?????????shape??????????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, "????????????????????????'test_conv3d_large_shape PASSED', ????????????{}".format(actual_info)

@allure.feature("randperm_cuda11")
def test_051_randperm_cuda11():
    case_name = "randperm_cuda11"
    cf.create_directory(cn["base_path"] + case_name)
    run_result_file_bianyi1 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "bianyi1.txt"
    run_result_file_bianyi2 = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "bianyi2.txt"
    cf.git_clone(cn["base_path"] + case_name, "git clone git@gitlab.bj.sensetime.com:platform/ParrotsDL/senseparrots.git")
    cf.cd_command(20, "cd senseparrots/")
    env_result = "pat2.0_dev_gcc5.4_cuda11"
    cf.check_env("source pat2.0_dev_gcc5.4_cuda11")
    cf.cd_command(20, "mkdir -p build")
    cf.cd_command(20, "cd build")
    run_command = "srun -p {} cmake .. -DATEN=ON -DHALF=ON  >> /{} 2>&1 &".format(cn["partition"], run_result_file_bianyi1)
    cf.run_and_extract_result("n", run_command, 500, "")
    run_command = "srun -p {} make -j12 && cd ../python && make -j12  >> /{} 2>&1 &".format(cn["partition"], run_result_file_bianyi2)
    cf.run_and_extract_result("n", run_command, 500, "")
    cf.cd_command(20, "export PYTHONPATH=$PWD:$PYTHONPATH")
    cf.cd_command(20, "cd ../../")
    cf.cd_command(180, cn["git_clone_command"])
    run_result_file = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
    log.info("run_result_file is {}".format(run_result_file))
    run_result_file_two = "/" + cn["pwd"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "two.txt"
    cf.cd_command(20, "cd parrots.test/tests/python_layer/modules")
    # env_result = cf.check_env(cn["source_envi"])
    info = "test_randperm PASSED"
    run_command = "srun -p {} --gres=gpu:1 pytest -vx randperm_cuda11.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("n",  run_command, 500, "")
    cat_file = "cat /{}".format(run_result_file)
    result = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result is {}".format(result))
    actual_info = []
    if result:
        if "test_randperm PASSED" not in result[0]:
            actual_info.append("??????????????????test_randperm PASSED??????")
    else:
        actual_info.append("??????????????????test_randperm PASSED??????")
    actual_info = []
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "randperm??????cuda11????????????"
        expect_info = "??????test_randperm PASSED??????"
        description = "??????: {}\n ??????: {}\n ????????????: {}\n ??????:  {}\n ??????:  {}\n   ??????:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
        try:
            local_run_result_file = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + ".txt"
            local_run_result_file_two = "/" + cn["local_path"] + cn["base_path"] + case_name + "/" + case_name + time_stamp + "two.txt"
            later_list = [local_run_result_file, local_run_result_file_two]
            original = [run_result_file.replace("mnt", ""), run_result_file_two.replace("mnt", "")]
            issue_upload_file = dlf.download_file("function", original, later_list, case_name)
            log.info("issue_upload_file is {}".format(issue_upload_file))
            a = AutoMakeIssueNA(cn["task_name"], summary, description, cn["assignee"])
            # a.submit_issue(issue_upload_file, cn["label"], cn["components"])
        except Exception as e:
            log.info(e)
    global  function_csv_list
    csv_list = [u"randperm??????cuda11????????????", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, "????????????????????????'test_randperm PASSED', ????????????{}".format(actual_info)



# def test_998_csv():
#     log.info("function_csv_list is {}".format(function_csv_list))
#     dlf.connect_vndevice("function")
#     path = "mkdir -p " + "/" + cn["local_path"] + "1102test/csv"
#     cf.cd_command(20, path)
#     with open("/{}1102test/csv/function_test1_{}.csv".format(cn["local_path"], time_stamp), "wb") as p:
#         csv_writer = ucsv.writer(p, encoding='gbk')
#         # csv_writer = csv.writer(p, dialect="excel")
#         try:
#             csv_writer.writerow([u"??????", u"????????????", u"??????", u"??????", u"????????????", u"????????????????????????", u"issue/??????"])
#         except Exception as e:
#             log.info("Exception is {}".format(e))
#         for i in range(len(function_csv_list)):
#             csv_writer.writerow(function_csv_list[i])
#     cf.cd_command(20, "exit")































if __name__ == '__main__':
    pytest.main(['-s', '-v', '-m "sunny"', 'test_parrots_function.py'])

