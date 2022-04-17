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

class AutoMakeIssueNA:
    date_expect_to_solve = datetime.datetime.now() + datetime.timedelta(days=1)
    dt = date_expect_to_solve.strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, taskname, summary, description, assignee):
        self.taskname = taskname
        self.summary = summary
        self.description = description
        self.assignee = assignee

    def submit_issue(self, file, labels, components, expect_value='right', username='????',
                     password='???', baseurl='https://jira.???.com',
                     url='/rest/api/2/issue'):
        date_expect_to_solve = datetime.datetime.now() + datetime.timedelta(days=1)
        dt = date_expect_to_solve.strftime("%Y-%m-%d %H:%M:%S")
        # log.info(date_expect_to_solve)
        log.info("components is {}".format(components))
        header = {"Content-Type": "application/json"}
        auth = [username, password]
        summary = "[{}] {}".format(self.taskname, self.summary)
        message = self.description
        json_object = {"fields":
                           {"project": {"key": "???"},
                            "summary": summary,
                            "description": message,
                            "issuetype": {"name": "Bug"},
                            "duedate": dt,
                            "assignee": {"name": "{}".format(self.assignee)},
                            "labels": ["{}".format(labels)],
                            "components": [{"name": components}]
                            }
                       }
        login_session = request.create_session('login_in', baseurl, header, auth=auth)
        addr = request.post_request('login_in', url, data=json_object)
        log.info('addr:%stest' % addr)
        responsedata = request.to_json(addr.content)
        log.info(responsedata)
        issue_key = responsedata.get('key')
        if isinstance(file, list):
            for i in range(len(file)):
                file_op = open(file[i], 'rb')
                files = {'file': file_op}
                log.info(issue_key)
                header2 = {'Accept': 'application/json', 'X-Atlassian-Token': 'no-check'}
                request_attach_file = request.create_session('login_in', baseurl, header2, auth=auth)
                url2 = '/rest/api/2/issue/' + issue_key + '/attachments'
                addr2 = request.post_request('login_in', url2, files=files)
                if addr2 != '<Response [200]>':
                    log.error(addr2.content)
                else:
                    log.info(addr2.content)
        else:
            file_op = open(file, 'rb')
            files = {'file': file_op}
            log.info(issue_key)
            header2 = {'Accept': 'application/json', 'X-Atlassian-Token': 'no-check'}
            request_attach_file = request.create_session('login_in', baseurl, header2, auth=auth)
            url2 = '/rest/api/2/issue/' + issue_key + '/attachments'
            addr2 = request.post_request('login_in', url2, files=files)
            if addr2 != '<Response [200]>':
                log.error(addr2.content)
            else:
                log.info(addr2.content)

    

