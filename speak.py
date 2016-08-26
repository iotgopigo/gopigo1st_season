#coding: utf-8
import subprocess
from datetime import datetime
import sys

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/usr/local/dic']
    htsvoice=['-m','/usr/share/hts-voice/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t)
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)
    wr.wait()


def speak(number):
#if構文をここにいれます。
	if number==0:
 		jtalk('出社しまぁす')
	elif number==1:
 		jtalk('おはようございます。')
	elif number==2:
 		jtalk('はい。よろこんで')
 	elif number==3:
 		jtalk('やばいやばい')
	elif number==4:
 		jtalk('お忙しいなか申し訳ないですが、はんこいただけますか')
 	elif number==5:
 		jtalk('ありがとうございます。課長、良い一日を')
	elif number==6:
 		jtalk('お待たせ。はんこもらってきたよぉ')
	elif number==7:
 		jtalk('今日はもう帰るねぇ。お先に失礼しまぁす')
	elif number==8:
 		jtalk('今日も、いい仕事したな～。')
	elif number==9:
 		jtalk('なんでしょう？')
	elif number==10:
 		jtalk('みつからないよ。')
	elif number==11:
 		jtalk('今日はいい天気ですね')
	elif number==12:
 		jtalk('今日は曇ってますね')
	elif number==13:
 		jtalk('今日は残念な天気ですね')
	elif number==14:
 		jtalk('さようなら')
	elif number==15:
 		jtalk('')

	elif number==20:
 		jtalk('僕に用事？')
	else:
 		return


if __name__ == '__main__':
	speak(int(sys.argv[1]))
