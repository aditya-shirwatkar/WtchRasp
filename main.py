import RPi.GPIO as g
from time import time, sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from picamera import PiCamera
cred = credentials.Certificate('/home/pi/pkrpi.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://evilwatchdog.firebaseio.com/',
    'storageBucket': 'evilwatchdog.appspot.com'
})

ref = db.reference('direction')
ref_logs = db.reference('logs').child('log_images')
bucket = storage.bucket()
camera = PiCamera()
def click_pic():
	t = int(time()*1000)
	ref_logs.update({str(t):'1'})
	camera.capture(str(t)+'.jpeg')
	blob = bucket.blob('logs/'+str(t)+'.jpeg')
	blob.upload_from_filename(str(t)+'.jpeg')
	print('Image Uploaded')
US_T = 1
US_E = 2
M_1 = 26
M_2 = 13
M_3 = 5
M_4 = 11
PIR = 7
g.setmode(g.BCM)
g.setup(US_T, g.OUT)
g.setup(US_E, g.IN)
g.setup(M_1, g.OUT)
g.setup(M_2, g.OUT)
g.setup(M_3, g.OUT)
g.setup(M_4, g.OUT)
g.setup(PIR, g.IN)
def getDistance():
	g.output(US_T, 1)
	sleep(0.001)
	g.output(US_T, 0)
	st = time()
	et = time()
	while g.input(US_E) == 0:
		st = time()
	while g.input(US_E) == 1:
		et = time()
	td = et-st
	d = 343*td/20
	return d

def dir1():
	g.output(M_1, 1)
	g.output(M_2, 0)
	g.output(M_3, 0)
	g.output(M_4, 1)
def dir2():
	g.output(M_1, 1)
	g.output(M_2, 0)
	g.output(M_3, 1)
	g.output(M_4, 0)
def dir3():
	g.output(M_1, 0)
	g.output(M_2, 1)
	g.output(M_3, 0)
	g.output(M_4, 1)
def dir4():
	g.output(M_1, 0)
	g.output(M_2, 1)
	g.output(M_3, 1)
	g.output(M_4, 0)
def stop():
	g.output(M_1, 0)
	g.output(M_2, 0)
	g.output(M_3, 0)
	g.output(M_4, 0)
def move(direction):
	if direction == 'r':
		dir_()
	if direction == 'l':
		dir_()
	if direction == 'f':
		dir_()
	if direction == 'b':
		dir_()
	if direction == 's':
		stop()
dir1()
while True:
	click_pic()
	sleep(10)
#	if getDistance()<10:
#		dir_#()
#	else:
#		dir_#()
#	print(ref.get())
