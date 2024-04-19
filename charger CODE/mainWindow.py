import tkinter as tk
import arabic_reshaper
from bidi.algorithm import get_display
import socket as skt
fnt = "XB Shiraz"
class mainWindow:
	def __init__(self,master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.master.title("Charger V0.1")
		self.master.attributes("-fullscreen", True)
		master.bind("<F11>", self.toggle_fullscreen)
		master.bind("<Escape>", self.end_fullscreen)
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
		self.app = skt.socketWindow(self.socket)
	
	def showManage(self):
		pass
		# instantiate manage window with top level window of current window (main window)
		#self.manage = tk.Toplevel(self.master)
		#self.app = manageWindow(self.manage)
		
	def onClosing(self):
		# exit video capture on exit program
		global imgVid
		imgVid.sigExit = True
		self.master.destroy()


if __name__ == "__main__":
	#Instantiate tkinter object
	root = tk.Tk()
	# create and run mainWindow object with mainloop method
	app = mainWindow(root)
	root.mainloop()
