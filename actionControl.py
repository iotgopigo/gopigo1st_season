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
#import speak        # 音声合成機能
import serchObject  # 物体探索機能
#------------------------------------------------------

#------------------------------------------------------
# パラメータ
#------------------------------------------------------
MODE_MAX                = 10   # モードの最大数[1〜MODE_MAX]
#------------------------------------------------------
#------------------------------------------------------
# define
#------------------------------------------------------
LOGO_DETECTION  = 'LOGO_DETECTION'
LABEL_DETECTION = 'LABEL_DETECTION'
FACE_DETECTION  = 'FACE_DETECTION'
TEXT_DETECTION  = 'TEXT_DETECTION'


#------------------------------------------------------


#------------------------------------------------------
# PT用
#------------------------------------------------------
def speak(num):

    text = {
            "Go to Campany!",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            }
    
    if num < 1 || num > 16 :
        print "out of range"

    print text[num]
    
    return
def Audio_Input(num):
    return 1
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
# 移動待ち
#------------------------------------------------------
def moveWait():
    # 停止するまで監視
    while 1:
        if Read_move_status() == 0:
            break
        time.sleep(0.5) # 0.5秒待ち
 
    return 

#------------------------------------------------------
# 行動1:出社
#------------------------------------------------------
def mode1():
    # おはようと言われるまで待機
    while 1:
        if Audio_Input(1) == 1:
            break
    # 「出社しまーす」と発話 
    speak(0)

    # Panasonicロゴの探索    
    ret = serchObject( LOGO_DETECTION, 'Panasonic' ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        speak(10)
        return 1

    # 回転
    movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    return 2

#------------------------------------------------------
# 行動2:保安所にあいさつ
#------------------------------------------------------
def mode2():

    time.sleep(2) # 2秒待ち

    # 「おはようございます」と発話 
    speak(1)    

    # 天気の認識
    rect = []
    label = imageRecognition( LABEL_DETECTION, "", rect)   # ラベル認識
    if label == "sun"
        # 「今日はいい天気ですね」と発話 
        speak(11)  
    elif label == "clowd"
        # 「今日は曇ってますね」と発話 
        speak(12)  
    elif label == "rain"
        # 「今日は残念な天気ですね」と発話 
        speak(13)  
    else
        # 「みつからないよ」と発話 
        speak(10)
     
    # 回転
    movement( 90, 1, 0 )
    # 移動待ち
    moveWait()

    return 3

#------------------------------------------------------
# 行動3:仕事の依頼
#------------------------------------------------------
def mode3():
    
    time.sleep(2) # 2秒待ち

    # おいでと言われるまで待機
    while 1:
        if Audio_Input(2) == 2:
            break

    # HELPの探索    
    ret = serchObject( TEXT_DETECTION, "HELP" ) # OCR
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        speak(10)
        return 1

    # 回転
    movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    # 「おはようございます」と発話 
    speak(1)    

    # 「なんでしょう？」と発話 
    speak(14)    

    # 課長ハンコと言われるまで待機
    while 1:
        if Audio_Input(3) == 3:
            break

    # 「はい、よろこんで」と発話 
    speak(2)    


    return 4

#------------------------------------------------------
# 行動4:課長のところへレッツゴー
#------------------------------------------------------
def mode4():
    time.sleep(2) # 2秒待ち

    # 課長の探索    
    ret = serchObject( TEXT_DETECTION, "課長" ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        speak(10)
        return 4

    # 回転
    movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    return 5

#------------------------------------------------------
# 行動5:課長の様子を伺う
#------------------------------------------------------
def mode5():
    time.sleep(2) # 2秒待ち

    # 表情の認識
    rect = []
    label = imageRecognition( FACE_DETECTION, "", rect)   # 表情認識

    if label == "anger"
        # 「やばい、やばい」と発話 
        speak(3)
        # 移動
        movement( 0 , 1, -10 )
        # 移動待ち
        moveWait()
        time.sleep(3) # 3秒待ち
        # 移動
        movement( 0 , 1, 10 )
        # 移動待ち
        moveWait()
    elif label == "-1":
        # 「みつからないよ」と発話 
        speak(10)
        return 5
    else
        return 6

#------------------------------------------------------
# 行動6:課長へお願い
#------------------------------------------------------
def mode6():

    # 「お忙しい中申し訳ないですが、はんこいただけますか？」と発話 
    speak(4)    

    # 終わったよと言われるまで待機
    while 1:
        if Audio_Input(2) == 2:
            break
    
    # 「ありがとうございます。課長、よい一日を」と発話 
    speak(5)    
      
    # 180度回転
    movement( 180, 1, 0 )
    # 移動待ち
    moveWait()
    
    return 7

#------------------------------------------------------
# 行動7:依頼者の席へ戻る
#------------------------------------------------------
def mode7():
    time.sleep(2) # 2秒待ち
    
    # HELPの探索    
    ret = serchObject( TEXT_DETECTION, "HELP" ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        speak(10)
        return 4

    # 回転
    movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    return 8

#------------------------------------------------------
# 行動8:依頼者へ成果物の報告
#------------------------------------------------------
def mode8():

    time.sleep(2) # 2秒待ち
    
    # 「お待たせ。はんこもらってきたよ～。」と発話 
    speak(6)

    # 「ありがとう、バイバイ。」と言われるまで待機
    while 1:
        if Audio_Input(3) == 3:
            break

    return 9

#------------------------------------------------------
# 行動9:ホームへ戻る
#------------------------------------------------------
def mode9():
    
    time.sleep(2) # 2秒待ち
    
    # 「今日はもう帰るね～。お先に失礼しま～す。」と発話 
    speak(7)

    # Panasonicロゴの探索    
    ret = serchObject( LOGO_DETECTION, 'Panasonic' ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        speak(10)
        return 9

    # 回転
    movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()
    
    # 「さようならー」と発話 
    speak(16)

    # -90度回転
    movement( -90, 1, 0 )
    # 移動待ち
    moveWait()

    
    return 10

#------------------------------------------------------
# 行動10:ホームへ戻る
#------------------------------------------------------
def mode10():

    # Nationalロゴの探索    
    ret = serchObject( LOGO_DETECTION, 'National' ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        speak(10)
        return 10

    # 回転
    movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()
    
    # 「今日も、いい仕事したな～」と発話 
    speak(15)

    return 11

#------------------------------------------------------
# 行動管理機能
#------------------------------------------------------
def actionControl( mode ):
    # 行動が終了するまでループ
    while mode < MODE_MAX+1:
        if mode == 1:
            mode = mode1()  # 行動1:出社
        elif mode == 2:
            mode = mode2()  # 行動2:保安所にあいさつ
        elif mode == 3:
            mode = mode3()  # 行動3:仕事の依頼   
        elif mode == 4:
            mode = mode4()  # 行動4:課長のところへレッツゴー   
        elif mode == 5:
            mode = mode5()  # 行動5:課長の様子を伺う   
        elif mode == 6:
            mode = mode6()  # 行動6:課長へお願い   
        elif mode == 7:
            mode = mode7()  # 行動7:依頼者の席へ戻る   
        elif mode == 8:
            mode = mode8()  # 行動8:依頼者へ成果物の報告     
        elif mode == 9:
            mode = mode9()  # 行動9:保安所に帰りの挨拶 
        elif mode == 10:
            mode = mode10() # 行動10:ホームへ戻る 

    # 停止命令
    movement(0,1,1)

    return

#------------------------------------------------------
# メイン関数
#------------------------------------------------------
if __name__ == "__main__":

    # 初期モードは1
    mode = 1
    # モード指定がある場合はモードにコマンドライン引数値を設定
    if(len(sys.argv) == 2):
        if int(sys.argv[1]) in range( 1, MODE_MAX ):
            mode = int(sys.argv[1])

    # メインスレッド開始
    print " === start main thread (main) === "

    # 行動管理
    actionControl(mode)
    
    # メインスレッド終了
    print " == end main thread === " 
