from tkinter import *
def on_after():
	tx.set("be")
window = Tk()
 
window.title("Welcome to LikeGeeks app")
tx = StringVar()
lbl = Label(window, textvariable=tx)
tx.set("Hell")
window.after(4000, on_after)
lbl.grid(column=0, row=0)
 
window.mainloop()