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
import random       # ランダム
#import speak        # 音声合成機能
import serchObject as serch  # 物体探索機能
#import imageRecognition as im # 画像認識機能
#import audioInput # 音声認識機能
#import movement as mv # 移動機能
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

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

#------------------------------------------------------
# PT用
#------------------------------------------------------
class Speak:
    def speak(self, num):
        text = [
            "Go to campany!",           #
            "Good morning!",            #
            "Sure, I’d be happy to.",   #
            "I’m freaking out.",        #
            "I am sorry to bother you while you are busy. Please put a signature.", #
            "Thank you for putting a signature. Have a nice day, Manager!", #
            "Sorry to keep you wating. I got a signature.", #
            "I’m leaving now. See you tomorrow.", #
            "See you.", #
            "", #
            "Not found!", # 
            "Today is good weather!", #
            "Today is cloudy.", #
            "Today's weather is bad.", #
            "How can I help you?", #
            "I did a good job today!" #
            ]
        if num < 0 or num > 16 :
            print "out of range"
        print "[AudioOutput] " + text[num]
        return
audioOut = Speak()

class Audio_Input:
    def Audio_Input(self, num):
        text = [
            "Please get a Manager's signature",
            "I've done it.",
            "Thank you. See you.",
            "It's working time.",
            "Come on!"
        ]
        if num < 0 or num > 5 :
            print "out of range"
        print "[AudioInput] " + text[num]
        return True
    def Audio_Input_Init(self):
        return

audioIn = Audio_Input()

class Movement:
    def movement(self, direction, speed, distance):
        print "[move] " + "distance:" + str(distance) + ", direction:" + str(direction)
        return 
    def Read_move_status(self):
        return 0
mv = Movement()

class ImageRecognition:
    def imageRecognition( self, mode, keyword, rect ):
        del rect[:]
        rect.append(-1)
        rect.append(-1)
        rect.append(-1)
        rect.append(-1)
        rect[0] = 320
        rect[1] = 240
        rect[2] = 320+160
        rect[3] = 240+120
        print "[ImageRecognition] mode:" + mode + ", keyword:" + keyword
        if mode == FACE_DETECTION:
            face = [ "JOY", "SORROW" , "ANGER", "SURPRISE", "-1" ]
            expression = face[ random.randint(0,4) ]
            print "face:" + expression
            return expression
        else :
            return keyword
im = ImageRecognition()
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
# 音声認識待ち
#------------------------------------------------------
def audioInputWait(num):
    # 認識結果初期化
    audioIn.Audio_Input_Init()
    # 認識待ち
    while 1:
        if audioIn.Audio_Input(num) == True:
            break
        time.sleep(0.1)
    return

#------------------------------------------------------
# 移動待ち
#------------------------------------------------------
def moveWait():
    # 停止するまで監視
    while 1:
        if mv.Read_move_status() == 0:
            break
        time.sleep(0.5) # 0.5秒待ち
 
    return 

