'''
The main file consists of window classes 
'''

import tkinter as tk
import arabic_reshaper
from bidi.algorithm import get_display
from pyfingerprint.pyfingerprint import PyFingerprint
from imageVideoThread import imageVideoThread
from DBIntract import DBIntract
import time
# instantiate object class to communicate with sqlite db
db = DBIntract()

#Create imageVideoThread to capture video on start program (and take picture after face recogniton)
imgVid = imageVideoThread()
fnt = "XB Shiraz"
ANDROID = "1"
IPHONE = "2"
TYPE_C = "3"
NOKIA  = "4"

'''
Main window class
''' 
class mainWindow:
	# intiate main window frame, background, buttons and properties 
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.master.configure(background='#3F2AB1')
		self.master.title("Charger V0.1")
		#self.master.attributes("-fullscreen",True)
		self.frame.configure(background='#3F2AB1')
		# button with click event to showSocket window for both phone charge and recieve phone buttons
		bidi_text = get_display(arabic_reshaper.reshape(u'شارژ گوشی'))
		self.socketButton = tk.Button(self.frame,text=bidi_text, command=self.showSocket)
		self.socketButton.configure(background = '#32AF3E',  font = (fnt,40))
		self.socketButton.pack()
		
		bidi_text = get_display(arabic_reshaper.reshape(u'دریافت گوشی'))
		self.socketButton = tk.Button(self.frame,text=bidi_text, command=self.showSocket)
		self.socketButton.configure(background = '#AF323E',  font = (fnt,40))
		self.socketButton.pack()
		
		bidi_text = get_display(arabic_reshaper.reshape(u'بخش مدیریت'))
		self.manageButton = tk.Button(self.frame,text=bidi_text, command=self.showManage)
		self.manageButton.configure(background = '#AF323E',  font = (fnt,40))
		self.manageButton.pack()
		self.frame.pack()
		# bind <F11> key to toggle full screen (default mode) 
		self.master.bind("<F11>", self.toggle_fullscreen)
		self.master.bind("<Escape>", self.end_fullscreen)
		# bind <ESC> key to exit full screen
		self.master.attributes("-fullscreen", True)
		
		self.imgVid = imgVid
		self.master.protocol("WM_DELETE_WINDOW", self.onClosing)
		
	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"
		
	def showSocket(self):
		# instantiate socket window with top level window of current window (main window)
		self.socket = tk.Toplevel(self.master)
		self.app = socketWindow(self.socket)
	
	def showManage(self):
		# instantiate manage window with top level window of current window (main window)
		self.manage = tk.Toplevel(self.master)
		self.app = manageWindow(self.manage)
		
	def onClosing(self):
		# exit video capture on exit program
		global imgVid
		imgVid.sigExit = True
		self.master.destroy()

'''
Select charger socket window class
'''
class socketWindow:
	# initiate buttons for types of charge sockets, each call getSocket() method on click
	def __init__(self, master):
		self.master = master
		self.shelfNum = None
		self.frame = tk.Frame(self.master)
		bidi_text = get_display(arabic_reshaper.reshape(u'لطفا نوع گوشی خود را مشخص کنید'))
		self.sText = tk.Label(self.frame, text= bidi_text, font = (fnt,25))
		self.sText.pack()
		
		bidi_text = get_display(arabic_reshaper.reshape(u'اندروید'))
		self.androidButton = tk.Button(self.frame,text=bidi_text, command= lambda:self.getSocket(ANDROID))
		self.androidButton.configure(background = '#A2AF3E',  font = (fnt,40))
		self.androidButton.pack()
		
		bidi_text = get_display(arabic_reshaper.reshape(u'آیفون'))
		self.iphoneButton = tk.Button(self.frame,text=bidi_text, command= lambda:self.getSocket(IPHONE))
		self.iphoneButton.configure(background = '#A2AF3E',  font = (fnt,40))
		self.iphoneButton.pack()

		bidi_text = get_display(arabic_reshaper.reshape(u'تایپ سی'))
		self.type_cButton = tk.Button(self.frame,text=bidi_text, command= lambda:self.getSocket(TYPE_C))
		self.type_cButton.configure(background = '#A2AF3E',  font = (fnt,40))
		self.type_cButton.pack()

		bidi_text = get_display(arabic_reshaper.reshape(u'نوکیا'))
		self.nokiaButton = tk.Button(self.frame,text=bidi_text, command= lambda:self.getSocket(NOKIA))
		self.nokiaButton.configure(background = '#A2AF3E',  font = (fnt,40))
		self.nokiaButton.pack()

		self.frame.pack()
		#self.master.attributes("-fullscreen", True)
		master.bind("<F11>", self.toggle_fullscreen)
		master.bind("<Escape>", self.end_fullscreen)
		
	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"
		
	def close_windows(self):
		self.master.destroy()
		#getSocket method
	def getSocket(self,socketType):
		#lock at db for socket window if exitsts with alocateShelf() in DBIntract class
		self.shelfNum = db.allocateShelf(socketType)
		if not (self.shelfNum is None):
			# instantiate fingerprint detect window
			self.finger = tk.Toplevel(self.master)
			self.app = fingerWindow(self.finger,self.shelfNum, socketType,"SET",self.master)
		else:
			#display does not exist message and return to main window
			self.message = tk.Toplevel(self.master)
			delayInMS = 3500
			self.app = messageWindow(u'متاسفانه در حال حاضر هیچ قفسه ای برای سوکت شما خالی نیست',delayInMS, self.message,self.master)

