# file: videocaptureasync.py
import threading
import cv2
import os
import time
FILE_OUTPUT = 'output.avi'
cascPath = "resources/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
class VideoCaptureAsync:
	def __init__(self, src=0, width=640, height=480):
		self.src = src
		self.cap = cv2.VideoCapture(self.src)
		fourcc = cv2.VideoWriter_fourcc(*'H264')
		self.out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (640,480))
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
		self.grabbed, self.frame = self.cap.read()
		self.started = False
		self.read_lock = threading.Lock()
		self.j = 0
	def set(self, var1, var2):
		self.cap.set(var1, var2)

	def start(self):
		if self.started:
			print('[!] Asynchroneous video capturing has already been started.')
			return None
		self.started = True
		self.thread = threading.Thread(target=self.update, args=())
		self.threadFace= threading.Thread(target=self.faceDetect, args=())
		
		# ~ self.thread.start()
		self.threadFace.start()
		return self

	def faceDetect(self):
		while self.started:
			ret, pic = self.cap.read()
			gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
		# ~ gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
			i = 0
			print(self.j)
			self.j += 1
			if len(faces) != 0:
				
				filename = "pics/image" + str(i) + ".png"
				i +=1
				cv2.imwrite(filename,pic)
	def update(self):
		while self.started:
			grabbed, frame = self.cap.read()
		    
			with self.read_lock:
				self.grabbed = grabbed
				self.frame = frame
				# ~ self.out.write(frame)

	def read(self):
		with self.read_lock:
		    # ~ frame = 
		    # ~ frame = cv2.flip(self.frame.copy(),0)
			frame = self.frame.copy()
			self.out.write(frame)
			# ~ gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# ~ faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
			# ~ if faces is not None:
				
		    # ~ grabbed = self.grabbed
		return None, frame

	def stop(self):
		self.started = False
		# ~ self.thread.join()
		# ~ self.threadFace.join()

	def __exit__(self, exec_type, exc_value, traceback):
		self.cap.release()
		self.out.release()
