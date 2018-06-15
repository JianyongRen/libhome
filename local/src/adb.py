#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import re
import signal
import time
import traceback
import platform

def match_ip(ip):
    if ip == None:
        return False
    #pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])(|:\d*)$')
    pattern = re.compile(r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)(|:\d+)$')
    ret = pattern.match(ip)
    if ret == None:
        return False
    else:
        return True

def match_ip_part(ip):
    pattern = re.compile('^(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)$')
    ret = pattern.match(ip)
    if ret == None:
        return False
    else:
        return True

def get_savefile():
    if platform.system() == "Windows":
        path = os.environ.get("APPDATA")
        return path + "\\adb_ip.txt"
    elif platform.system().startswith("CYGWIN_NT"):
        path = os.environ.get("APPDATA")
        print("path: " + path)
        return path + "\\adb_ip.txt"
    elif platform.system() == "Linux":
        path = os.path.expanduser('~')
        return path + "/.adb_ip.txt"
    else:
        path = os.path.expanduser('~')
        return path + "/.adb_ip.txt"

def get_saveip():
    adb_file = get_savefile()
    #print("adb file: %s" % (adb_file))
    if os.path.exists(adb_file) == False:
        return None

    f = open(adb_file,"r")
    try:
        lines = f.readlines()
        for l in lines:
            if match_ip(l):
                return l
    finally:
        f.close()

    return None

def set_saveip(ip):
    adb_file = get_savefile()
    f = open(adb_file,"w")
    try:
        f.write(ip)
    finally:
        f.close()

def replace_ip(ip_port, ip):
    #print("replace_ip(%s, %s)" % (ip_port,ip))
    strinfo = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    new_ip = strinfo.sub(ip, ip_port)
    if match_ip(new_ip):
        return new_ip
    else:
        return None

def replace_ip_last_part(ip_port, last):
    strinfo = re.compile('\d+:')
    new_ip = strinfo.sub(last+":", ip_port)
    if match_ip(new_ip):
        return new_ip
    else:
        return None

def recombine_ip(ip, saved_ip):
    #print("ip:%s, saved_ip:%s" % (ip, saved_ip))
    if ip == None:
        if match_ip(saved_ip):
            return saved_ip
        else:
            return None
    if (match_ip(ip) or match_ip_part(ip)) == False:
        print("IP地址不合法！")
        return None
    if ip.find(":") != -1:
        return ip
    if saved_ip == None:
        if ip.find(".") != -1:
            return ip + ":5555"
        else:
            print("IP地址不完整！")
            return None
    if match_ip_part(ip):
        return replace_ip_last_part(saved_ip, ip)
    else:
        return replace_ip(saved_ip, ip)

def get_inputip(saved_ip):
    str_input = None
    patern = re.compile('^\d+$')
    while True:
        str_input = input("请输入机顶盒IP：")
        str_input = str_input.strip()
        if str_input in ("q","exit","quit"):
            sys.exit(0)
        ip = recombine_ip(str_input, saved_ip)
        if ip != None:
            print("ip: %s" % ip)
            return ip
        else:
            print("    IP 地址不合法！")

def _run_cmd(cmd, cwd=None, timeout=0):
    proc = subprocess.Popen(cmd, shell=True, cwd=cwd)
    if timeout <= 0:
        proc.wait()
    else:
        wait_time = 0.0
        while proc.poll() is None and wait_time < timeout:
            time.sleep(0.2)
            wait_time += wait_time

    if proc.returncode is not 0:
        print("\nError: run \"%s\" failed with returncode(%d)!" % (cmd, proc.returncode))
    return proc.returncode

def run_adb(ip, adb_cmd, timeout=0):
    cmd = None
    if ip != None:
        cmd = "adb -s %s %s" % (ip, adb_cmd)
    else:
        cmd = "adb " + adb_cmd
    print(cmd)
    _run_cmd(cmd, timeout=timeout)


def connect(saved_ip, ip):
    #print("connect(%s, %s)" % (saved_ip,ip))
    '''
    if ip != None and match_ip(ip) == False:
        print("    IP 地址不合法！")
        ip = get_inputip(saved_ip)
    '''
    if saved_ip != None:
        run_adb(saved_ip, "disconnect")

    ip = recombine_ip(ip, saved_ip)
    if ip == None:
        ip = get_inputip(saved_ip)

    if ip != saved_ip:
        set_saveip(ip)
    cmd = "adb connect %s" % ip
    print(cmd)
    _run_cmd(cmd, timeout=5)

'''
捕获Ctrl+C
'''
def handler(signal_num,frame):
    print("\nYou Pressed Ctrl-C.")
    sys.exit(signal_num)

def main(argc, argv):

    signal.signal(signal.SIGINT, handler)

    '''
    for i in range(0,argc):
        print("参数[%d]：%s" % (i,argv[i]))
    '''
    if argc == 1:
        _run_cmd("adb")
        return

    saved_ip = get_saveip()
    #print("saved_ip: %s" % saved_ip)

    if argv[1] == "co" or argv[1] == "connect":
        if argc == 3:
            connect(saved_ip, argv[2])
        else:
            connect(saved_ip, None)
        return
    elif saved_ip == None:
        connect(None, None)
        saved_ip = get_saveip()

    if argv[1] == "re" or argv[1] == "remount":
        run_adb(saved_ip, "remount", 5)
    elif argv[1] == "reboot":
        run_adb(saved_ip, "shell sync", 5)
        time.sleep(2)
        run_adb(saved_ip, "reboot", 5)
    elif argv[1] in ("root"):
        cmd = ""
        for i in range(1,argc):
            cmd = cmd + " " + argv[i]
        run_adb(saved_ip, cmd, 5)
    elif argv[1] == "find":
        cmd = "shell busybox"
        for i in range(1, argc):
            cmd = cmd + " " + argv[i]
        run_adb(saved_ip, cmd)
    else:
        cmd = ""
        for i in range(1, argc):
            cmd = cmd + " " + argv[i]
        run_adb(saved_ip, cmd)

if __name__=='__main__':
    main(len(sys.argv), sys.argv)

