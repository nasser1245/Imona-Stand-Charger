#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 18:03:47 2019

@author: nasser
"""
import tkinter as tk
LARGE_FONT= ("Verdana", 12)
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
         button1 = tk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
         button1.pack()
 
#         button2 = tk.Button(self, text="Page One",
#                             command=lambda: controller.show_frame(PageOne))
#         button2.pack()
# =============================================================================
        