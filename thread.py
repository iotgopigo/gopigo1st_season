#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------
# インポート
#------------------------------------------------------
import threading    # スレッド
import time         # 時間処理
import datetime     # 日時取得
import sys          # システム
#------------------------------------------------------

#------------------------------------------------------
# パラメータ
#------------------------------------------------------
MOTOR_CTRL_CYCLE        = 0.2 # モータ制御周期[s]
IMAGE_PROCESSING_CYCLE  = 1.0 # 画像処理周期[s]
MODE_MAX                = 7   # モードの最大数[0〜MODE_MAX]
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
# モータ制御スレッドクラス
#------------------------------------------------------
class MotorCtrlThread(CtrlThread):
    # 初期化
    def __init__(self, cycle):
        super(MotorCtrlThread, self).__init__(cycle)
        self.__leftReferenceSpeed  = 0  # 最初は停止
        self.__rightReferenceSpeed = 0  # 最初は停止
    
    # 処理
    def run(self):
        while not self.stop_event.is_set():
            time.sleep(self.cycle)
            print "sub thread ("+ self.__class__.__name__ +") : " + str(datetime.datetime.today())
            print "leftReferenceSpeed:" + str(self.__leftReferenceSpeed) 
            print "rightReferenceSpeed:" + str(self.__rightReferenceSpeed)
    
    # 目標速度の設定
    def setSpeed(self, leftReferenceSpeed, rightReferenceSpeed):
        self.__leftReferenceSpeed  = leftReferenceSpeed   # 
        self.__rightReferenceSpeed = rightReferenceSpeed  #

#------------------------------------------------------
# 画像処理スレッドクラス
#------------------------------------------------------
class ImageProcessingThread(CtrlThread):
    # 処理
    def run(self):
        while not self.stop_event.is_set():
            time.sleep(self.cycle)
            print "sub thread ("+ self.__class__.__name__ +") : " + str(datetime.datetime.today())


#------------------------------------------------------
# メイン関数 
#------------------------------------------------------
if __name__ == '__main__':

    # モードを0に
    mode = 0
    if(len(sys.argv) == 2):
        if int(sys.argv[1]) in range(MODE_MAX+1):
            mode = int(sys.argv[1])

    print "モード:" + str(mode)

    # モータ制御スレッド生成
    th_motorCtrl = MotorCtrlThread(MOTOR_CTRL_CYCLE)
    # 画像処理スレッド生成
    th_imageProcessing = ImageProcessingThread(IMAGE_PROCESSING_CYCLE)
    
    # メインスレッド
    print " === start main thread (main) === "
    for i in range(5):
        time.sleep(1)
        print "main thread : " + str(datetime.datetime.today())
        th_motorCtrl.setSpeed(i,i) # 目標速度の変更
    print " == end main thread === " 
    
    # 画像処理スレッドの停止
    th_imageProcessing.stop() 
    # モータ制御スレッドの停止
    th_motorCtrl.stop() 
