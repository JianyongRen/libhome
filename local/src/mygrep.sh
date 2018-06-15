#!/bin/sh

#echo "grep --include=*.{h,c,cpp,java,cfg,xml,groovy} -rn $*"
grep --include=*.{h,c,cpp,java,cfg,xml,groovy,js} -rn $* .

#echo "grep --exclude={tags,*.so,*.o,*.a,*.class,*.dex,*.lib} --exclude-dir={.svn,.git,.repo} -rn $* ."
#grep --exclude={tags,*.so,*.o,*.a,*.class,*.dex} --exclude-dir={.svn,.git,.repo} -rn $* .

