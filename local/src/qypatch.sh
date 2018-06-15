#!/bin/sh

src=$1
dst=$2

cur_path=`pwd`

if [ "${src}" == "" ];then
	echo "Error: no patch dir given!"
	exit 1
fi

if [ "${dst}" == "" ];then
	dst=.
fi

if [ "${src:0:1}" != "/" ];then
	src=${cur_path}/$src
fi
if [ "${dst:0:1}" != "/" ];then
	dst=${cur_path}/$dst
fi

if [ ! -d ${dst}/thirdparty-libs ];then
	echo "Error: ${dst}/thirdparty-libs is not exists or not dir!"
	exit 1
fi

if [ ! -d ${src}/include ];then
	if [ -d ${src}/android_armeabi/include ];then
		src=${src}/android_armeabi
	else
		echo "Error: ${src}/include is not exists or not dir!"
		exit 1
	fi
fi

cp -rf ${src}/include/*.h  ${dst}/thirdparty-libs/include/pumaplayer/puma/
cp -rf ${src}/include/cupid/*.h  ${dst}/thirdparty-libs/include/pumaplayer/cupid/
cp -rf ${src}/include/live_controller/*.h  ${dst}/thirdparty-libs/include/pumaplayer/live_controller

cp -rf ${src}/*.{so,dat,crt} ${dst}/thirdparty-libs/libs/android/puma_tv/shared/armeabi/
cp -rf ${src}/*.jar ${dst}/thirdparty-libs/libs/android/puma_tv/jar/

pushd ${dst}/thirdparty-libs/libs/android/puma_tv/shared/armeabi/
mv libffmpeg-armv6-vfp.so libmcto_ffmpeg-armv6-vfp.so
mv libffmpeg-armv7-neon.so libmcto_ffmpeg-armv7-neon.so
popd

pushd ${dst}/thirdparty-libs
git status -s | while read line
do
	arr=($line)
	if [ "${arr[0]}" == "M" ];then
		if [ "${arr[1]:0-3}" == ".so" ];then
			echo "cp -f ${arr[1]} ${dst}/tvplayer/libs/armeabi/"
			cp -f ${arr[1]} ${dst}/tvplayer/libs/armeabi/
		elif [ "${arr[1]:0-4}" == ".jar" ];then
			echo "cp -f ${arr[1]} ${dst}/tvplayer/libs/"
			cp -f ${arr[1]} ${dst}/tvplayer/libs/
		fi
	fi
done
popd


