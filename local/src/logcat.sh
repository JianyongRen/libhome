#!/bin/sh

save_log_file=1
log_file=$HOME/logs/logcat-`date +%Y%m%d%H%M%S`.txt

for var in $*
do
	if [ "$var" == "-c" ];then
		save_log_file=0
	elif [ "$var" == "-f" ];then
		save_log_file=0
	fi
done

if [ $save_log_file -eq 1 ];then
	adb logcat $* 2>&1 | tee $log_file
	#if [ ${PIPESTATUS[0]} -ne 0 ];then
	#	rm $log_file
	#fi
else
	adb logcat $*
fi

