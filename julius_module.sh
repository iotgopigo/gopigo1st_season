#!/bin/bash

iconv -f utf8 -t eucjp ./dic/voiceList.yomi | ~/dev/julius-kits/dictation-kit-v4.3.1-linux/bin/yomi2voca.pl > ./dic/voiceList.dic

#julius -C ~/dev/julius-kits/dictation-kit-v4.3.1-linux/main.jconf -C ~/dev/julius-kits/dictation-kit-v4.3.1-linux/am-gmm.jconf -nostrip -module
julius -C ./dic/voiceList.jconf -nostrip -module
