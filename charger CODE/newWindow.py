import tkinter as tk
class mainWindow:
	def __init__(self,master):
		self.master = master
		container = root.Frame(self)
		self.master.title("Charger V0.1")
		self.master.attributes("-fullscreen", True)
		self.master.bind("<F11>", self.toggle_fullscreen)
		self.master.bind("<Escape>", self.end_fullscreen)
		self.frames = {}
		for F in (StartPage, PageOne, PageTwo):
			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame(StartPage)

	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.master.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.master.attributes("-fullscreen", False)
		return "break"

        
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
        


#Instantiate tkinter object
root = tk.Tk()
# create and run mainWindow object with mainloop method
app = mainWindow(root)
root.mainloop()