import time
import threading

import psutil
from datetime import datetime

INTERVAL_SEC = 1

KEY_LIST = [
    "status",  # 进程状态
    "name",  # 进程名
    "pid",  # 进程号
    # "create_time",  # 进程启动时间
    # "cpu_percent",  # cpu占用率
    # "cpu_times",
    # "username",  # 启动进程的用户
    # "num_threads",  # 线程数量
    "memory_percent",  # 内存使用率
    # "cmdline",  # 启动命令
    # "cpu_affinity"  # 使用了哪些核
]


PROC_LIST = [
    "Taskmgr.exe",
    "芒果TV.exe"
]


def get_pid(pname):
    for proc in psutil.process_iter():  # 迭代windows里所有的进程(psutil.process_iter),遍历查询
        # print(“pid-%d,name:%s” % (proc.pid,proc.name()))
        if proc.name() == pname:
            return proc.pid


def get_proc_info(pid, key_lis):
    """ 记录某个进程的状态 """
    while True:
        pid_obj = psutil.Process(pid)  # 通过某个进程ID获取进程对象
        dic = pid_obj.as_dict(attrs=key_lis)  # 取出进程对象的详细信息
        # 增加CPU占用率，间隔时间1秒捕捉CPU(因为内存一直占用，所以不用间隔获取)
        dic["cpu_percent"] = pid_obj.cpu_percent(interval=1)
        dic['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 监控时间
        print(dic)


def do_monitor():
    proc_ids = []
    for proc_name in PROC_LIST:
        proc_ids.append(get_pid(proc_name))  # 通过进程名把进程ID放入列表中

    for proc_id in proc_ids:
        # 创建独立线程, 因为proc_obj.cpu_percent(interval=1)是阻塞调用
        # 注册线程中需要执行的get_proc_info方法及其参数
        t = threading.Thread(target=get_proc_info, args=(proc_id, KEY_LIST))
        t.start()  # 启动线程
        time.sleep(0.1)  # 临时解决并发输出的脏数据


if __name__ == '__main__':
    do_monitor()
