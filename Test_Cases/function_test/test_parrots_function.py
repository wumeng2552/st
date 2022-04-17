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
            actual_info.append("dataloader {} 测试失败, 找不到Test Passed".format(type))
    else:
        actual_info.append("dataloader {} 测试失败, 找不到Test Passed".format(result))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dataloader {} 测试失败".format(type)
        expect_info = "dataloader {} 测试通过".format(type)
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:   {}\n  备注: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"python层_dataloader", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "Test Passed" in result[0], "期望显示Test Passed!信息,实际显示{}".format(result[0])
    else:
        assert False, "期望显示Test Passed!信息,实际显示"


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
                    actual_info.append("dataloader {} 测试失败，找不到Test Passed".format(type))
        else:
            actual_info.append("dataloader {} 测试失败，找不到两个Test Passed".format(type))
    else:
        actual_info.append("dataloader {} 测试失败, 找不到两个Test Passed".format(result))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dataloader {} 测试失败".format(type)
        expect_info = ["dataloader {} 测试通过".format(type)]
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:   {}\n  备注: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"python层_dataloader", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        if len(result) == 2:
            for i in range(len(result)):
                assert "Test Passed" in result[i], "期望显示Test Passed!信息,实际显示{}".format(result[i])
        else:
            assert False, "期望显示两个Test Passed!信息,实际显示{}".format(result)

    else:
        assert False, "期望显示两个Test Passed!信息,实际显示{}".format(result)


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
            actual_info.append("import mmcv不成功")
    else:
        actual_info.append("import mmcv不成功")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dish_pybind11测试失败"
        expect_info = "成功安装mmcv并且可以成功import"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:   {}\n  备注: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"python层_dataloader", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "mmcv/__init__" in result[0], "期望显示import mmcv成功信息'mmcv/__init__',实际显示{}".format(result[0])
    else:
        assert False, "期望显示import mmcv成功信息'mmcv/__init__',实际显示"


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
                    actual_info.append("没有提示:Save successfully!")
        else:
            actual_info.append("没有打印1个Save successfully!")
    else:
        actual_info.append("parrots 执行save，没有提示:Save successfully!")
    keyword_1 = "Load and check successfully"
    parrots_1 = cf.run_and_extract_result("y", cat_file, 80, keyword_1)
    if parrots_1:
        if len(parrots_1) == 2:
            for i in range(2):
                if "Load and check successfully" not in parrots_1[i]:
                    actual_info.append("pytorch load，没有提示:Load and check successfully!")
        else:
            actual_info.append("没有打印两个:Load and check successfully!")
    else:
        actual_info.append("没有打印两个:Load and check successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 序列化测试失败"
        expect_info = [
            "如果parrots 执行save 成功，打印:Save successfully! 如果 pytorch load 成功， 打印:Load and check successfully! 如果 parrots load 成功，再次打印:Load and check successfully! "]
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:   {}\n  备注: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"序列化，反序列化及推理精度", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if parrots_0:
        if len(parrots_0) == 1:
            for i in range(1):
                assert "Save successfully" in parrots_0[i], "期望打印Save successfully，实际{}".format(parrots_0[i])
        else:
            assert False, "期望打印1个Save successfully!, 实际{}".format(parrots_0)
    else:
        assert False, "期望打印1个Save successfully!, 实际{}".format(parrots_0)
    if parrots_1:
        if len(parrots_1) == 2:
            for i in range(2):
                assert "Load and check successfully" in parrots_1[i], "期望打印Load and check successfully, 实际{}".format(
                    parrots_1[i])
        else:
            assert False, "期望打印两个:Load and check successfully!, 实际{}".format(parrots_1)
    else:
        assert False, "期望打印两个:Load and check successfully!, 实际{}".format(parrots_1)


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
            actual_info.append("没有报出RuntimeError")
    else:
        actual_info.append("没有报出RuntimeError")
    info_ten = "tensor\(\[2. 2.\]\)"
    result_end = cf.run_and_extract_result("y", "x + 1", 60, info_ten)
    if result_end:
        if "tensor([2. 2.])" not in result_end:
            actual_info.append("没有报出tensor([2. 2.])")
    else:
        actual_info.append("没有报出tensor([2. 2.])")
    cf.cd_command(20, "exit()")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "host2cuda错误处理测试失败"
        expect_info = ["预期报出RuntimeError", "显示结果tensor([2. 2.])"]

        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:   {}\n  备注: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info( "function_file_link.ini","function_slurm_link",case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"host2cuda错误处理测试", case_name, env_result, flag, run_result_file,
                gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if x_result:
        assert "RuntimeError" in x_result, "期望显示RuntimeError,实际显示{}".format(x_result)
    else:
        assert False, "期望显示RuntimeError,实际显示{}".format(x_result)
    if result_end:
        assert "tensor([2. 2.])" in result_end, "期望显示tensor([2. 2.]),实际显示{}".format(result_end)
    else:
        assert False, "期望显示tensor([2. 2.]),实际显示{}".format(result_end)


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
                actual_info.append("{}读取数据失败，log日志没有找到跑成功的信息'benchmark_avg_iter_time'".format(kind[i]))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots datareader测试失败"
        expect_info = "CephReader,MemcachedReader,DirectReader读取数据成功，log日志都能找到benchmark_avg_iter_time信息"

        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望: {}\n 实际: {}\n  备注: {}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots datareader测试", case_name, env_result, flag, run_result_file,
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
                actual_info.append("速度测试结果:{} > 2.1".format(float(result[0])))

        else:
            if float(result[0]) > 1.6:
                actual_info.append("速度测试结果:{} > 1.6".format(float(result[0])))

    else:
        actual_info.append("没有显示速度")
    flag = "success"
    if actual_info:
        flag = "fail"
        if cn["ip"] == "10.5.38.31" or cn["ip"] == "10.5.36.31":
            expect_info = "速度测试结果:{} < 2.1".format(float(result[0]))
        else:
            expect_info = "速度测试结果:{} < 1.6".format(float(result[0]))

        summary = "Parrots 小op执行(timy ops)测试失败"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 小op执行(timy ops)", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if cn["ip"] == "10.5.38.31" or cn["ip"] == "10.5.36.31":
        if result:
            assert float(2.1) > float(result[0]), "在SH36集群期望速度小于2.1s',实际显示{} > 2.1".format(float(result[0]))
        else:
            assert False, "没有显示速度"
    else:
        if result:
            log.info("result[0] type is {}".format(type(result[0])))
            assert float(1.6) > float(result[0]), "在SH1984集群,期望速度小于1.6s',实际显示{} > 1.6".format(float(result[0]))
        else:
            assert False, "没有显示速度"



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
            actual_info.append("SYNC MODE 训练找不到结束关键字Epoch: [1/1][5000/5005]")
    else:
        actual_info.append("SYNC MODE 训练找不到结束关键字Epoch: [1/1][5000/5005]")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 执行模式（exec_mode）-SYNC MODE 测试失败"
        expect_info = ["SYNC MODE 训练在 1 个 epoch 之后结束"]
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 执行模式（exec_mode_sync）测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if sync_result:
        assert "Epoch: [1/1][5000/5005]" in sync_result[0], "期望SYNC MODE 训练在 1 个 epoch 之后结束, 实际找不到结束关键字Epoch: [1/1][5000/5005]"
    else:
        assert False, "期望SYNC MODE 训练在 1 个 epoch 之后结束, 实际找不到结束关键字Epoch: [1/1][5000/5005]"


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
            actual_info.append("ASYNC MODE 训练找不到结束关键字Epoch: [1/1][5000/5005]")
    else:
        actual_info.append("ASYNC MODEE 训练找不到结束关键字Epoch: [1/1][5000/5005]")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 执行模式（exec_mode）-ASYNC MODE 测试失败"
        expect_info = ["Epoch: [1/1][5000/5005]"]
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 执行模式（exec_mode_async）测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if async_result:
        assert "Epoch: [1/1][5000/5005]" in async_result[0], "期望SYNC MODE 训练在 1 个 epoch 之后结束, 实际找不到结束关键字Epoch: [1/1][5000/5005]"
    else:
        assert False, "期望SYNC MODE 训练在 1 个 epoch 之后结束, 实际找不到结束关键字Epoch: [1/1][5000/5005]"



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
            actual_info.append("nonoverlap 没有显示正常结束标志Benchmark: [199/200]，不是正常结束")
    else:
        actual_info.append("nonoverlap 没有显示正常结束标志Benchmark: [199/200]，不是正常结束")
        nonoverlap_time = 0
    # read overlap result
    cat_file = "cat /{}".format(run_result_file)
    over = cf.run_and_extract_result("y", cat_file, 80, info)
    if over:
        overlap_time = over[0][1].split(")")[0]
        log.info("overlap_time is {}".format(overlap_time))
        if "199/200" not in over[0]:
            actual_info.append("overlap 没有显示正常结束标志Benchmark: [199/200]，不是正常结束")

    else:
        actual_info.append("overlap 没有显示正常结束标志Benchmark: [199/200]，不是正常结束")
        overlap_time = 0
    if overlap_time:
        if nonoverlap_time:
            if float(overlap_time) > float(nonoverlap_time):
                actual_info.append("overlap 的时间:{}没有比 nonoverlap的时间: {}短".format(overlap_time, nonoverlap_time))
        else:
            actual_info.append("没有nonoverlap time")
    else:
        actual_info.append("没有overlap time")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 通信计算重叠（overlap）测试失败"
        expect_info = "overlap和nonoverlap训练正常结束，overlap 的时间比 nonoverlap 的时间短"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 通信计算重叠（overlap）", case_name, env_result, flag, [run_result_file, run_result_file_no], gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if nonover:
        assert "199/200" in nonover[0], "期望nonoverlap显示正常结束标志Benchmark: [199/200], 实际显示{}".format(nonover[0])
    else:
        assert False, "期望nonoverlap显示正常结束标志Benchmark: [199/200], 实际显示{}".format(nonover)
    if over:
        assert "199/200" in over[0], "期望overlap显示正常结束标志Benchmark: [199/200], 实际显示{}".format(over[0])
    else:
        assert False, "期望overlap显示正常结束标志Benchmark: [199/200], 实际显示{}".format(over)
    if overlap_time:
        if nonoverlap_time:
            assert float(nonoverlap_time) > float(
                overlap_time), "期望overlap 的时间比 nonoverlap 的时间短, 实际overlap 的时间{} > nonoverlap 的时间{}".format(
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
                            actual_info.append("parrots{} 的 {} time 大于 parrots0.5 的{} time".format(cn["source_envi"], types[i], types[i]))
                else:
                    actual_info.append("没有找到parrots0.5的7个算子信息")
            else:
                actual_info.append("没有找到parrots{}的7个算子信息".format(cn["source_envi"]))
        else:
            actual_info.append("没有找到parrots0.5的7个算子信息")
    else:
        actual_info.append("没有找到parrots{}的7个算子信息".format(cn["source_envi"]))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots CUDA random算子性能对比测试失败"
        expect_info = "与parrots0.5的性能对比:parrots {} 的 ['rand', 'randn', 'randperm', 'randint', 'bernoulli_', 'cauchy_', 'random_']时间 少于 parrots0.5 ['rand', 'randn', 'randperm', 'randint', 'bernoulli_', 'cauchy_', 'random_']时间".format(cn["source_envi"])
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots CUDA random算子性能测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if rusult_now:
        if rusult_5:
            if len(rusult_now) == 7:
                if len(rusult_5) == 7:
                    for i in range(len(rusult_now)):
                        assert float(rusult_now[i]) < float(rusult_5[i]), "期望parrots {} 的 {} time 少于 parrots0.5 的{} time, 实际parrots{} 的 {} time: {} > parrots0.5 的{} time: {}".format(cn["source_envi"], types[i], types[i], cn["source_envi"], types[i], float(rusult_now[i]), types[i], float(rusult_5[i]))
                else:
                    assert False, "没有找到parrots0.5的7个算子信息"
            else:
                assert False, "没有找到parrots{}的7个算子信息".format(cn["source_envi"])
        else:
            assert False, "没有找到parrots0.5的7个算子信息"
    else:
        assert False, "没有找到parrots{}的7个算子信息".format(cn["source_envi"])


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
            actual_info.append("没有输出:All tests successfully!")
    else:
        actual_info.append("没有输出:All tests successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "测试Parrots训练模型多次转换是否均正常测试失败"
        expect_info = "期望输出:All tests successfully!"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots训练模型多次转换是否均正常测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "All tests successfully!" in result, "期望显示All tests successfully!,实际显示{}".format(result)
    else:
        assert False, "期望显示All tests successfully!,实际显示{}".format(result)

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
            actual_info.append("validation的psnr的小于26")
    else:
        actual_info.append("validation的psnr的值没有显示")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "测试Parrots训练模型多次量化训练是否均正常测试失败"
        expect_info = "validation的psnr的值大于26"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots训练模型多次量化训练是否均正常测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if valiation_result:
        assert float(valiation_result[-1]) > 26, "期望validation的psnr的大于26,实际validation的psnr的小于26"
    else:
        assert False, "validation的psnr的值没有显示"



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
            actual_info.append("没有显示 'Close Successfully!'")
    else:
        actual_info.append("没有显示 'Close Successfully!'")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "测试Parrots进行量化训练模型中途取消是否会产生不良影响测试失败"
        expect_info = "运行会中途取消的模型转换，提示Close Successfully!"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots进行量化训练模型中途取消是否会产生不良影响测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "Close Successfully!" in result[0], "期望运行会中途取消的模型转换提示Close Successfully!, 实际显示{}".format(result[0])
    else:
        assert False, "期望运行会中途取消的模型转换提示Close Successfully!, 实际显示{}".format(result)


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
            actual_info.append("没有显示 'Upload Successfully' ")
    else:
        actual_info.append("没有显示 'Upload Successfully'")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "测试Parrots训练模型结构能否可视化测试失败"
        expect_info = "Upload Successfully"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots训练模型结构能否可视化测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if upload_result:
        assert "Upload Successfully" in upload_result[0], "期望显示Upload Successfully,实际显示{}".format(upload_result[0])
    else:
        assert False, "期望显示Upload Successfully,实际显示{}".format(upload_result)


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
            actual_info.append("运行会中途取消的模型转换，没有提示:Close Successfully!")
    else:
        actual_info.append("运行会中途取消的模型转换，没有提示:Close Successfully!")
    convert_info = "Test Successfully\!"
    run_command_convert = "srun -p {} --gres=gpu:1 python test_convert.py  >> /{}".format(cn["partition"], run_result_file)
    cf.run_and_extract_result("y",  run_command_convert, 860, "")
    cat_file = "cat /{}".format(run_result_file)
    convert_result = cf.run_and_extract_result("y",  cat_file, 60, convert_info)
    if convert_result:
        if "Test Successfully!" not in convert_result:
            actual_info.append("测试能否正常转换，没有提示:Test Successfully!")
    else:
        actual_info.append("测试能否正常转换，没有提示:Test Successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "测试Parrots训练模型转换中途取消是否会产生不良影响测试失败"
        expect_info = ["运行会中途取消的模型转换，成功的话则会提示:Close Successfully!", "测试能否正常转换，成功的话会输出:Test Successfully!"]
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots训练模型转换中途取消是否会产生不良影响测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if cancel_result:
        assert "Close Successfully!" in cancel_result, "期望显示Close Successfully!,实际显示{}".format(cancel_result)
    else:
        assert False, "期望显示Close Successfully!,实际显示{}".format(cancel_result)
    if convert_result:
        assert "Test Successfully!" in convert_result, "期望显示Test Successfully!,实际显示{}".format(convert_result)
    else:
        assert False, "期望显示Test Successfully!,实际显示{}".format(convert_result)


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
            actual_info.append("pytest报错")
    else:
        actual_info.append("pytest报错")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 训练生态支持/torchvision测试测试失败"
        expect_info = "pytest正常通过，没有报错"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 训练生态支持/torchvision测试测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "PASSED   [100%]" in result[0], "期望显示pytest正常通过标志PASSED   [100%],实际显示{}".format(result[0])
    else:
        assert False, "期望显示pytest正常通过标志PASSED   [100%],实际显示{}".format(result)



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
                actual_info.append("没有开启debug模式报错")
        else:
            actual_info.append("没有开启debug模式报错")
    except Exception as e:
        log.info(e)
    debug_info = "AssertionError"
    python_debug_command = 'PARROTS_USER_UPLOAD_DEBUG=1 python -c "import torch" >> {} 2>&1 &'.format(run_result_file1)
    cf.run_and_extract_result("n",  python_debug_command, 800, "")
    cat_file = "cat /{}".format(run_result_file1)
    debug_result = cf.run_and_extract_result("y",  cat_file, 10, debug_info)
    if debug_result:
        if "AssertionError" not in debug_result[0]:
            actual_info.append("开启debug模式没有报错")
    else:
        actual_info.append("开启debug模式没有报错")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "parrots0.8.0 数据埋点debug模式测试失败"
        expect_info = "没有开启debug模式的情况下在集群使用parrots时，预期一切正常,开启debug模式的情况下在集群直接使用parrots时，预期报出AssertionErro"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"数据埋点debug模式测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if nodebug_result:
        assert "MCA parameter" in nodebug_result[0], "开启debug模式时在集群使用parrots预期一切正常, 实际没有找到正常通过标志MCA parameter"
    else:
        assert False, "开启debug模式时在集群使用parrots预期一切正常, 实际没有找到正常通过标志MCA parameter"
    if debug_result:
        assert "AssertionError" in debug_result[0], "开启debug模式在集群直接使用parrots预期报出AssertionError, 实际没有找到AssertionError"
    else:
        assert False, "开启debug模式在集群直接使用parrots预期报出AssertionError, 实际没有找到AssertionError"


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
            actual_info.append("执行no_dump.sh后没有打印'Segmentation fault'信息")
    else:
        actual_info.append("执行no_dump.sh后没有打印'Segmentation fault'信息")
    file_list = cf.cd_command(20, "ll")
    no_core = re.compile("core.\d+")
    no_core_result = re.findall(no_core, file_list)
    if no_core_result:
        actual_info.append("执行no_dump.sh后，本地目录产生core.<pid>" )
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots noDump测试失败"
        expect_info = "执行no_dump.sh后，屏幕上同样先打印编译信息，然后打印segmentation fault信息，本地目录不会产生core.<pid>"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots noDump测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("执行dump.sh后没有 打印'Segmentation fault'信息")
    else:
        actual_info.append("执行dump.sh后没有 打印'Segmentation fault'信息")
    core = "ll >> /{}".format(run_result_file)
    cf.run_and_extract_result("n",  core, 1, "")
    cat_file = "cat /{}".format(run_result_file)
    core_result = cf.run_and_extract_result("y",  cat_file, 60, "core.\d+")
    if core_result:
        if "core" not in core_result[0]:
            actual_info.append("执行dump.sh后，本地未生成core.<pid>")
    else:
        actual_info.append("执行dump.sh后，本地未生成core.<pid>")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots Dump测试失败"
        expect_info = "执行dump.sh后，本地会生成core.<pid>（其中pid为进程号，是数字类型）。屏幕首先打印编译信息，然后打印segmentation fault报错信息"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots Dump测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("屏幕显示没有 'invalid broadcast bcast' 信息")
    else:
        actual_info.append("屏幕显示没有 'invalid broadcast bcast' 信息")
    find_file = cf.run_and_extract_result("y",  "ll", 10, "log_exception.txt")
    if find_file:
        file_info = cf.run_and_extract_result("y",  "cat log_exception.txt", 20, info)
        if file_info:
            if "invalid broadcast bcast" not in file_info[0]:
                actual_info.append("文件log_exception.txt 没有 'invalid broadcast bcast' 信息")
        else:
            actual_info.append(" 文件 log_exception.txt 没有 'invalid broadcast bcast' 信息")
    else:
        actual_info.append("没有找到log_exception.txt文件")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 测试异常下的日志测试失败"
        expect_info = "屏幕显示invalid broadcast bcast信息，并且生成了一个文件，文件名为log_exception.txt，其内容同屏幕显示"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 测试异常下的日志测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
                actual_info.append("file 没有 {}".format(file_expect_result[i]))
    else:
        actual_info.append("没有找到log_level.txt文件")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 测试日志分级测试失败"
        expect_info = "屏幕显示[I] info 1，[W] warn 1....等信息，并且会同时生成一个文件，文件名为log_level.txt，其内容同屏幕"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 测试日志分级测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
                actual_info.append("log_limit.txt 没有 message")
        else:
            actual_info.append("log_limit.txt 没有 message")
    else:
        actual_info.append("没有找到log_limit.txt文件")
    find_file1 = cf.run_and_extract_result("y",  "ll", 10, "log_limit.1.txt")
    if find_file1:
        result1 = cf.cd_command(20, "cat log_limit.1.txt")
        log.info("result1 is {}".format(result1))
        if result1:
            if "message is here!" not in result1:
                actual_info.append("log_limit.1.txt 没有 message")
        else:
            actual_info.append("log_limit.1.txt 没有 message")
    else:
        actual_info.append("没有找到log_limit.1.txt文件")
    find_file2 = cf.run_and_extract_result("y",  "ll", 10, "log_limit.2.txt")
    if find_file2:
        result2 = cf.cd_command(20, "cat log_limit.2.txt")
        log.info("file_result is {}".format(result2))
        if result2:
            if "message is here!" not in result2:
                actual_info.append("log_limit.2.txt 没有 message")
        else:
            actual_info.append("log_limit.2.txt 没有 message")
    else:
        actual_info.append("没有找到log_limit.2.txt文件")
    flag = "success"
    if actual_info:
        flag = "fail"
        log.info("result is {}".format(result))
        summary = "Parrots 测试日志的大小限制测试失败"
        expect_info = "生成了三个文件 log_limit.txt， log_limit.1.txt， log_limit.2.txt，三个文件内容都有message is here!"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 测试日志的大小限制测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("屏幕没有显示gpu id: 3这些信息")
    else:
        actual_info.append("屏幕没有显示gpu id: 3这些信息")
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
                actual_info.append("{} 内容不正确,实际内容为:{}".format(log_file_find[i], result_file_end))
    else:
        actual_info.append("找到{}个log_model文件".format(len(log_file_find)))
        log.info("log_file_find is {}".format(log_file_find))
        file_info = ["gpu id: 0", "gpu id: 1", "gpu id: 2", "gpu id: 3"]
        log.info("cat result_file is:")
        for i in range(len(log_file_find)):
            log.info("cat file is {}".format(log_file_find[i]))
            result_file_end = cf.cd_command(20, 'cat {}'.format(log_file_find[i]))
            time.sleep(1)
            log.info("result_file_end is {}".format(result_file_end))
            if file_info[i] not in result_file_end:
                actual_info.append("{} 内容不正确, 实际内容为:{}".format(log_file_find[i], result_file_end))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 验证多进程下的日志系统测试失败"
        expect_info = "屏幕显示model name信息，生成了四个文件"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 验证多进程下的日志系统测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("最后一行没有打印Total pycfile 0")
    else:
        actual_info.append("最后一行没有打印Total pycfile 0")
    if result_2:
        if "dist-info/RECORD" not in result_2[0]:
            actual_info.append("倒数第二行没有打印dist-info/RECORD")
    else:
        actual_info.append("倒数第二行没有打印dist-info/RECORD")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 部署代码pyc加密测试失败"
        expect_info = "倒数第二行打印dist-info/RECORD,最后一行打印Total pycfile 0"        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 部署代码pyc加密测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("dataloader prefetch 2 at origin测试失败, 找不到Test for dataloader prefetch_remain passed".format(result))
    else:
        actual_info.append("dataloader prefetch 2 at origin测试失败, 找不到Test for dataloader prefetch_remain passed".format(result))
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "dataloader_prefetch 测试失败"
        expect_info = "显示Test for dataloader prefetch_remain passed信息"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"dataloader_prefetch 测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
    cf.cd_command(20, "cd ../")    # ·µ»Øext_based_pytorch
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
            actual_info.append("没有找到test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED信息")
        if "test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED" not in srun_result:
            actual_info.append("没有找到test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED信息")
    else:
        actual_info.append("没有找到test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED, test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots extension测试失败"
        expect_info = "找到test_gelu.py::TestExtension::test_pytorch_ext_gelu_cpu PASSED, test_gelu.py::TestExtension::test_pytorch_ext_gelu_cuda PASSED信息"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots extension测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("没有找到test successfully!信息，报错日志生成失败")
    else:
        actual_info.append("没有找到test successfully!信息，报错日志生成失败")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots测试报错日志生成测试失败"
        expect_info = "Parrots测试报错日志生成测试成功, 打印:test successfully"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots测试报错日志生成测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("执行测试文件 test_config_env.py 没有正常运行, 找不到正常运行信息")
    else:
        actual_info.append("执行测试文件 test_config_env.py 没有正常运行, 找不到正常运行信息")
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
            actual_info.append("执行python命令行和语句，得到结果不是True")
    else:
        actual_info.append("执行python命令行和语句，得到结果不是True")
    on_off = "sed -i" + " " + '"{}'.format("s/PARROTS_OPBENCHMARK: ") + "'{}'".format(
        "ON") + "/PARROTS_OPBENCHMARK: " + "'{}'".format("OFF") + '{}"'.format("/") + " " + "~/.parrots/config.yaml"
    log.info("off_on is {}".format(off_on))
    cf.cd_command(20, on_off)
    cf.cd_command(20, "cat ~/.parrots/config.yaml")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots验证配置文件导入环境变量测试失败"
        expect_info = "执行测试文件 test_config_env.py 正常运行，无报错, 执行python命令行和语句，得到结果为True"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots验证配置文件导入环境变量测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("屏幕上没有打印出time costing origin信息")
    else:
        actual_info.append("屏幕上没有打印出time costing origin信息")
    if rusult_now_1:
        if "time costing coderized" not in rusult_now_1[0]:
            actual_info.append("屏幕上没有打印出time costing coderized信息")
    else:
        actual_info.append("屏幕上没有打印出time costing coderized信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "在线编译benchmark功能测试失败"
        expect_info = "屏幕上打印出如下字样time costing origin: XXXX,time costing coderized: XXXX"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"在线编译benchmark功能测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("没有找到模型训练成功标志:benchmark_mem_cached")
    else:
        actual_info.append("没有找到模型训练成功标志:benchmark_mem_cached")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "cuda10环境模型训练失败"
        expect_info = "cuda10环境模型训练成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"cuda10环境模型训练", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("没有找到无GPU使用parrots成功标志:successfully")
    else:
        actual_info.append("没有找到无GPU使用parrots成功标志:successfully")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "无GPU使用parrots测试失败"
        expect_info = "无GPU使用parrots测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"无GPU使用parrots测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("没有打印:Test successfully!")
    else:
        actual_info.append("没有打印:Test successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "parrots stack 优化测试失败"
        expect_info = "parrots stack 优化测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"parrots stack 优化测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("没有打印:Import Torchvision Successfully!")
    else:
        actual_info.append("没有打印:Import Torchvision Successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots测试torchvision测试失败"
        expect_info = "Parrots测试torchvision测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots测试torchvision测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("日志重复打印[100/7330]")
        else:
            if "[100/7330]" not in run_result[0]:
                actual_info.append("没有打印:[100/7330]")
    else:
        actual_info.append("没有打印:[100/7330]")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "验证mmdet等模型log打印一遍测试失败"
        expect_info = "验证mmdet等模型log打印一遍测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"验证mmdet等模型log打印一遍测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("没有找到timeline.json文件")
    else:
        actual_info.append("没有找到timeline.json文件")
    ConvForward = "grep -ws " + "'{}' timeline.json -A 3  >> /{}".format('"name": "ConvForward",', export_result_file)
    log.info("ConvForward is {}".format(ConvForward))
    cf.cd_command(60, ConvForward)
    ConvForward_info = "ConvForward"
    ConvForward_result = cf.run_and_extract_result("y", cat_file, 20, ConvForward_info)
    log.info("ConvForward_result is {}".format(ConvForward_result))
    if ConvForward_result:
        if len(ConvForward_result) != 6:
            actual_info.append("timeline.json没有找到6个ConvForward信息")
    else:
        actual_info.append("timeline.json没有找到6个ConvForward信息")
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
            actual_info.append("没有找到time.json文件")
    else:
        actual_info.append("没有找到time.json文件")
    unset_ConvForward = "grep -ws " + "'{}' time.json -A 3  >> /{}".format('"name": "ConvForward",', unset_result_file)
    log.info("unset_ConvForward is {}".format(unset_ConvForward))
    cf.cd_command(60, unset_ConvForward)
    unset_ConvForward_info = "ConvForward"
    unset_ConvForward_result = cf.run_and_extract_result("y", unset_cat_file, 30, unset_ConvForward_info)
    log.info("unset_ConvForward_result is {}".format(unset_ConvForward_result))
    if unset_ConvForward_result:
        if len(unset_ConvForward_result) != 6:
            actual_info.append("time.json没有找到6个ConvForward信息")
    else:
        actual_info.append("time.json没有找到6个ConvForward信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots测试timeline打印fn和op开关测试失败"
        expect_info = "Parrots测试timeline打印fn和op开关测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots测试timeline打印fn和op开关测试", case_name, env_result, flag, [export_result_file, unset_result_file], gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        assert "timeline.json" in run_result[0], "期望找到timeline.json文件，实际{}".format(run_result)
    else:
        assert False, "期望找到timeline.json文件，实际{}".format(run_result)
    if unset_run_result:
        assert "time.json" in unset_run_result[0], "期望找到time.json文件，实际{}".format(unset_run_result)
    else:
        assert False, "期望找到time.json文件，实际{}".format(unset_run_result)
    if ConvForward_result:
        assert len(ConvForward_result) == 6, "期望timeline.json找到6个ConvForward信息，实际{}".format(ConvForward_result)
    else:
        assert False, "期望timeline.json找到6个ConvForward信息，实际{}".format(ConvForward_result)
    if unset_ConvForward_result:
        assert len(unset_ConvForward_result) == 6, "期望time.json找到6个ConvForward信息，实际{}".format(unset_ConvForward_result)
    else:
        assert False, "期望time.json找到6个ConvForward信息，实际{}".format(unset_ConvForward_result)


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
            actual_info.append("没有找到All tests passed信息")
    else:
        actual_info.append("没有找到All tests passed信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "fork dataloader启动参数序列化/压缩/传输融合测试测试失败"
        expect_info = "fork dataloader启动参数序列化/压缩/传输融合测试测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"fork dataloader启动参数序列化/压缩/传输融合测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        assert "All tests passed" in run_result[0], "期望找到All tests passed信息，实际{}".format(run_result)
    else:
        assert False, "期望找到All tests passed信息，实际{}".format(run_result)


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
            actual_info.append("没有找到'rpn_final.caffemodel' 文件")
    else:
        actual_info.append("没有找到'rpn_final.caffemodel' 文件")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 测试Pointcloud3ddet中parrots模型转caffe是否成功失败"
        expect_info = "Parrots 测试Pointcloud3ddet中parrots模型转caffe是否成功测试通过"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 测试Pointcloud3ddet中parrots模型转caffe是否成功", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "rpn_final.caffemodel" in result[0], "期望生成的FPNv2_caffe目录下有一个叫rpn_final.caffemodel的文件,实际显示{}".format(result[0])
    else:
        assert False, "期望生成的FPNv2_caffe目录下有一个叫rpn_final.caffemodel的文件,实际显示"


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
            actual_info.append("没有正常打印Parameter Group 0")
    else:
        actual_info.append("没有正常打印Parameter Group 0")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 验证多进程读取配置文件测试失败"
        expect_info = "Parrots 验证多进程读取配置文件测试测试成功"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 验证多进程读取配置文件测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if run_result:
        assert "Parameter Group 0" in run_result[0], "期望正常打印，无报错卡住，实际{}".format(run_result)
    else:
        assert False, "期望正常打印，无报错卡住，实际{}".format(run_result)

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
            actual_info.append("执行后，没有输出 test successfully!")
    else:
        actual_info.append("执行后，没有输出 test successfully!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Parrots 测试basicConfig接口测试失败"
        expect_info = "执行后，观察到输出 test successfully!"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name.lower()), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 测试basicConfig接口测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name.lower())]
    function_csv_list.append(csv_list)
    if valiation_result:
        assert "test successfully" in valiation_result[0], "执行后，观察到输出 test successfully!"
    else:
        assert False, "执行后，没有输出 test successfully!"

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
            actual_info.append("执行后，没有输出 Congratulations! Test pass!")
    else:
        actual_info.append("执行后，没有输出 Congratulations! Test pass!")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "Initilization测试失败"
        expect_info = "执行后，观察到输出 Congratulations! Test pass!"
        
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Initilization测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if valiation_result:
        assert "Congratulations! Test pass!" in valiation_result[0], "执行后，观察到输出 Congratulations! Test pass!"
    else:
        assert False, "执行后，没有输出 Congratulations! Test pass!"


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
                    actual_info.append("没有找到模型训练成功标志:benchmark_avg_iter_time")
            else:
                actual_info.append("没有找到模型训练成功标志:benchmark_avg_iter_time")
            flag = "success"
    if actual_info:
        flag = "fail"
        summary = "验证使用pavi2 + parrots 模型训练失败"
        expect_info = "验证使用pavi2 + parrots 模型可以正常跑通成功"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"验证使用pavi2 + parrots 模型训练", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if version:
        assert pavi_version == "2"
        if result:
            assert "benchmark_avg_iter_time" in result[0], "期望找到模型训练成功标志:benchmark_avg_iter_time，实际{}".format(result)
        else:
            assert False, "期望找到模型训练成功标志:benchmark_avg_iter_time，实际{}".format(result)


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
            actual_info.append("解决dummydataloader和pooldataloader冲突测试失败, 找不到All tests passed")
    else:
        actual_info.append("解决dummydataloader和pooldataloader冲突测试失败, 找不到All tests passed")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "解决dummydataloader和pooldataloader冲突测试失败, 找不到All tests passed测试失败"
        expect_info = "解决dummydataloader和pooldataloader冲突测试通过"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"解决dummydataloader和pooldataloader冲突测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "All tests passed" in result[0], "期望显示All tests passed信息,实际显示{}".format(result[0])
    else:
        assert False, "期望显示All tests passed信息,实际显示"

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
            actual_info.append("没有找到[PASSED] Forward Error Test信息")
    else:
        actual_info.append("没有找到[PASSED] Forward Error Test信息")

    if result_two:
        if "[PASSED] Compute Result Test: cpu" not in result_two[0]:
            actual_info.append("没有找到[PASSED] Compute Result Test: cpu信息")
    else:
        actual_info.append("没有找到[PASSED] Compute Result Test: cpu信息")

    if result_three:
        if "[PASSED] Compute Result Test: cuda" not in result_three[0]:
            actual_info.append("没有找到[PASSED] Compute Result Test: cuda信息")
    else:
        actual_info.append("没有找到[PASSED] Compute Result Test: cuda信息")

    if result_four:
        if "[PASSED] FloatFunctional Test" not in result_four[0]:
            actual_info.append("没有找到[PASSED] FloatFunctional Test信息")
    else:
        actual_info.append("没有找到[PASSED] FloatFunctional Test信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "modules FloatFunctional测试失败"
        expect_info = "Forward Error Test通过,Compute Result Test通过"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"modules FloatFunctional测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result_one:
        assert "[PASSED] Forward Error Test" in result_one[0], "期望屏幕显示[PASSED] Forward Error Test, 实际显示{}".format(result_one)
    else:
        assert False, "期望屏幕显示[PASSED] Forward Error Test, 实际显示{}".format(result_one)
    if result_two:
        assert "[PASSED] Compute Result Test: cpu" in result_two[0], "期望屏幕显示[PASSED] Compute Result Test: cpu, 实际显示{}".format(result_two)
    else:
        assert False, "期望屏幕显示[PASSED] Compute Result Test: cpu, 实际显示{}".format(result_two)
    if result_three:
        assert "[PASSED] Compute Result Test: cuda" in result_three[0], "期望屏幕显示[PASSED] Compute Result Test: cuda, 实际显示{}".format(result_three)
    else:
        assert False, "期望屏幕显示[PASSED] Compute Result Test: cuda, 实际显示{}".format(result_three)
    if result_four:
        assert "[PASSED] FloatFunctional Test" in result_four[0], "期望屏幕显示[PASSED] Compute Result Test: cuda, 实际显示{}".format(result_four)
    else:
        assert False, "期望屏幕显示[PASSED] FloatFunctional Test, 实际显示{}".format(result_four)



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
            actual_info.append("屏幕没有显示[PASSED] Communication Test信息")
    else:
        actual_info.append("屏幕没有显示[PASSED] Communication Test信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "通信接口对齐Pytorch测试失败"
        expect_info = "通信接口对齐Pytorch测试成功，输出PASSED信息"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"通信接口对齐Pytorch测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "[PASSED] Communication Test" in result[0]
    else:
        assert False, "期望显示成功信息'[PASSED] Communication Test', 实际显示{}".format(result)

# @pytest.mark.skip(reason="不想执行")
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
            actual_info.append("在旧版本parrots环境 pat0.13.0rc0下config.yaml已恢复被删除的条目化")
    cf.cd_command(20, 'conda deactivate')
    env_result = cf.check_env(cn["source_envi"])
    cf.cd_command(20, 'python -c "import torch"')
    result = cf.cd_command(20, 'cat .parrots/config.yaml | grep "PARROTS_DEBUG_MODE: None"')
    if result:
        if "PARROTS_DEBUG_MODE: None" not in result:
            actual_info.append("在新版本parrots环境{}下config.yaml没有恢复被删除的条目化".format(env_result))
    flag = "success"
    if len(actual_info) > 0:
        flag = "fail"
        summary = "Parrots 验证环境变量增多后框架能够及时更新本地配置文件增加条目测试失败"
        expect_info = "Parrots 验证环境变量增多后框架能够及时更新本地配置文件增加条目测试成功，在新版本parrots环境{}下config.yaml没有恢复被删除的条目化".format(env_result)
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"Parrots 验证环境变量增多后框架能够及时更新本地配置文件增加条目测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
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
            actual_info.append("屏幕没有显示SUCCESS信息")
    else:
        actual_info.append("屏幕没有显示SUCCESS信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "初始化通信对齐Pytorch测试失败"
        expect_info = "初始化通信对齐Pytorch测试成功，输出SUCCESS信息"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"初始化通信对齐Pytorch测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "SUCCESS" in result[0]
    else:
        assert False, "期望显示成功信息'SUCCESS', 实际显示{}".format(result)


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
            actual_info.append("屏幕没有显示SUCCESS信息")
    else:
        actual_info.append("屏幕没有显示SUCCESS信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "不再提示被捕获的异常产生的log文件的路径信息测试失败"
        expect_info = "不再提示被捕获的异常产生的log文件的路径信息测试成功，输出SUCCESS信息"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"不再提示被捕获的异常产生的log文件的路径信息测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if result:
        assert "SUCCESS" in result[0]
    else:
        assert False, "期望显示成功信息'SUCCESS', 实际显示{}".format(result)


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
            actual_info.append("屏幕没有显示test successfully信息")
    else:
        actual_info.append("屏幕没有显示test successfully信息")
    run_command_two = "srun -p {} --gres=gpu:1 python ddp_twice_used.py  >> /{} 2>&1 &".format(cn["partition"], run_result_file_two)
    cf.run_and_extract_result("n",  run_command_two, 500, "")
    cat_file = "cat /{}".format(run_result_file_two)
    result_two = cf.run_and_extract_result("y",  cat_file, 60, info)
    log.info("result_two is {}".format(result_two))
    actual_info = []
    if result_two:
        if "test successfully" not in result_two[0]:
            actual_info.append("屏幕没有显示test successfully信息")
    else:
        actual_info.append("屏幕没有显示test successfully信息")
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "DDP find_unused_parameters功能测试失败"
        expect_info = "输出test successfully信息"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"DDP find_unused_parameters功能测试", case_name, env_result, flag, [run_result_file, run_result_file_two], gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, "期望显示成功信息'test successfully', 实际显示{}".format(actual_info)

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
            actual_info.append("屏幕没有显示test_conv3d_large_shape PASSED信息")
    else:
        actual_info.append("屏幕没有显示test_conv3d_large_shape PASSED信息")
    actual_info = []
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "conv3d支持大shape输入功能测试失败"
        expect_info = "输出test_conv3d_large_shape PASSED信息"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"conv3d支持大shape输入功能测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, "期望显示成功信息'test_conv3d_large_shape PASSED', 实际显示{}".format(actual_info)

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
            actual_info.append("屏幕没有显示test_randperm PASSED信息")
    else:
        actual_info.append("屏幕没有显示test_randperm PASSED信息")
    actual_info = []
    flag = "success"
    if actual_info:
        flag = "fail"
        summary = "randperm支持cuda11功能测试"
        expect_info = "输出test_randperm PASSED信息"
        description = "分支: {}\n 环境: {}\n 重现步骤: {}\n 期望:  {}\n 实际:  {}\n   备注:{}\n".format(cn["git_clone_command"], env_result, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name), expect_info, actual_info, cn["note"])
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
    csv_list = [u"randperm支持cuda11功能测试", case_name, env_result, flag, run_result_file, gcf.get_dic_three_info("function_file_link.ini", "function_slurm_link", case_name)]
    function_csv_list.append(csv_list)
    if actual_info:
        assert False, "期望显示成功信息'test_randperm PASSED', 实际显示{}".format(actual_info)



# def test_998_csv():
#     log.info("function_csv_list is {}".format(function_csv_list))
#     dlf.connect_vndevice("function")
#     path = "mkdir -p " + "/" + cn["local_path"] + "1102test/csv"
#     cf.cd_command(20, path)
#     with open("/{}1102test/csv/function_test1_{}.csv".format(cn["local_path"], time_stamp), "wb") as p:
#         csv_writer = ucsv.writer(p, encoding='gbk')
#         # csv_writer = csv.writer(p, dialect="excel")
#         try:
#             csv_writer.writerow([u"功能", u"测试用例", u"环境", u"结果", u"结果文件", u"测试用例文档链接", u"issue/备注"])
#         except Exception as e:
#             log.info("Exception is {}".format(e))
#         for i in range(len(function_csv_list)):
#             csv_writer.writerow(function_csv_list[i])
#     cf.cd_command(20, "exit")































if __name__ == '__main__':
    pytest.main(['-s', '-v', '-m "sunny"', 'test_parrots_function.py'])

