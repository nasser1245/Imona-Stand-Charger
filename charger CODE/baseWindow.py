# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import tkinter as tk
#import arabic_reshaper
#from bidi.algorithm import get_display
#from pyfingerprint.pyfingerprint import PyFingerprint
#from imageVideoThread import imageVideoThread
#from DBIntract import DBIntract
import time

LARGE_FONT = ("Verdana", 12)


class baseWindow(tk.Tk):

	def __init__(self, *args, **kwargs):
        
		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)

		container.configure(background='#3F2AB1')
		#container.title("Charger V0.1")
		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, PageOne, PageTwo):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

        
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
		button.pack()

		button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
		button2.pack()


class PageOne(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
		button2.pack()


class PageTwo(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
		button2.pack()
        


app = baseWindow()
app.mainloop()