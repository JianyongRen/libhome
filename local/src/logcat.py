#!/usr/bin/python2
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

_proc = None
_file_obj = None

def _log_file():
    if platform.system() == "Windows":
        return ("C:\Users\\renjianyong\Documents\logs\logcat-%s.txt" %
                (time.strftime("%Y%m%d%H%M%S", time.localtime())))
    else:
        return ("/cygdrive/c/Users/renjianyong/Documents/logs/logcat-%s.txt" %
                (time.strftime("%Y%m%d%H%M%S", time.localtime())))

def _run_cmd(cmd):
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

    if proc.returncode is not 0:
        print("\nError: run \"%s\" failed with returncode(%d)!" % (cmd, proc.returncode))
    return proc.returncode


def _run_logcat(cmd):
    _run_cmd('%s | Tee-Object -FilePath %s' % (cmd, _log_file()))

'''
捕获Ctrl+C
'''
def handler(signal_num,frame):
    print("\nYou Pressed Ctrl-C.")
    if _proc is not None:
        _proc.terminate()
        #_proc.wait()
        #time.sleep(1)

    '''
    if _file_obj is not None:
        _file_obj.close()
    '''

def _main(argv):
    del argv[0]
    signal.signal(signal.SIGINT, handler)
    cmd = ["adb", "logcat"]
    #print(argv)
    for var in argv:
        if var == "-c":
            return _run_cmd(' '.join(cmd + argv))

    _run_logcat(' '.join(cmd + argv))

if __name__=='__main__':
    _main(sys.argv)

