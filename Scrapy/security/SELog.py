# coding=utf-8

import logging
import os

class FunLog(object):

    def fun(self):
        """
            @Auth: Jay-Z
            @Desc: 用于记录程序执行中的log信息，显示在控制台，并保存在当前路径的log1文件夹,如果当前路径已经存在，则log2,log3,log4...

        """
        #控制创建log文件夹
        count = 1
        flagLog = True

        # 创建一个logger
        logger = logging.getLogger()
        # Log等级总开关
        logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
#        while flagLog:
#            if os.path.exists("./log"+str(count)):
#                count+=1
#            else:
#                os.makedirs("./log"+str(count))
#                flagLog = False
#
#        logfile = "./log"+str(count)+"/logger.txt"
        logfile = "./log1/logger.txt"
        fh = logging.FileHandler(logfile, mode='a+')
        # 输出到file的log等级的开关
        fh.setLevel(logging.DEBUG)   

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # 输出到console的log等级的开关
        ch.setLevel(logging.INFO)   

        # 定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 第五步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger


if __name__ == "__main__":

    logger = FunLog().fun()
    # 日志
    logger.debug('this is a logger debug message')
    logger.info('this is a logger info message')
    logger.warning('this is a logger warning message')
    logger.error('this is a logger error message')
    logger.critical('this is a logger critical message')
