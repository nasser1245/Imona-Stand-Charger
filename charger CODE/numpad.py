import tkinter, tkinter.ttk as ttk
import random
import hashlib
hashGen = hashlib.sha512()
hashGen.update ("5".encode('utf-8'))
hash = hashGen.hexdigest()
print ("your hash is: ", hash)
class BaseWindow(tkinter.Tk):
	def _Change(self):
		x,y = self.winfo_width(), self.winfo_height()
		
		self.minsize(x,y); self.maxsize(x, y)
		#this locks the window into what size the window is in this called
		
	def FGridFormatButtons(self, ButtonList, NewLineAmount = 3 ):
		self.Row = 0
		self.Col = 0
		for Button in ButtonList:
			Button.grid(row= self.Row, column = self.Col)
			self.Col += 1
			if self.Col  == NewLineAmount:
				# when the Col variable gets to the NewLineAmount, then it will got to the new line.
				# Making this very good for when you want to have a crap tone of buttons :D
				self.Row += 1
				self.Col = 0
				continue
		# This entire def is formatting the buttons using theGrid system in tkinter. As all of the buttons
		# in the ButtonList are set to go with each other frame, all we have to do here is do .grid()!
class Window(BaseWindow):
	def __init__(self, **args):
		super(Window, self).__init__()
		# This just stops the recursion, when I say that I mean if you don't have this,
		# It just loops and crashes. We don't want that.
		
		self.EntryFrame = ttk.Frame(self)
		self.PadFrame = ttk.Frame(self)
		
		self.EntryFrame.pack(padx = 5, pady = 5)
		self.PadFrame.pack(padx = 5, pady = 5)
		# These create the frames, for the loop entry, and the bottom pad.
		
		self.AllButtons = []
		self.CanWrite = True
		
		self.Code = args.get("code") or random.randrange(9999)
		self.Timer = args.get("timer") or 2000
		
		print("DEBUG: %d"% self.Code) # Unlock code
		
		for x in range(1,10):
			self.AllButtons.append(ttk.Button(self.PadFrame, width = 4, text = x, command = lambda y = x: self.Update(y)))
			self.bind(str(x), lambda CatchEvent, y = x: self.Update(y))
			

			
		self.FGridFormatButtons(self.AllButtons)
		
		self.ZeroButton = ttk.Button(self.PadFrame, width = 4, text = 0, command = lambda: self.Update(0))
		self.SubmitButton = ttk.Button(self.PadFrame, width = 4, text = "Ent", command = self.CheckCode)
		self.ClearButton = ttk.Button(self.PadFrame, width = 4, text = "C", command = lambda:self.Update(-1))
		
		self.ClearButton.grid(row = self.Row, column = 0)
		self.ZeroButton.grid(row = self.Row, column = 1)
		self.SubmitButton.grid(row = self.Row, column = 2)
		
		self.bind("0", lambda CatchEvent: self.Update(0))
		self.bind("<Return>", lambda CatchEvent: self.CheckCode())
		self.
		self.KeyEnter = ttk.Entry(self.EntryFrame, state = "disabled")
		self.KeyEnter.pack()
		
		self.after(5, self._Change)
		
		#----
	def Update(self, x):
		if self.CanWrite:
			self.KeyEnter["state"] = "normal"
			
			if x == -1:
				self.KeyEnter.delete(0, tkinter.END)
			else:
				self.KeyEnter.insert(tkinter.END, x)
			self.KeyEnter["state"] = "disabled"
	
	def CheckCode(self):
		Key = self.KeyEnter.get()
		
		self.Update(-1)
		
		if Key == str(self.Code):
			self.Update("Correct Code!")
			self.after(self.Timer, self.destroy)
		else:
			self.Update("Incorrect Code!")
			
		self.ChangeWritePerms()
		self.after(self.Timer, self.ChangeWritePerms)
	
	def ChangeWritePerms(self):
		if self.CanWrite:
			self.CanWrite = False
		else:
			self.CanWrite = True
			self.Update(-1)

# start the window
Window().mainloop()
		