'''
Costumized messages window
'''
class messageWindow:
	def __init__(self, message,delay, master, destroyWindow= None):
		self.master = master
		self.destroyWindow = destroyWindow
		self.frame = tk.Frame(self.master)
		bidi_text = get_display(arabic_reshaper.reshape(message))
		self.sText = tk.Label(self.frame, text= bidi_text, font = (fnt,25))
		self.sText.pack()
		self.frame.pack()
		self.master.attributes("-fullscreen", True)
		# set exit time after display message
		root.after(delay, self.exitMessage)
		
	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"
		
	def exitMessage(self):
		if not (self.destroyWindow is None):
			self.destroyWindow.destroy()
		self.master.destroy()
		
'''
Fingerprint & communication with fingerprint module class
'''
class fingerWindow:
	def __init__(self, master, shelfNum, socketType, operation="SET", destroyWindow = None):
		self.shelfNum = shelfNum
		self.socketType = socketType
		self.destroyWindow = destroyWindow
		self.master = master
		self.frame = tk.Frame(self.master)
		self.bidi_text = tk.StringVar()
		self.sText = tk.Label(self.frame, textvariable= self.bidi_text, font = (fnt,25))
		self.sText.pack()
		self.frame.pack()
		self.shelfNum = shelfNum
		
		self.master.attributes("-fullscreen", True)
		master.bind("<F11>", self.toggle_fullscreen)
		master.bind("<Escape>", self.end_fullscreen)
		# decide if user wants to set finger (and charger phone) or get finger
		# (and recieve phone) with different methods and messages 
		if operation == "SET":
			self.frame.update()
			# after 1 ms goto setFinger method
			self.setFinger()
		elif operation == "GET":
			self.getFinger()
				
	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"
		
	def getFinger(self):
		print ("1")
		
	def setFinger(self):
		i = 0
		ps = False
		#start recording time of camera video to capture users face for future considerations
		imgVid.recordStart()
		#print('PASSED!')
		#TODO: do not store any data until confirm that user delivers his phone
		while i<3 and ps != True:
			i +=1
			self.bidi_text.set(get_display(arabic_reshaper.reshape(u'لطفا انگشت خود را روی حسگر قرار دهید')))
			self.frame.update()
			time.sleep(1)
			while (finger.readImage() == False):
				pass
			finger.convertImage(0x01)
			
			result = finger.searchTemplate()
			positionNumber = result[0]
			if (positionNumber >= 0):
				self.bidi_text.set(get_display(arabic_reshaper.reshape(u'این اثر انگشت در سیستم وجود دارد. درصورتی که مایل به دریافت گوشی خود هستید از گزینه  "دریافت گوشی" استفاده کنید')))
				self.frame.update()
				time.sleep(5)
				break
			else:
				self.bidi_text.set(get_display(arabic_reshaper.reshape(u'انگشت خود را بردارید')))
				self.frame.update()
				time.sleep(2)
				self.bidi_text.set(get_display(arabic_reshaper.reshape(u'جهت حفظ موارد امنیتی مجددا همان انگشت را روی حسگر قرار دهید ')))
				self.frame.update()
				
				while (finger.readImage() == False):
					pass
				finger.convertImage(0x02)
				time.sleep(1)
				if ( finger.compareCharacteristics() == 0 ):
					self.bidi_text.set(get_display(arabic_reshaper.reshape(u'عدم تطابق اثر انگشت ها')))
					self.frame.update()
					time.sleep(2.5)
					continue
				else:
					ps = True
					finger.createTemplate()	
					#print(sel)
					positionNumber = int(self.shelfNum)
					if positionNumber != int(self.shelfNum):
						self.bidi_text.set(get_display(arabic_reshaper.reshape(u'خطا در تکمیل عملیات')))
						self.frame.update()
						time.sleep(2)
						break
					else:
			# ~ shelf allocation
						self.bidi_text.set(get_display(arabic_reshaper.reshape(u'اثر انگشت شما با موفقیت ثبت شد')))
						self.frame.update()
						time.sleep(2)
						direction = ""
						if int(self.socketType) == 1:
							direction = u'چپ'
						else:
							direction = u'راست'
						self.bidi_text.set(get_display(arabic_reshaper.reshape(u'لطفا گوشی خود را به سوکت سمت ' +direction + u' صندوق شماره ' + str(self.shelfNum) + u' متصل نموده و آن را داخل صندوق قرار دهید')))
						self.frame.update()
						time.sleep(8)
						inOut = 1
						# ~ 1 for Deliver and 2 for Restore
						fingerID = finger.downloadCharacteristics()
						strFinger = ''.join(format(x, '02x') for x in fingerID)
						storeMsg = ""
						while storeMsg != "Success":
							storeMsg = imgVid.recordStop(self.shelfNum, 
							self.socketType, strFinger, inOut)
							if storeMsg == "NO FACE":
								self.bidi_text.set(get_display(arabic_reshaper.reshape(u'لطفا چهره خود را به سمت دوربین نگه دارید.')))
								self.frame.update()
								time.sleep(2)
						print("Store message: ", storeMsg)
				# ~ connectivity check here
				# ~ proximity sensor check here
				# ~ if all things goes right
				# ~ store data in the files

						# ~ writeInConf = self.shelf.write(self.shelfNum,self.socketType, strFinger)
						self.success = 0
					
					if self.success == 1:
						self.bidi_text.set(get_display(arabic_reshaper.reshape(u'کاربر گرامی، گوشی شما در امنیت شارژ می شود! می توانید با گزینه دریافت گوشی، آن را تحویل بگیرید')))
						self.frame.update()
						time.sleep(7)
						break
				# update config.json
					else:
						self.bidi_text.set(get_display(arabic_reshaper.reshape(u'مشکل در عملیات تحویل و شارژ گوشی')))
						self.frame.update()
						time.sleep(3)
						break
		self.exitFinger()		
			
	def exitFinger(self):
		if not (self.destroyWindow is None):
			self.destroyWindow.destroy()
		self.master.destroy()

