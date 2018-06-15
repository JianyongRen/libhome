#!/bin/sh

cmd=$1

git_list=(
ssh://git@gitlab.qiyi.domain:10022/vr_player/qyuniutil.git
ssh://git@gitlab.qiyi.domain:10022/vr_player/qyuniutil-pub.git
ssh://git@gitlab.qiyi.domain:10022/vr_player/thirdparty-libs.git
ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvplayer.git
ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvplayerapi.git
ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvplayerutils.git
ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvuniplayersdk.git
ssh://git@gitlab.qiyi.domain:10022/iddplayer/tvuniplayersdk-jni.git
ssh://git@gitlab.qiyi.domain:10022/vr_player/unibuild.git
ssh://git@gitlab.qiyi.domain:10022/iddplayer/uniplayerdata-pub.git
ssh://git@gitlab.qiyi.domain:10022/vr_player/uniplayersdk.git
ssh://git@gitlab.qiyi.domain:10022/vr_player/uniplayersdk-pub.git
)

if [ "${cmd}" == "clone" ];then
	for var in ${git_list[@]};
	do
		dir_name=${var##*/}
		dir_name=${dir_name%\.git}
		if [ ! -d ${dir_name}/.git ];then
			echo "git clone ${var}"
			if [ "${dir_name}" == "unibuild" ];then
				git clone $var -b TV
			else
				git clone $var -b TV8.5
			fi
		fi
	done
elif [ "${cmd}" == "forall" ] && [ "$2" != "" ];then
	for file in ./*;
	do
		if [ -d ${file}/.git ];then
			pushd ${file}
			sh $2
			popd
		fi
	done
fi

