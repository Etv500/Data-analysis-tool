# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 13:25:16 2020

@author: elvis
"""

import csv
import os
import easygui
###############################
#import########################
###############################

def importdata(collectname: str):
    os.system('cmd /c "mongoimport --host="localhost" --port=27017 --collection=' + collectname + '--db=Summative09 --upsert --file=' + collectname + '.json"')
    collectname = collectname
    
    
def import_csvjson_tomongo(collectname: str, filespath, header, db, client):
    is_collection_there = collectname in db.list_collection_names() 
    if is_collection_there == True:
        easygui.msgbox(collectname + ' is there! loading up to date records', title="Updating records")
        importdata(collectname)
    else:
        easygui.msgbox(collectname + ' is not there! loading', title="Loading records")
        with open(filespath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                doc={}
                for n in range(0,len(header)):
                    doc[header[n]] = row[n]   
                db[collectname].insert_one(doc)   
        print('Current dbs')     
        print(client.list_database_names())
        print('Current collections')
        print(db.list_collection_names())
    
def mainpath():
    filespath = open("filespath.txt", "r")
    filespath = filespath .read()
    return filespath