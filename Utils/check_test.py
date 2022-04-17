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
from Utils.implement_op import Implement, CommonFunction


log = logging.getLogger(__name__)
request = RequestsLibrary.RequestsLibrary()
connect = ssh()
gcf = GetConfigInfo()
time_stamp = str(eval(gcf.get_dic_two_info("/connect_file.ini", "time_stamp")["time_stamp"]))

class ThroughIndicators:
    
    def check_result(self, pwd, base_path, case_name, frame, model, check_info, type=None, pa_info=None):
        log.info("check model result")
        jira_file = "/" + pwd + base_path + case_name + "/parrots.test/jira/{}_jira{}".format(frame, time_stamp)
        model_file = "/" + pwd + base_path + case_name + "/log_file/" + frame + "_" + model
        log.info("{} model_file is {}".format(model, model_file))
        result = self.get_train_result(check_info, model_file)
        log .info("result is {}".format(result))
        end_result = "success"
        if type == "speed":
            jira_file = "/" + pwd + base_path + case_name + "/parrots.test/jira/{}_jira{}".format(case_name, time_stamp)
            speed_yuzhi = gcf.get_dic_three_info(pa_info[0], pa_info[1], model.lower())
            yuzhi_env = gcf.get_dic_three_info(pa_info[2], pa_info[3], "{}_{}".format(frame.lower(), pa_info[4]))
            end_result = self.compare_result("speed", result[0], speed_yuzhi, frame, model, pa_info[5], pa_info[6])
            end_list = frame + " " + model + " " + pa_info[7] + " " + yuzhi_env + " " + speed_yuzhi + " " + str(result) + " " + end_result + " " + model_file + " " + pa_info[1]
        else:
            end_list = frame + " " + model + " " + str(result) + " " + model_file
        all_result_model = "/" + pwd + base_path + case_name + "/parrots.test/all_result_model{}".format(time_stamp)
        log.info("all_result_model is {}".format(all_result_model))
        delete = "sed -i '/" + frame + " " + model + " " + "\[" + "/d' " + all_result_model
        log.info("delete is {}".format(delete))
        CommonFunction().input(delete)
        all_result_model_info = CommonFunction().input("wc -l {}".format(all_result_model)).replace(all_result_model, " ")
        log.info("all_result_model_info is {}".format(all_result_model_info))
        if "0" in all_result_model_info[0] or "No such file or directory" in all_result_model_info:
            export_sh = "echo  '{}' > {}".format(end_list, all_result_model)
        else:
            export_sh = "sed -i '$a " + end_list + "'" + " " + all_result_model
        log.info("export_sh is {}".format(export_sh))
        CommonFunction().input(export_sh)
        if "null" in result[0] or end_result == "fail":
            delete_jira = "sed -i '/" + frame + " " + model + " " + "\[" + "/d' " + jira_file
            log.info("delete_jira is {}".format(delete_jira))
            CommonFunction().input(delete_jira)
            jira_file_info = CommonFunction().input("wc -l {}".format(jira_file)).replace(jira_file, " ")
            log.info("jira_file_info is {}".format(jira_file_info))
            if "0" in jira_file_info[0] or "No such file or directory" in jira_file_info:
                export_sh = "echo  '{}' > {}".format(end_list, jira_file)
            else:
                export_sh = "sed -i '$a " + end_list + "'" + " " + jira_file
            log.info("export_sh is {}".format(export_sh))
            CommonFunction().input(export_sh)
            assert False
        

    def accuracy_info_re(self, model_name, log_file_info):
        sign = gcf.get_dic_three_split_info(model_name.lower(), "/accuracy_sign_info.ini", "accuracy_sign_re", ",")
        log.info("sign is {}".format(sign))
        accuracy_list = []
        for i in range(len(sign)):
            key_re = sign[i]                  # key_re = "{}:\s\d+[.]\d+".format(sign[i])
            log.info("key_re is {}".format(key_re))
            key_sign = gcf.get_dic_three_split_info(model_name.lower(), "/accuracy_sign_info.ini", "accuracy_sign_info", ",")
            p = re.compile(r"{}".format(key_re))
            file_info = CommonFunction().input("tail -n300 {} | grep '{}'".format(log_file_info, key_sign[i]))
            accuracy = re.findall(p, file_info.replace("[01;31m[K", "").replace("", "").replace("[m[K", "").replace("[01;31m", "").replace('"', ""))
            log.info("accuracy is {}".format(accuracy))
            if accuracy:
                accuracy_info = accuracy[-1].split(":")[-1].strip(" ").split(" ")[0]
                log.info("accuracy_info is {}".format(accuracy_info))
            else:
                accuracy_info = "null"
            accuracy_list.append(accuracy_info)
        log.info("accuracy_list is {}".format(accuracy_list))
        time.sleep(20)
        return accuracy_list
    

    def speed_info_re(self, log_file_info):
        avg_commad = "cat {} | grep 'benchmark_avg_iter_time'".format(log_file_info)
        avg_log_file_info = CommonFunction().input(avg_commad)
        if avg_log_file_info:
            avg_p = re.compile(r"benchmark_avg_iter_time.*(\d+[.]\d+)")
            avg_speed_result = re.findall(avg_p, avg_log_file_info)
            log.info("speed is {}".format(avg_speed_result))
            if avg_speed_result:
                speed_value = avg_speed_result[0]
            else:
                speed_value = "null"
        else:
            speed_value = "null"
        return speed_value


    def alloc_info_re(self, log_file_info):
        alloc_run_command = "cat {} |grep 'benchmark_mem_alloc'".format(log_file_info)
        alloc_log_file_info = CommonFunction().input(alloc_run_command)
        log.info("alloc_log_file_info is {}".format(alloc_log_file_info))
        if alloc_log_file_info:
            alloc_p = re.compile(r"benchmark_mem_alloc.*[0-9]\d{1,50}")
            alloc_speed_result_0 = re.findall(alloc_p, alloc_log_file_info)
            if alloc_speed_result_0:
                alloc_speed_result = re.findall(r"\d+", alloc_speed_result_0[0])
                if alloc_speed_result:
                    alloc_value = alloc_speed_result[0]
                else:
                    alloc_value = "null"
            else:
                alloc_value = "null"
        else:
            alloc_value = "null"
        return alloc_value


    def total_time_info_re(self, log_file_info):
        total_run_command = "cat {} |grep 'benchmark_total_time'".format(log_file_info)
        total_log_file_info = CommonFunction().input(total_run_command)
        log.info("total_time_log_file_info is {}".format(total_log_file_info))
        if total_log_file_info:
            total_p = re.compile("benchmark_total_time.*(\d+\d+[.]\d+)|(\d+[.]\d+)")
            total_speed_result = re.findall(total_p, total_log_file_info)
            if total_speed_result:
                total_time_list = total_speed_result[0]
                total_time_list_value = list(filter(lambda x: any(x), total_time_list))
                if total_time_list_value:
                    total_time = total_time_list_value[0]
                else:
                    total_time = "null"
            else:
                total_time = "null"
        else:
            total_time = "null"
        return total_time

    def cached_info_re(self, log_file_info):
        cached_run_command = "cat {} |grep 'benchmark_mem_cached'".format(log_file_info)
        cached_log_file_info = CommonFunction().input(cached_run_command)
        log.info("cached_log_file_info is {}".format(cached_log_file_info))
        if cached_log_file_info:
            cached_p = re.compile(r"benchmark_mem_cached.*[0-9]\d{1,50}")
            cached_speed_result_0 = re.findall(cached_p, cached_log_file_info)
            if cached_speed_result_0:
                cached_speed_result = re.findall(r"\d+", cached_speed_result_0[0])
                if cached_speed_result:
                    cached_value = cached_speed_result[0]
                else:
                    cached_value = "null"
            else:
                cached_value = "null"
        else:
            cached_value = "null"
        return cached_value

    def pure_training_time_info_re(self, log_file_info):
        pure_training_run_command = "cat {} |grep 'benchmark_pure_training_time'".format(log_file_info)
        pure_training_log_file_info = CommonFunction().input(pure_training_run_command)
        log.info("pure_training_time_log_file_info is {}".format(pure_training_log_file_info))
        if pure_training_log_file_info:
            pure_training_p = re.compile(r"benchmark_pure_training_time.*(\d+\d+[.]\d+)|(\d+[.]\d+)")
            pure_training_speed_result = re.findall(pure_training_p, pure_training_log_file_info)
            if pure_training_speed_result:
                pure_training_time_list = pure_training_speed_result[0]
                pure_training_time_list_value = list(filter(lambda x: any(x), pure_training_time_list))
                if pure_training_time_list_value:
                    pure_training_time = pure_training_time_list_value[0]
                else:
                    pure_training_time = "null"
            else:
                pure_training_time = "null"
        else:
            pure_training_time = "null"
        return pure_training_time


    def compare_result(self, type, train_result, train_yuzhi, frame, model, actual_info_list, summary_list):
        flag = "success"
        if type == "speed":
            if "null" not in train_result:
                if float(train_result) > float(train_yuzhi):
                    actual_info_list.append("{}框架{}模型速度{} > {}".format(frame, model, train_result, train_yuzhi))
                    summary_list.append("速度 ")
                    flag = "fail"
            else:
                actual_info_list.append("没有找到{}框架{}模型的速度".format(frame, model))
                summary_list.append("速度 ")
                flag = "fail"
            
        elif type == "alloc":
            if "null" not in train_result:
                if float(train_result) > float(train_yuzhi):
                    actual_info_list.append("{}框架{}模型显存{} > {}".format(frame, model, train_result, train_yuzhi))
                    summary_list.append("显存 ")
            else:
                actual_info_list.append("没有找到{}框架{}模型的显存".format(frame, model))
                summary_list.append("显存 ")
        elif type == "total_time":
            if "null" not in train_result:
                log.info("total_time_result is {}".format(train_result))
                if float(train_result) > float(train_yuzhi):
                    actual_info_list.append("{}框架{}模型总时间{} > {}".format(frame, model, train_result, train_yuzhi))
                    summary_list.append("总时间 ")
            else:
                actual_info_list.append("没有找到{}框架{}模型的总时间".format(frame, model))
                summary_list.append("总时间 ")
        return flag

    def get_train_result(self, args, file):
        train_result_list = []
        if "speed" in args:
            speed = self.speed_info_re(file)
            train_result_list.append(speed)
        if "alloc" in args:
            alloc = self.alloc_info_re(file)
            train_result_list.append(alloc)
        if "cached" in args:
            cached = self.cached_info_re(file)
            train_result_list.append(cached)
        if "pure_training_time" in args:
            pure_training_time = self.pure_training_time_info_re(file)
            train_result_list.append(pure_training_time)
        if "total_time" in args:
            total_time = self.total_time_info_re(file)
            train_result_list.append(total_time)
        return train_result_list

       
