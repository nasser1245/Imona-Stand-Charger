import threading
import cv2
import os
from datetime import datetime
import shutil
import time
from DBIntract import DBIntract

'''
class to intract with camera to capture videos and take picture from 
user faces for future unplanned conditions and improve security
for instance when finger does not detected.
'''
class imageVideoThread:
	# initialize video frame and open cv
	def __init__(self, src=0, width= 640, height= 480):
		self.src = src
		# initialize video capture object
		self.cap = cv2.VideoCapture(self.src)
		self.outvid = None
		self.db = DBIntract(checkSameThread=False)
		# ~ self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		# ~ self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
		# ~ self.grabbed, self.frame = self.cap.read()
		
		# haar pattern for face recognition from pics 
		cascPath = "res/haarcascade_frontalface_default.xml"
		# initialize face recognition classifier with cascade pattern
		self.faceCascade = cv2.CascadeClassifier(cascPath)
		self.lock = False
		self.vidCreateFilePass = True
		self.vidStartTime = None
		self.vidEndTime = None
		self.vidPath = None
		self.recordingState = False
		self.startFrame = 0
		self.startTime = 0
		self.endFrame = 0
		self.vidCreateFilePass = True
		self.frameNum = 0
		self.sigExit = False
		self.fileList = []
		# create and start video thread for capture video while programs runs with method captureVideo()
		self.threadVid = threading.Thread(target=self.captureVideo, args=(width,height))
		self.threadVid.start()
		# create image thread for take pictures from user faces with method captureImage()
		self.threadImg = threading.Thread(target=self.captureImage, args=())
		
	def set(self, var1, var2):
		self.cap.set(var1, var2)

    # start recording of user video and capture from his face			
	def recordStart(self):
		self.recordingState = True
		self.threadImg.start()
		self.startFrame = self.frameNum
		self.startTime = datetime.now()

	# stop recording 
	def recordStop(self, shelfNum, socketType, strFinger, inOut):
		# recording end frame
		self.endFrame = self.frameNum
		if self.fileList == []:
			return "NO FACE"
		self.db.insertUse(self.vidPath,self.startFrame, self.endFrame,
		self.startTime, datetime.now(), self.fileList, shelfNum, socketType,
		strFinger, inOut)
		self.startFrame = 0
		self.startTime = 0
		self.endFrame = 0
		self.fileList = []
		self.recordingState = False
		return "Success"
	# capture video in entire time program runs in seperate thread
	def captureVideo(self, width, height):
		while True and not self.sigExit:
			# in first time video file creates, below condition executes
			if self.vidCreateFilePass == True:
				# ~ initialize video file
				
				self.vidStartTime = datetime.now()
				# unique video file name with date time values
				self.vidPath = "res/vid/"+str(self.vidStartTime)[:19]+".avi"
				self.frameNum = 0
				print ("Video Address: ", self.vidPath)
				# compressed h264 video format with 20.0 fps
				fourcc = cv2.VideoWriter_fourcc(*'H264')
				frames = 20.0
				self.outvid = cv2.VideoWriter(self.vidPath, fourcc, frames, (width,height))
				self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
				self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
				self.db.insertVideo(self.vidPath)
				# ~ delete old video and image files if disk have limited space (below than 3 GigaBytes)
				total, used, free = shutil.disk_usage("/")
				if (free // ( 2**30)) < 3:
					# get old videos and images to fulsh them from memory to free up space
					# with removeOldeVidAndImg() method in DBIntract class
					files = self.db.removeOldVidAndImg()
					os.remove(files[0])
					for i in files[1]:
						os.remove(i)
				# set vidCreateFilePass to false to ignore this section in future loops
				self.vidCreateFilePass = False
			# self.lock member variable thread as a semaphor for camera resource
			# to ensure that this resource was not occupies with other thread 
			# (image capture or video capture thread)
			while self.lock == True:
				pass
			self.lock = True
			ret, frame = self.cap.read()
			
			self.lock = False
			if ret == True:
				frame = cv2.flip(frame,0)
				# write frame to end of video
				self.outvid.write(frame)
				self.frameNum += 1
			endTime = datetime.now()
			diff = endTime-self.vidStartTime
			# ~ checks length of the video if exceeds 24 hour closes video and create new video file
			if diff.days == 1 and self.recordingState == False:
				self.vidCreateFilePass = True
				self.db.closeVideo(self.vidPath)
				self.outvid.release()
				
	#capture image and save if face detects
	def captureImage(self):
		numDetected = 0
		self.fileList = []
		# max 6 detected face captures
		while numDetected < 6 and self.recordingState == True:
			while self.lock == True:
				pass
			self.lock = True
			ret, pic = self.cap.read()
			self.lock = False
			# convert image to grayscale
			gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
			# face detector with sensivity 1.2 
			faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.2,
			minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
			#cv2.imshow('frame',gray)
			
			# if face detect store it
			if len(faces) != 0:
				print('Face Detects')
				fileName = ("res/pic/" + str(datetime.now())[:22] +
				"_"+str(numDetected+1)+ ".png")
				cv2.imwrite(fileName,pic)
				# append picture to file list for store in db
				self.fileList.append(fileName)
				numDetected += 1
			# sleep 1 second, hope gestures change in this time!
			time.sleep(1)
		
			
	def __del__(self):
		# ~ print("this lines executes")
		self.cap.release()
		self.outvid.release()
		self.db.closeVideo(self.vidPath)
		cv2.destroyAllWindows()
		
