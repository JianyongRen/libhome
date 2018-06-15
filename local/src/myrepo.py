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

git_list = [
        'ssh://git@gitlab.qiyi.domain:10022/vr_player/qyuniutil.git',
        'ssh://git@gitlab.qiyi.domain:10022/vr_player/qyuniutil-pub.git',
        'ssh://git@gitlab.qiyi.domain:10022/vr_player/thirdparty-libs.git',
        'ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvplayer.git',
        'ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvplayerapi.git',
        'ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvplayerutils.git',
        'ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvuniplayersdk.git',
        'ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvuniplayersdk-jni.git',
        'ssh://git@gitlab.qiyi.domain:10022/vr_player/unibuild.git',
        'ssh://git@gitlab.qiyi.domain:10022/iddplayer/uniplayerdata-pub.git',
        'ssh://git@gitlab.qiyi.domain:10022/vr_player/uniplayersdk.git',
        'ssh://git@gitlab.qiyi.domain:10022/vr_player/uniplayersdk-pub.git'
        ]

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

