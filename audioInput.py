#################################################################
#######                ##########################################
#######  音声認識機能  ##########################################
#######                ##########################################
#################################################################

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time							# 時間
import sys             			 	# システム
import threading        			# スレッド
import xml.etree.ElementTree as ET	# XML用
import subprocess					# サブプロセス


#---------------------------------------------------------------
# socketをインポート
#---------------------------------------------------------------
import socket
host = 'localhost'
port = 10500

#---------------------------------------------------------------
# recv_dataから、キーワードを抜き出すためにキーワード変数を定義(不要？)
#---------------------------------------------------------------
Bunsyo_Keyword1 = u'時間だよ'
Bunsyo_Keyword2 = u'課長'
Bunsyo_Keyword3 = u'押した'
Bunsyo_Keyword4 = u'バイバイ'
Bunsyo_Keyword5 = u'おいで'

#------------------------------------------------------
# 継承元制御スレッドクラス
#------------------------------------------------------
class CtrlThread(threading.Thread):
    # 初期化と開始
    def __init__(self, cycle):
        super(CtrlThread, self).__init__()
        self.stop_event = threading.Event() # 停止させるかのフラグ
        self.cycle = cycle                  # 制御周期の設定
	self.deamon = True
        # スレッドの開始
        print " === start " + self.__class__.__name__ + " === "
        self.start()

    # 停止命令
    def stop(self):
        self.stop_event.set()
        self.join()    # スレッドが停止するのを待つ
        print " === end " + self.__class__.__name__ + " === "

#------------------------------------------------------
# 機能クラス
#------------------------------------------------------
class voiceThread(CtrlThread) :
	# 初期化
        def __init__ ( self, cycle ):
               	self.Audio_Result = 0
#---------------------------------------------------------------
# Juliusに接続(不要)
# GoPiGo経由か、NW経由か
#---------------------------------------------------------------
		self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientsock.connect((host, port))
		print "connect"
#---------------------------------------------------------------
#モジュールモードON (不要)
#---------------------------------------------------------------
                super(voiceThread, self).__init__(cycle)
	 	return
	# 
	def stop(self):
		self.clientsock.shutdown(socket.SHUT_RDWR)
		self.clientsock.close()
		super(voiceThread, self).stop()

        # 実行
        def run( self ):
		command = ''	
		while not self.stop_event.is_set():
#---------------------------------------------------------------
# 取得した音声情報をXMLファイルからrecv_dataとして表示する
#（ただし、ゴミ情報あり）
#---------------------------------------------------------------
			recv_data = self.clientsock.recv(2048)
#---------------------------------------------------------------
# 取得した言語からゴミワードを取り除く
#---------------------------------------------------------------
			sp = recv_data.split('.\n')
		 	for elem in sp:
	  			if(elem != ''):
	   				if elem.find('<SHYPO') != -1 and elem.find('</SHYPO>') == -1:
						elemBuffer = elem
					else:
						if elem.find('<SHYPO') == -1 and elem.find('</SHYPO>') != -1:
							elem = elemBuffer + elem
	      					elemBuffer = ''

		   				try:
		     					root = ET.fromstring(elem)
	     						for word in root.iter('WHYPO'):
	         						command = word.get('WORD')
	         						print(command)
	       							global_order = command
	 					except:
	     						pass
	     						#print("Failed to parse")

#---------------------------------------------------------------
# 取得したキーワードと対応する管理No.を、変数
# Audio_Resultへ代入する
#---------------------------------------------------------------
			if command == Bunsyo_Keyword1 :
   				self.Audio_Result = 1
			elif command == Bunsyo_Keyword2 :
   				self.Audio_Result = 2
			elif command == Bunsyo_Keyword3 :
   				self.Audio_Result = 3
			elif command == Bunsyo_Keyword4 :
   				self.Audio_Result = 4
			elif command == Bunsyo_Keyword5 :
   				self.Audio_Result = 5

		return

# ------------------------------------------
# 関数名：getVoiceRecognitionResult
# 引数：num(1～5が有効値)
# 引数の意味：認識結果がどの番号(num)と一致しているかを確認するため。
# 機能：AudioResultとnumが一致しているか確認し、結果をresに保存。
#      （一致していればTrue、間違っていれば、Falseをresに代入）
#       AudioResultを空にする（0を代入する）。
#       resを戻り値として返す。
#戻り値：res(True or False)
#------------------------------------------
	def getVoiceRecognitionResult(self, num):
		res = False
		if num == self.Audio_Result:
        		res = True
        		self.Audio_Result = 0
    		else:
        		res = False
       	 		self.Audio_Result = 0

		return res

#---------------------------------------------------------------
# ●改善内容
# 誤認識しないように、音声スコアが高いものだけを抜き出せるような
# コートを追加できたらいい！！！！
#---------------------------------------------------------------
# 

if __name__ == "__main__":
        # スレッド生成
        th_voice = voiceThread( 0.05 )
	while th_voice.getVoiceRecognitionResult(4) != True:
		time.sleep(5)

       # スレッドの停止
        th_voice.stop()
