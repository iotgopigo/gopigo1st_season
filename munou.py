#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
from janome.tokenizer import Tokenizer


def think(inStr):
    if inStr == u"おはよう":
        outStr = u"おはよう"
    elif inStr == u"ただいま":
        outStr = u"おかえり"
    else :
        outStr = u"訳が分からないよ";
    return outStr

if __name__ == '__main__':
    import random, sys, os
    
    t = Tokenizer()

    # 元にする文章の読み込み
    filename = "sample_test.txt"
    input_txt = open(filename, "r").read()

    # ユニコード文字列を渡す必要がある
    inString = unicode(input_txt,"utf-8")
    
    # わかち書きした単語をリストに格納する
    wordlist = t.tokenize(inString)

    # マルコフ連鎖テーブルの作成
    markov = {}
    pw = "" # pw - previous word, cw - current word
    for cw in wordlist:
        if pw:
            if markov.has_key(pw):
                lst = markov[pw]
            else:
                lst = []

            lst.append(cw.surface)
            markov[pw] = lst
        pw = cw.surface

    # マルコフ連鎖で文章作成
    words = t.tokenize(unicode(sys.argv[1],"utf-8"))
    for word in words:
        print word
    selectword = words[0].surface
    sentence = ""
    count = 0
    while count < 5:
        sentence += selectword
        if markov.has_key(selectword) == False:
            break
        selectword = random.choice(markov[selectword])
        count += 1

    if count == 5:
        print sentence

    for test in markov[selectword]
        print test 
