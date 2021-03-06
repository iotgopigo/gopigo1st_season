#coding: utf-8
from gopigo import *
import time
import logging
#import imageRecognition as im # 画像認識機能

#------------------------------------------------------
# define
#------------------------------------------------------
# 画像サイズ
IMAGE_WIDTH = 640
LOGO_DETECTION  = 'LOGO_DETECTION'
LABEL_DETECTION = 'LABEL_DETECTION'
FACE_DETECTION  = 'FACE_DETECTION'
TEXT_DETECTION  = 'TEXT_DETECTION'
#------------------------------------------------------

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
# -----------------------------------------------
# テスト用					
# -----------------------------------------------
class ImageRecognition:
    def __init__(self):
	self.tmp_num = 0

    def imageRecognition ( self, mode, keyword, rect ):
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

	self.tmp_num = self.tmp_num+1
	if self.tmp_num == 3:
		self.tmp_num = 0
		return keyword

	return "-1"
        if mode == FACE_DETECTION:
            face = [ "JOY", "SORROW" , "ANGER", "SURPRISE", "-1" ]
            expression = face[ random.randint(0,4) ]
            print "face:" + expression
            return expression
        else :
            return keyword
    
im = ImageRecognition()

#def enable_servo():
#        return

#def disable_servo():
#        return

#def servo( position ):
#        return

#def us_dist(pin):
#	return 5
# -----------------------------------------------


# 物体探索機能
def serchObject( mode, keyword ):
	distance = -1			# 距離
	direction = -1			# 方向
	servo_angle = 0			# サーボ角度
	find_flag = False		# 発見フラグ
	rect = []			# 画像認識結果枠(左上x,y,右下x,y)
	cam_param = 60			# 位置と方向の関係

	# サーボ有効化
	enable_servo()
	# サーボを0度にセット
	servo( servo_angle )
	
	# 探索
	while servo_angle <= 180:
		servo( servo_angle )	# サーボをservo_angle度にセット
		time.sleep(0.5)		# 待機
		# 画像認識
		im_ret = im.imageRecognition( mode, keyword, rect )
		# 認識成功ならば探索終了
		if im_ret == keyword:
			find_flag = True
			break
		servo_angle += 20	# 20度回転

	# 探索に成功した場合
	if find_flag == True:
	 	# 角度のセット
		direction = servo_angle
		# 画像中の物体中心位置に修正
		dir_cam = cam_param * ((rect[0] + rect[2])/2.0 - IMAGE_WIDTH/2.0)/(IMAGE_WIDTH/2.0)
		# 修正量のデバッグ出力
		logging.debug('dir_cam: %d', dir_cam)
		direction += dir_cam
		# 範囲制限処理
		if direction < 0:
			direction = 0
		if direction > 180:
			direction = 180
		# 物体中心にサーボ移動
		servo( int(direction) )
		# 超音波センサによる距離測定
		distance = us_dist(15)
		if distance > 300:	#until 3m
			distance = -1
			direction = -1

	# サーボ無効化
	disable_servo()

	# 結果を返す
	ret = [distance, direction]
	return ret


# メイン関数
if __name__ == "__main__":
	ret = serchObject( 'LOGO_DETECTION', 'Panasonic' )

	print 'distance:%d[cm] direction:%d[deg]' % (ret[0], ret[1])
