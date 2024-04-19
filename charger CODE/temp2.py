from guizero import App
app = App()
#app.tk.overrideredirect(True)
width = app.tk.winfo_screenwidth()
height = app.tk.winfo_screenheight()
app.tk.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))

#app.tk.update_idletasks()
#app.tk.wm_attributes("-type","splash")
#app.tk.update()
app.display()