#------------------------------------------------------
# 行動1:出社
#------------------------------------------------------
def mode1():
    logging.debug("mode1()")

    #  時間だよと言われるまで待機
    audioInputWait(3)

    # 「出社しまーす」と発話 
    audioOut.speak(0)

    # Panasonicロゴの探索    
    ret = serch.serchObject( LOGO_DETECTION, 'Panasonic' ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 1

    # 回転
    mv.movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    mv.movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    return 2

#------------------------------------------------------
# 行動2:保安所にあいさつ
#------------------------------------------------------
def mode2():
    logging.debug("mode2()")
    
    time.sleep(2) # 2秒待ち

    # 「おはようございます」と発話 
    audioOut.speak(1)    

    # 天気の認識
    rect = []
    label = im.imageRecognition( LABEL_DETECTION, "", rect)   # ラベル認識
    if label == "sun":
        # 「今日はいい天気ですね」と発話 
        audioOut.speak(11)  
    elif label == "clowd":
        # 「今日は曇ってますね」と発話 
        audioOut.speak(12)  
    elif label == "rain":
        # 「今日は残念な天気ですね」と発話 
        audioOut.speak(13)  
    else :
        # 「みつからないよ」と発話 
        audioOut.speak(10)
     
    # 回転
    mv.movement( 90, 1, 0 )
    # 移動待ち
    moveWait()

    return 3

#------------------------------------------------------
# 行動3:仕事の依頼
#------------------------------------------------------
def mode3():
    logging.debug("mode3()")

    time.sleep(2) # 2秒待ち

    # おいでと言われるまで待機
    audioInputWait(4)

    # HELPの探索    
    ret = serch.serchObject( TEXT_DETECTION, "HELP" ) # OCR
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 1

    # 回転
    mv.movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    mv.movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    # 「おはようございます」と発話 
    audioOut.speak(1)    

    # 「なんでしょう？」と発話 
    audioOut.speak(14)    

    # 課長ハンコと言われるまで待機
    audioInputWait(0)

    # 「はい、よろこんで」と発話 
    audioOut.speak(2)    

    return 4

#------------------------------------------------------
# 行動4:課長のところへレッツゴー
#------------------------------------------------------
def mode4():
    logging.debug("mode4()")

    time.sleep(2) # 2秒待ち

    # 課長の探索    
    ret = serch.serchObject( TEXT_DETECTION, "課長" ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 4

    # 回転
    mv.movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    mv.movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    return 5

#------------------------------------------------------
# 行動5:課長の様子を伺う
#------------------------------------------------------
def mode5():
    logging.debug("mode5()")

    time.sleep(2) # 2秒待ち

    # 表情の認識
    rect = []
    label = im.imageRecognition( FACE_DETECTION, "", rect)   # 表情認識

    if label == "ANGER":
        # 「やばい、やばい」と発話 
        audioOut.speak(3)
        # 移動
        mv.movement( 0 , 1, -10 )
        # 移動待ち
        moveWait()
        time.sleep(3) # 3秒待ち
        # 移動
        mv.movement( 0 , 1, 10 )
        # 移動待ち
        moveWait()
        return 5
    elif label == "-1":
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 5
    else :
        return 6

#------------------------------------------------------
# 行動6:課長へお願い
#------------------------------------------------------
def mode6():
    logging.debug("mode6()")

    # 「お忙しい中申し訳ないですが、はんこいただけますか？」と発話 
    audioOut.speak(4)    

    # 終わったよと言われるまで待機
    audioInputWait(1)
    
    # 「ありがとうございます。課長、よい一日を」と発話 
    audioOut.speak(5)    
      
    # 180度回転
    mv.movement( 180, 1, 0 )
    # 移動待ち
    moveWait()
    
    return 7

#------------------------------------------------------
# 行動7:依頼者の席へ戻る
#------------------------------------------------------
def mode7():
    logging.debug("mode7()")

    time.sleep(2) # 2秒待ち
    
    # HELPの探索    
    ret = serch.serchObject( TEXT_DETECTION, "HELP" ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 4

    # 回転
    mv.movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    mv.movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()

    return 8

#------------------------------------------------------
# 行動8:依頼者へ成果物の報告
#------------------------------------------------------
def mode8():
    logging.debug("mode8()")

    time.sleep(2) # 2秒待ち
    
    # 「お待たせ。はんこもらってきたよ～。」と発話 
    audioOut.speak(6)

    # 「ありがとう、バイバイ。」と言われるまで待機
    audioInputWait(2)

    return 9

#------------------------------------------------------
# 行動9:ホームへ戻る
#------------------------------------------------------
def mode9():
    logging.debug("mode9()")
    
    time.sleep(2) # 2秒待ち
    
    # 「今日はもう帰るね～。お先に失礼しま～す。」と発話 
    audioOut.speak(7)

    # Panasonicロゴの探索    
    ret = serch.serchObject( LOGO_DETECTION, 'Panasonic' ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 9

    # 回転
    mv.movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    mv.movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()
    
    # 「さようならー」と発話 
    audioOut.speak(8)

    # -90度回転
    mv.movement( -90, 1, 0 )
    # 移動待ち
    moveWait()

    return 10

#------------------------------------------------------
# 行動10:ホームへ戻る
#------------------------------------------------------
def mode10():
    logging.debug("mode10()")

    # Nationalロゴの探索    
    ret = serch.serchObject( LOGO_DETECTION, 'National' ) # 物体探索
    # 探索に失敗した場合
    if ret[0] == -1:
        # 「みつからないよ」と発話 
        audioOut.speak(10)
        return 10

    # 回転
    mv.movement( ret[1], 1, 0 )
    # 移動待ち
    moveWait()

    # 移動
    mv.movement( 0 , 1, ret[0] )
    # 移動待ち
    moveWait()
    
    # 「今日も、いい仕事したな～」と発話 
    audioOut.speak(15)

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
    mv.movement(0,1,1)

    return

#------------------------------------------------------
# メイン関数
#------------------------------------------------------
def main():
    # 初期モードは1
    mode = 1
    # モード指定がある場合はモードにコマンドライン引数値を設定
    if(len(sys.argv) == 2):
        if int(sys.argv[1]) in range( 1, MODE_MAX+1 ):
            mode = int(sys.argv[1])
        else :
            print "Out of range. sys.argv[1]=" + sys.argv[1]
            return

    # メインスレッド開始
    print " === start main thread (main) === "

    # 行動管理
    actionControl(mode)
    
    # メインスレッド終了
    print " == end main thread === " 

#------------------------------------------------------
# スクリプト実行
#------------------------------------------------------
if __name__ == "__main__":
    main()
