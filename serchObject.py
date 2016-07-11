#coding: utf-8
#from gopigo import *
import time
import logging
#import imageRecognition

# 画像サイズ
IMAGE_WIDTH = 640

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
# -----------------------------------------------
# テスト用					
# -----------------------------------------------
def imageRecognition ( mode, keyword, rect ):
	rect.clear()
	rect.append(-1)
	rect.append(-1)
	rect.append(-1)
	rect.append(-1)
	rect[0] = 0
	rect[1] = 0
	rect[2] = 320
	rect[3] = 240

	return keyword

def enable_servo():
        return

def disable_servo():
        return

def servo( position ):
        return

def us_dist(pin):
	return 5
# -----------------------------------------------


# 物体探索機能
def serchObject( mode, keyword ):
	dist = -1				# 距離
	dir = -1				# 方向
	servo_angle = 0			# サーボ角度
	find_flag = False		# 発見フラグ
	rect = []				# 画像認識結果枠(左上x,y,右下x,y)
	cam_param = 0.1			# 位置と方向の関係

	# サーボ有効化
	enable_servo()
	# サーボを0度にセット
	servo( servo_angle )
	
	# 探索
	while servo_angle < 180:
		servo( servo_angle )	# サーボをservo_angle度にセット
		time.sleep(0.5)			# 待機
		# 画像認識
		im_ret = imageRecognition( mode, keyword, rect )
		# 認識成功ならば探索終了
		if im_ret == True:
			find_flag = True
			break
		servo_angle += 30	# 30度回転

	# 探索に成功した場合
	if find_flag == True:
	 	# 角度のセット
		dir = servo_angle
		# 画像中の物体中心位置に修正
		dir_cam = cam_param * ((rect[0] + rect[2]) / 2 - IMAGE_WIDTH/2)
		# 修正量のデバッグ出力
		logging.debug('dir_cam: %d', dir_cam)
		dir += dir_cam
		# 範囲制限処理
		if dir < 0:
			dir = 0
		if dir > 180:
			dir = 180
		# 物体中心にサーボ移動
		servo(servo)
		# 超音波センサによる距離測定
		dist = us_dist(15)

	# サーボ無効化
	disable_servo()

	# 結果を返す
	ret = [dist, dir]
	return ret


# メイン関数
if __name__ == "__main__":
	ret = serchObject( 'LOGO_DETECTION', 'Panasonic' )

	print 'dist:%d[deg] direction:%d[cm]' % (ret[0], ret[1])