class loginWindow:
	def __init__(self,master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.master.attributes("-fullscreen", True)
		master.bind("<F11>", self.toggle_fullscreen)
		master.bind("<Escape>", self.end_fullscreen)
		#self.EntryFrame = 
	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"
		
	def FGridFormatButtons(self, buttonList, newLineAmount = 3 ):
		self.Row = 0
		self.Col = 0
		for Button in buttonList:
			Button.grid(row= self.Row, column = self.Col)
			self.Col += 1
			if self.Col  == newLineAmount:
				# when the Col variable gets to the NewLineAmount, then it will got to the new line.
				# Making this very good for when you want to have a crap tone of buttons :D
				self.Row += 1
				self.Col = 0
				continue
				
		
class manageWindow:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		
		bidi_text = get_display(arabic_reshaper.reshape(u'دسترسی به قفسه'))
		self.androidButton = tk.Button(self.frame,text=bidi_text, command= self.showAccessedShelf)
		self.androidButton.configure(background = '#A2AF3E',  font = (fnt,40))
		self.androidButton.pack()
		
		bidi_text = get_display(arabic_reshaper.reshape(u'فعال/غیرفعال کردن سوکت'))
		self.iphoneButton = tk.Button(self.frame,text=bidi_text, command= self.showActivateSocket)
		self.iphoneButton.configure(background = '#A2AF3E',  font = (fnt,40))
		self.iphoneButton.pack()


		self.frame.pack()
		self.master.attributes("-fullscreen", True)
		master.bind("<F11>", self.toggle_fullscreen)
		master.bind("<Escape>", self.end_fullscreen)
		
	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"
	
	def showAccessedShelf(self):
		# instantiate manage window with top level window of current window (main window)
		self.shelfAccess = tk.Toplevel(self.master)
		self.app = accessWindow(self.manage)
		
	def showActivateSocket(self):
		# instantiate manage window with top level window of current window (main window)
		self.shelfAccess = tk.Toplevel(self.master)
		self.app = AccessWindow(self.manage)

class accessWindow:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		
		bidi_text = get_display(arabic_reshaper.reshape(u'دسترسی به قفسه'))
		self.androidButton = tk.Button(self.frame,text=bidi_text, command= self.showAccessedShelf)
		self.androidButton.configure(background = '#000F3E',  font = (fnt,40))
		self.androidButton.pack()
		
		bidi_text = get_display(arabic_reshaper.reshape(u'فعال/غیرفعال کردن سوکت'))
		self.iphoneButton = tk.Button(self.frame,text=bidi_text, command= self.showActivateSocket)
		self.iphoneButton.configure(background = '#A2A00E',  font = (fnt,40))
		self.iphoneButton.pack()


		self.frame.pack()
		self.master.attributes("-fullscreen", True)
		master.bind("<F11>", self.toggle_fullscreen)
		master.bind("<Escape>", self.end_fullscreen)
'''
Starting code:
First, tries to connect to fingerprint module from USB1 (ttyS1, Rx:pin38,Tx:pin40)
with 5V R308 fingerprint module
'''
if __name__ == '__main__':

	try:
		#Password: 0x00000000
		finger = PyFingerprint('/dev/ttyS1', 57600, 0xFFFFFFFF, 0x00000000)

		if ( finger.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')

	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		exit(1)
	#Instantiate tkinter object
	root = tk.Tk()
	# create and run mainWindow object with mainloop method
	app = mainWindow(root)
	root.mainloop()
