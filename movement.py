#!/usr/bin/env python
# coding: utf-8


#------------------------------------------------------
# インポート
#------------------------------------------------------  
import time	    	# 時間処理 
import logging      	# ログ
import sys          	# システム   
import threading    	# スレッド 
from gopigo import * 	# GoPiGo

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

#------------------------------------------------------
# パラメータ
#------------------------------------------------------
CHECK_MOVE_CYCLE 	= 0.2 		# 状態確認周期[s]
WHEEL_DIAMETER    	= 6.5		# タイヤ直径[cm]
VEHICLE_WIDTH 		= 12.0		# 車体幅[cm]
PULSE_PER_ROLL 		= 18		# 1回転辺りのパルス数[pulse]

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
# 移動機能クラス
#------------------------------------------------------
class movementThread(CtrlThread) :	

	# 初期化
	def __init__ ( self, cycle ):
		super(movementThread, self).__init__(cycle)
		enable_encoders()
		self.speed 	= 2		# 速度設定
 		self.direction 	= 0		# 方向[度]
		self.distance 	= 0		# 距離[cm]
		self.move_flag 	= False  	# 移動状態
		return

	# 実行
	def run( self ):
		while not self.stop_event.is_set():
			if read_enc_status() == 0: 
				self.move_flag = False

			time.sleep( self.cycle )
		return 	
	
	# 速度の設定
	def setSpeed ( self, speed ):
		print "speed:" + str(speed)
		# 入力エラー処理
		# 速度
		if speed < 0:
			return 0
		if speed > 3:
			return 0

		# 指定速度が0であれば停止
		if speed == 0:
			self.move_stop()
		
		self.speed = speed
		
		if self.speed == 1:
			# モータに速度設定
			set_speed( 50 )
		elif self.speed == 2:
			# モータに速度設定
			set_speed( 100 )
		elif self.speed == 3:
			# モータに速度設定
			set_speed( 200 )
		
		return 1

	# 回転
	def rotation( self, direction, speed ):
		
		# 入力エラー処理
		# 角度
		if direction < -180:
			return 0
		if direction > 180:
			return 0
		
		# 速度の設定
		if self.setSpeed( speed ) == 0:
			return 0

		# 停止中であれば設定有効
		if self.read_move_status() == False:
			self.direction = direction
			# パルス数の計算
           		pulse = int( (float(abs(direction)) / 360.0 * VEHICLE_WIDTH/WHEEL_DIAMETER) * PULSE_PER_ROLL * 1.1)
			print "rotation pulse:"+str(pulse)
			# ロータリーエンコーダの目標パルス数設定
			enc_tgt( 1, 1, pulse )
			
			# 角度がマイナスの場合
			if self.direction < 0:
				left_rot()	# 左信地回転
			else :
				right_rot()	# 右信地回転

			self.move_flag = True
		return 1

	# 移動
	def movement( self, distance, speed ):
		# 入力エラー処理
		# 距離
		if distance < -100:
			return 0
		if distance > 100:
			return 0

		# 速度の設定
		if self.setSpeed( speed ) == 0:
			return 0

		# 停止中であれば設定有効
		if self.read_move_status() == False:
			self.distance = distance
			# パルス数の計算
			pulse = int(float(abs(distance)) / (WHEEL_DIAMETER*3.1415926) * PULSE_PER_ROLL)*2
			
			print "movement pulse:"+str(pulse)
			# ロータリーエンコーダの目標パルス数設定
			enc_tgt( 1, 1, pulse )

			# 距離がマイナスの場合
			if self.distance < 0:
				bwd()	# 前進
			else :
				fwd()	# 後退
			
			self.move_flag = True
		return 1
	
	# 停止
	def move_stop( self ):
		stop()
		self.move_flag = False
		return

	# 移動状態の読み込み
 	def read_move_status( self ):
		return self.move_flag

	# 速度設定の読み込み
	def read_speed_status( self ):
		return self.speed


#------------------------------------------------------
# function
#------------------------------------------------------
# メイン関数
if __name__ == "__main__":

	# 移動機能スレッド生成
    	th_move = movementThread( CHECK_MOVE_CYCLE )
	
	th_move.rotation(90, 2)
	while th_move.read_move_status():
		time.sleep(0.5)
	time.sleep(1)

	th_move.movement(30, 2)
	while th_move.read_move_status():
		time.sleep(0.5)
	time.sleep(1)
	
	th_move.rotation(-90, 2)
	while th_move.read_move_status():
		time.sleep(0.5)
	time.sleep(1)

	th_move.movement(-30, 2)
	while th_move.read_move_status():
		time.sleep(0.5)
	time.sleep(1)

	th_move.move_stop()

	# 移動機能スレッドの停止
    	th_move.stop() 
