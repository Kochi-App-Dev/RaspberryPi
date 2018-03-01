# coding: UTF-8
import RPi.GPIO as GPIO
import time
import subprocess
from subprocess import Popen
import datetime
import argparse
import subprocess

####### 定数 #######
GPIO_SW_1 = 6
GPIO_SW_2 = 13
GPIO_SW_3 = 19
GPIO_SW_BLUE = 26

GPIO_LED_1 = 25
GPIO_LED_2 = 8
GPIO_LED_3 = 7

GPIO_LED_TOWER_RED = 16
GPIO_LED_TOWER_YELLOW = 20
GPIO_LED_TOWER_GREEN = 21


####### イベントデータ #######
eventList = []
def readEventData():
	# eventデータ取得
	fp = open('./event.txt')
	global eventList
	eventList = fp.readlines()
	fp.close()
	#print (eventList)

def eventBeforeDays(days, sound):
	data = getIndexByFuture(days)
	if len(data) <= 0:
		print('eventBeforeDays:' + str(days) + ' no data')
		return 0
	startMP3(sound)
	say = data[1] + data[2]
	#print ("say:" + say)
	startSayProcess(say)
	return 1
	
def startSayProcess(say):
	cmd = "./say " + say
	#proc = Popen( cmd,shell=True )
	proc = subprocess.call(cmd, shell=True )
	#print( "process id = %s" % proc.pid )
	

def startTalkProcess():
    cmd = "./p3.py"
    #proc = Popen( cmd,shell=True )
    proc = subprocess.call(cmd, shell=True )
    #print( "process id = %s" % proc.pid )
    


def startMP3(file):
	cmd = "aplay " + file
	proc = Popen( cmd,shell=True )
	#proc = subprocess.call(cmd, shell=True)
	print( "process id = %s" % proc.pid )

	
def convertDate(str):
	return datetime.datetime.strptime(str, "%Y%m%d%H%M")

# 現在日時よりdays後の直近の流星群配列インデックスを返す
def getIndexByFuture(days):
	
	now = datetime.datetime.now()		# 現在日時
	for line in eventList:
#		print(line)
		data = line.split(",")
		if (days < 0):
			return data
		
		eventDD = convertDate(data[0])
		sa = (eventDD-now).days
		if (sa <= days and sa >= 0):
			return data
		
	return []

####### 処理メイン #######
iC0 = 0											# now process
count = 0
parser = argparse.ArgumentParser(description="Receive stock codes, a start date, and an end date")
parser.add_argument("-g",
					"--gpio",
					nargs="?",
					type=str,
					default="",
					help=u"GPIOを使用する場合は-gを付けて起動",
					dest="use_gpio"
					)

parser.add_argument("-s",
					"--sample",
					nargs="?",
					type=str,
					default="",
					help=u"テスト再生する場合は-sを付けて起動",
					dest="use_sample"
					)
useGPIO = parser.parse_args().use_gpio
useSample = parser.parse_args().use_sample


readEventData()


if useSample == "on":
	startMP3('music/01.wav')
	iC0 = GPIO_SW_3
	eventBeforeDays(-1, 'onepoint/3.wav')
	time.sleep(5.01)

