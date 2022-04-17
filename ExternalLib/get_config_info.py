import logging

from ExternalLib import read_config

rd = read_config.ReadConfig()
log = logging.getLogger(__name__)


class GetConfigInfo:

    @staticmethod
    def get_dic_two_info(init_file, title):
        cn_info = rd.read_ini_config(init_file, title)
        return cn_info

    @staticmethod
    def get_two_result(init_file, title, frame_name):
        cn_info = rd.read_ini_config(init_file, title,)
        result = cn_info[frame_name].split(",")
        log.info("result is {}".format(result))
        num = result[0]
        wait_time = result[1]
        return num, wait_time

    @staticmethod
    def get_dic_three_info(init_file, title, model_name):
        cn_info = rd.read_ini_config(init_file, title)
        return cn_info[model_name]

    @staticmethod
    def get_dic_three_split_info(model_name, init_file, title, split_symbol):
        cn_info = rd.read_ini_config(init_file, title)
        cn_info = cn_info[model_name].split(split_symbol)
        return cn_info

    @staticmethod
    def get_dic_three_split_list_info(init_file, frame_name, split_symbol):
        cn_info = rd.read_ini_config(init_file, frame_name)
        result = list(cn_info.values())
        log.info("result is {}".format(result))
        cn_info_end = []
        for i in range(len(result)):
            end_result = result[i].split(split_symbol)
            cn_info_end.append(end_result)
        return cn_info_end




    
if __name__ == "__main__":
    s = GetConfigInfo()
    