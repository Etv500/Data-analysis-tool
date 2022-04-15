# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 12:16:26 2020

@author: elvis
"""



import LOAD_DATA
import PROCESS_VISUAL_DATA_v2
from tkinter import *
import IMPORT_DATA as mymo 
import DELETE
###############################
#GUI###########################
###############################
class window_design:
    
    def __init__(self):
        main_window = Tk()
 
        main_window.geometry("700x550")
        main_window.minsize("700","550")
        main_window.maxsize("700","550")
        main_window.title("Some good software")
        main_window.configure(bg='grey')
        
        ####LEFT FRAME##########################################################################
        mainframe = Frame (main_window, bd=3, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=5, padx=-50) 
        
        ####INTRO, LOAD AND PROCESS#############################################################
        introlabel = Label(mainframe, text="Welcome to Some Good Software!", padx=100, pady=10, font='Helvetica 12 bold')
        introlabel.grid(row=0,column=0, sticky=E+W, padx=100, pady=10)
          
        button1= Button(mainframe, text="LOAD/UPDATE DATA", bg="white", activebackground='green', width = 40, command=LOAD_DATA.load_data)
        button1.grid(row=1,column=0,  padx=100, pady=10)

        button2= Button(mainframe, text="PROCESS DATA & OUTPUT STATS (Points 1,2,3)", bg="white", activebackground='green', width = 40, command=lambda: PROCESS_VISUAL_DATA_v2.process.process_data(False))                                                                          
        button2.grid(row=2,column=0,  padx=100, pady=10)
         
        leftmainframe = Frame (main_window, bd=3, bg='pink', highlightbackground="pink", highlightcolor="green", highlightthickness=1, padx=-50) 
       
        ####OUTPUT VIOLATIONS CHART (Point 4)#####################################################
        violchartframe = Frame (leftmainframe, bd=3, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=1, padx=-50) 
       
        rangelabel1 = Label(violchartframe, text="Select rows range for the chart:", font='Helvetica 10')
        rangelabel1.grid(row=1,column=0, sticky=E+W, padx=50, pady=10)
        
        violchartframe.grid()
        
        violchartframe_range = Frame (violchartframe, bd=3, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=1) 
        
        startviol = Entry(violchartframe_range, bd = 3)
        startviol.grid(row=3,column=0,  padx=5, pady=10)
        startviol.insert(END, 'input start row')
        
        endviol = Entry(violchartframe_range, bd = 3)
        endviol.grid(row=3,column=2,  padx=5, pady=10)
        endviol.insert(END, 'input end row')
        
        button3= Button(violchartframe, text="OUTPUT VIOLATIONS CHART (Point 4)", bg="white", activebackground='green', width = 40, command=lambda: PROCESS_VISUAL_DATA_v2.process.process_visual_viol((startviol.get()), endviol.get()))
        button3.grid(row=0,column=0,  padx=50, pady=10)
        
        violchartframe_range.grid()
        
        spacerframe = Frame (mainframe, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=0, padx=-50) 
        spacerframe.grid()
        
        ####OUTPUT CORRELATION ANALYSIS (Point 5)#####################################################
        correlationframe = Frame (leftmainframe, bd=3, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=1, padx=-50) 
        
        button4= Button(correlationframe, text="OUTPUT CORRELATION ANALYSIS (Point 5)", bg="white", activebackground='green', width = 40, command=lambda: PROCESS_VISUAL_DATA_v2.process.process_visual_correl((startcorrel.get()), endcorrel.get()))
        button4.grid(row=0,column=0, padx=50, pady=10)     
        
        rangelabel2 = Label(correlationframe, text="Select rows range for the chart:", font='Helvetica 10')
        rangelabel2.grid(row=1,column=0, sticky=E+W, padx=50, pady=10)
        
        correlationframe.grid()
        
        correlationframe_range = Frame (correlationframe, bd=3, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=1) 
        
        startcorrel = Entry(correlationframe_range, bd = 3)
        startcorrel.grid(row=3,column=0,  padx=5, pady=10)
        startcorrel.insert(END, 'input start row')
        
        endcorrel = Entry(correlationframe_range, bd = 3)
        endcorrel.grid(row=3,column=2,  padx=5, pady=10)
        endcorrel.insert(END, 'input end row')
        
        correlationframe_range.grid()
        
        spacerframe = Frame (mainframe, bg='grey', highlightbackground="pink", highlightcolor="green", highlightthickness=0, padx=-50) 
        spacerframe.grid()
        
        ####RESET#####################################################
        button5= Button(mainframe, text="RESET - EMPTY ALL DATA AND FILES", bg="white", activebackground='green', width = 40, command=DELETE.resetall)
        button5.grid(row=7,column=0,  padx=100, pady=10)

        ######################################################################################
        mainframe.grid()
        mainframe.grid_columnconfigure(1,weight=1) 
        leftmainframe.grid(row=1,column=0) 
        leftmainframe.grid_columnconfigure(1,weight=1) 
        main_window.grid_columnconfigure(0,weight=1) 
        main_window.mainloop() 
        
window_design()