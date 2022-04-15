# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 18:45:30 2020

@author: elvis
"""

from pathlib import Path
import IMPORT_DATA as mymo 
import os
import shutil
from pymongo import MongoClient
import easygui

def resetall():
    
    #######delete All_input_and_output folder###########
    filespath = mymo.mainpath()  
    shutil.rmtree(filespath, ignore_errors=True)
    
    #######delete all JSON backup######################
    if os.path.exists('./violations.json') == True:
        os.remove("violations.json")
    if os.path.exists('./inventroy.json') == True:
        os.remove("inventroy.json")
    if os.path.exists('./inspections.json') == True:
        os.remove("inspections.json")
    if os.path.exists('./filespath.txt') == True:
        os.remove("filespath.txt")
  
    #######delete MongoDB collections###################
    client = MongoClient('localhost', 27017)
    db = client.Summative09
    db['inspections'].drop()
    db['violations'].drop()
    db['inventroy'].drop()
    
    easygui.msgbox("Application reset complete!", title="Application reset")
