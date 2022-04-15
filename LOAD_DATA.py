# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 12:52:28 2020

@author: elvis
"""

#training here:https://api.mongodb.com/python/current/tutorial.html
#check in services in windows search and check MongoDB is running before using it or set it to running

from pymongo import MongoClient
import pandas as pd
import IMPORT_DATA as mymo 
from tkinter import *
import os
import easygui
import sys
import BACKUP_DATA as bu
###############################
#LOAD DATA#####################
###############################

def load_data():
    #Connect Mongo##########################################################################################################################
    client = MongoClient('localhost', 27017)  #or client = MongoClient('mongodb://localhost:27017/')
    #Check db exists##########################################################################################################################
    db = client.Summative09
    dbnames = client.list_database_names()
    if 'Summative09' in dbnames:
        print ('Summative09 is there!') #db already created
    else:
        db = client["Summative09"]  #create db
    #Input Path to files########################################################################################################################### 
    
    ####CONTROLLA SE filespath esiste
    
    filespath = ''
    if os.path.exists('./filespath.txt') == False or os.stat('./filespath.txt').st_size == 0:
        while True:  
            try:
                filespath = simpledialog.askstring("Input directory for source data" , "Enter directory to the csv file to be loaded using the following format C:/Users/xxxx/Inputs_and_outputs/" )
                result = os.listdir(filespath)
                text_file = open("filespath.txt", "w")
                text_file.write(filespath)
                text_file.close()
            except FileNotFoundError:
                messagebox.showerror("FileNotFoundError", "Directory does not exist or is empty")
            else:
                break
    
    filespath = mymo.mainpath()
    #Load and backup Inspections###########################################################################################################################
    collectname = 'inspections'
    csvdata_load =  filespath + 'Inspections.csv'
    csvdata_header = [ 'ACTIVITY DATE',	'OWNER ID',	'OWNER NAME',	'FACILITY ID',	'FACILITY NAME',	'RECORD ID',	'PROGRAM NAME',	'PROGRAM STATUS',	'PROGRAM ELEMENT (PE)',	'PE DESCRIPTION',	'FACILITY ADDRESS',	'FACILITY CITY',	'FACILITY STATE',	'FACILITY ZIP',	'SERVICE CODE',	'SERVICE DESCRIPTION',	'SCORE',	'GRADE',	'SERIAL NUMBER',	'EMPLOYEE ID',	'Location',	'2011 Supervisorial District Boundaries (Official)',	'Census Tracts 2010',	'Board Approved Statistical Areas',	'Zip Codes']
    inspections = mymo.import_csvjson_tomongo(collectname, csvdata_load, csvdata_header, db, client)
    os.system('cmd /c "mongoexport --host="localhost" --port=27017 --collection='+collectname+' --db=Summative09 --out='+collectname+'.json"')
    #Load and backup Inventroy###########################################################################################################################   
    collectname = 'inventroy'
    csvdata_load = filespath + 'Inventroy.csv'
    csvdata_header =  ['FACILITY ID',	'FACILITY NAME',	'RECORD ID',	' PROGRAM NAME',	'PROGRAM ELEMENT (PE)',	'PE DESCRIPTION',	'FACILITY ADDRESS',	'FACILITY CITY',	'FACILITY  STATE',	'FACILITY ZIP',	'FACILITY LATITUDE',	'FACILITY LONGITUDE',	'OWNER ID',	'OWNER NAME',	'OWNER ADDRESS',	'OWNER CITY',	'OWNER STATE',	'OWNER ZIP',	'Location',	'Census Tracts 2010',	'2011 Supervisorial District Boundaries (Official)',	'Board Approved Statistical Areas',	'Zip Codes']
    inventroy = mymo.import_csvjson_tomongo(collectname, csvdata_load, csvdata_header, db, client)
    os.system('cmd /c "mongoexport --host="localhost" --port=27017 --collection='+collectname+' --db=Summative09 --out='+collectname+'.json"')
    #Load and backup Violations###########################################################################################################################   
    collectname = 'violations'
    csvdata_load = filespath + 'violations.csv'
    csvdata_header = ['SERIAL NUMBER',	'VIOLATION  STATUS',	'VIOLATION CODE',	'VIOLATION DESCRIPTION',	'POINTS']
    violations = mymo.import_csvjson_tomongo(collectname, csvdata_load, csvdata_header, db, client)
    os.system('cmd /c "mongoexport --host="localhost" --port=27017 --collection='+collectname+' --db=Summative09 --out='+collectname+'.json"')  
    ######################################################################################################################################
    easygui.msgbox("Data Loaded/Updated!", title="Data Load/Update")