try:
	if useGPIO == "on":
		print "starting GPIO"
		####### GPIO設定 #######
		GPIO.setmode(GPIO.BCM) # GPIO番号で指定
		GPIO.setup(GPIO_SW_1, GPIO.IN)					# event before 1 week
		GPIO.setup(GPIO_SW_2, GPIO.IN)					# event before 1 day
		GPIO.setup(GPIO_SW_3, GPIO.IN)					# event is today
		GPIO.setup(GPIO_SW_BLUE, GPIO.IN)				# input voice
		GPIO.setup(GPIO_LED_1, GPIO.OUT)
		GPIO.setup(GPIO_LED_2, GPIO.OUT)
		GPIO.setup(GPIO_LED_3, GPIO.OUT)
		GPIO.setup(GPIO_LED_TOWER_RED, GPIO.OUT)
		GPIO.setup(GPIO_LED_TOWER_YELLOW, GPIO.OUT)
		GPIO.setup(GPIO_LED_TOWER_GREEN, GPIO.OUT)

		GPIO.output(GPIO_LED_1, 0)      # 1 week led off
		GPIO.output(GPIO_LED_2, 0)      # 1 day led on
		GPIO.output(GPIO_LED_3, 0)      # today led off
		GPIO.output(GPIO_LED_TOWER_GREEN, 0)		# status ok
		GPIO.output(GPIO_LED_TOWER_RED, 0)
		GPIO.output(GPIO_LED_TOWER_YELLOW, 0)
		while True:
			# check a input
			sw1 = GPIO.input(GPIO_SW_1)
			sw2 = GPIO.input(GPIO_SW_2)
			sw3 = GPIO.input(GPIO_SW_3)
			swBlue = GPIO.input(GPIO_SW_BLUE)
			if sw1 == 0:
				if iC0 == 0:
					iC0 = GPIO_SW_1
					GPIO.output(GPIO_LED_1, 1)		# 1 week led on
					GPIO.output(GPIO_LED_2, 0)		# 1 day led off
					GPIO.output(GPIO_LED_3, 0)		# today led off
					GPIO.output(GPIO_LED_TOWER_GREEN, 1)
					GPIO.output(GPIO_LED_TOWER_YELLOW, 0)
					GPIO.output(GPIO_LED_TOWER_RED, 0)
					eventBeforeDays(7, 'onepoint/1.wav')
					iC0 = 0
			elif sw2 == 0:
				if iC0 == 0:
					iC0 = GPIO_SW_2
					GPIO.output(GPIO_LED_1, 0)		# 1 week led off
					GPIO.output(GPIO_LED_2, 1)		# 1 day led on
					GPIO.output(GPIO_LED_3, 0)		# today led off
					GPIO.output(GPIO_LED_TOWER_GREEN, 0)
					GPIO.output(GPIO_LED_TOWER_YELLOW, 1)
					GPIO.output(GPIO_LED_TOWER_RED, 0)

					eventBeforeDays(1, 'onepoint/2.wav')
					iC0 = 0
			elif sw3 == 0:
				if iC0 == 0:
					data = getIndexByFuture(0)
					if len(data) > 0:
						startMP3('music/01.wav')
						iC0 = GPIO_SW_3
						GPIO.output(GPIO_LED_1, 0)		# 1 week led off
						GPIO.output(GPIO_LED_2, 0)		# 1 day led off
						GPIO.output(GPIO_LED_3, 1)		# today led on
						GPIO.output(GPIO_LED_TOWER_GREEN, 0)
						GPIO.output(GPIO_LED_TOWER_YELLOW, 0)
						GPIO.output(GPIO_LED_TOWER_RED, 1)

						eventBeforeDays(0, 'onepoint/3.wav')
						iC0 = 0
			elif swBlue == 0:
				if iC0 == 0:
					iC0 = GPIO_SW_BLUE
					startTalkProcess()
					iC0 = 0

			time.sleep(0.01)
			count = count + 1
			if count % 50 == 0:
#				print iC0
				count = 0
#			else:
#				print iC0,
				print (iC0)

		GPIO.output(GPIO_LED_TOWER_GREEN, 0)		# status off
		GPIO.output(GPIO_LED_1, 0)					# 1 week led off
		GPIO.output(GPIO_LED_2, 0)					# 1 day led off
		GPIO.output(GPIO_LED_3, 0)					# today led off
		GPIO.cleanup() # <- 消灯
	else:
		print "starting check"
		eventT = eventBeforeDays(7, 'onepoint/3.wav')
		if (eventT == 0):
			event1 = eventBeforeDays(1, 'onepoint/2.wav')
			if (event1 == 0):
				event7 = eventBeforeDays(7, 'onepoint/1.wav')
		
except KeyboardInterrupt:
	pass


