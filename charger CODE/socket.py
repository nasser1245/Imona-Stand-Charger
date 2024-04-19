#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 17:23:10 2019

@author: nasser
"""
import tkinter as tk
import arabic_reshaper
from bidi.algorithm import get_display
fnt = "XB Shiraz"
ANDROID = "1"
IPHONE = "2"
TYPE_C = "3"
NOKIA  = "4"

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
	#	self.shelfNum = db.allocateShelf(socketType)
	#	if not (self.shelfNum is None):
			# instantiate fingerprint detect window
	#		self.finger = tk.Toplevel(self.master)
	#		self.app = fingerWindow(self.finger,self.shelfNum, socketType,"SET",self.master)
	#	else:
			#display does not exist message and return to main window
		#	self.message = tk.Toplevel(self.master)
		#	delayInMS = 3500
		#	self.app = messageWindow(u'متاسفانه در حال حاضر هیچ قفسه ای برای سوکت شما خالی نیست',delayInMS, self.message,self.master)
