#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------
# インポート
#------------------------------------------------------
import threading    # スレッド
import time         # 時間処理
import datetime     # 日時取得
import sys          # システム
import logging      # ログ取得
#------------------------------------------------------

#------------------------------------------------------
# パラメータ
#------------------------------------------------------
MODE_MAX                = 9   # モードの最大数[1〜MODE_MAX]
#------------------------------------------------------

#------------------------------------------------------
# 継承元制御スレッドクラス
#------------------------------------------------------
class CtrlThread(threading.Thread):
    # 初期化と開始
    def __init__(self, cycle):
        super(CtrlThread, self).__init__()
        self.stop_event = threading.Event() # 停止させるかのフラグ
        self.cycle = cycle                  # 制御周期の設定
        # スレッドの開始
        print " === start " + self.__class__.__name__ + " === "
        self.start()

    # 停止命令
    def stop(self):
        self.stop_event.set()
        self.join()    # スレッドが停止するのを待つ
        print " === end " + self.__class__.__name__ + " === "

#------------------------------------------------------
# 行動1:出社
#------------------------------------------------------
def mode1():
    # おはようと言われるまで待機
    while 1:
        if Audio_Input(1) == 1:
            break
    # 「いってきまーす」と発話 
    speak(0)
    
    return 2

#------------------------------------------------------
# 行動2:
#------------------------------------------------------
def mode2():
    return 3

#------------------------------------------------------
# 行動3:
#------------------------------------------------------
def mode3():
    return 4

#------------------------------------------------------
# 行動4:
#------------------------------------------------------
def mode4():
    return 5

#------------------------------------------------------
# 行動5:
#------------------------------------------------------
def mode5():
    return 6

#------------------------------------------------------
# 行動6:
#------------------------------------------------------
def mode6():
    return 7

#------------------------------------------------------
# 行動7:
#------------------------------------------------------
def mode7():
    return 8

#------------------------------------------------------
# 行動8:
#------------------------------------------------------
def mode8():
    return 9

#------------------------------------------------------
# 行動9:
#------------------------------------------------------
def mode9():
    return 10

#------------------------------------------------------
# 行動管理機能
#------------------------------------------------------
def actionControl( mode ):
    # 行動が終了するまでループ
    while mode < MODE_MAX+1:
        if mode == 1:
            mode = mode1() # 行動1:出社
        else if mode == 2:
            mode = mode2() # 行動2:保安所にあいさつ
        else if mode == 3:
            mode = mode3() # 行動3:仕事の依頼   
        else if mode == 4:
            mode = mode4() # 行動4:課長のところへレッツゴー   
        else if mode == 5:
            mode = mode5() # 行動5:課長の様子を伺う   
        else if mode == 6:
            mode = mode6() # 行動6:課長へお願い   
        else if mode == 7:
            mode = mode7() # 行動7:依頼者の席へ戻る   
        else if mode == 8:
            mode = mode8() # 行動8:依頼者へ成果物の報告     
        else if mode == 9:
            mode = mode9() # 行動9:ホームへ戻る 

    return

#------------------------------------------------------
# メイン関数
#------------------------------------------------------
if __name__ == "__main__":

    # 初期モードは1
    mode = 1
    # モード指定がある場合はモードにコマンドライン引数値を設定
    if(len(sys.argv) == 2):
        if int(sys.argv[1]) in range(1,MODE_MAX):
            mode = int(sys.argv[1])

    # メインスレッド開始
    print " === start main thread (main) === "

    # 行動管理        
	actionControl(mode)

    # メインスレッド終了
    print " == end main thread === " 