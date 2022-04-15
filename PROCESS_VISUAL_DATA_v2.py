# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:50:28 2020

@author: elvis
"""

from pymongo import MongoClient
import pandas as pd
import numpy as np
import os
from tkinter import *
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sn
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import IMPORT_DATA as mymo 
import easygui
import BACKUP_DATA as bckup

###############################
#PROCESS DATA##################
###############################

class process:

    def process_data(skipstats) :
        filespath = mymo.mainpath()
        
    
        
        client = MongoClient('localhost', 27017)
        db = client.Summative09
        
        if ('violations' in db.list_collection_names()) == True and ('inspections' in db.list_collection_names()) == True and ('inventroy' in db.list_collection_names()) == True:
            
            #Load all to dataframe##########################################################################################################################
            df_inspections = pd.DataFrame(list(db['inspections'].find()))
            df_inspections.drop(df_inspections.index[0], inplace=True)
            df_inventroy = pd.DataFrame(list(db['inventroy'].find()))
            df_inventroy = df_inventroy.drop(df_inventroy.index[0])
            df_violations = pd.DataFrame(list(db['violations'].find()))
            df_violations = df_violations.drop(df_violations.index[0])
   
        #Transformations##########################################################################################################################
            
            #1.	Outputs should not include any data from vendors that have a ‘PROGRAM STATUS’ of INACTIVE
            is_active =  df_inspections['PROGRAM STATUS']=='ACTIVE'
            df_inspections = df_inspections[is_active]
            
            #2. Extract info between parenthesis from PE DESCRIPTION to a new column without modifying the source column 
            new = df_inspections['PE DESCRIPTION'].str.split("(", n = 1, expand = True) 
            df_inspections["workings"]= new[1]
            new = df_inspections["workings"].str.split(")", n = 1, expand = True) 
            df_inspections["TYPE OF SEATING"]= new[0] 
            df_inspections.drop(columns =["workings"], inplace = True) 
    
            ############Skip stats if need only clean data laod/save without stats##################################################
            if skipstats == False:
                #Inspections:3.	Produce the mean, mode and median for the inspection score per year SCORE, grouping by Zip Codes or TYPE OF SEATING
                #a.
                #drop missing values
                seatings_stats_df = df_inspections.filter(["TYPE OF SEATING", "SCORE"], axis=1)
                seatings_stats_df = seatings_stats_df.replace(["NaN", 'NaT', None, ''''''], np.nan)
                seatings_stats_df = seatings_stats_df.dropna(axis=0, how='any')
                grouping_variable = 'TYPE OF SEATING'
                #convert SCORE to integer
                seatings_stats_df_baseforanalysis = seatings_stats_df.astype({grouping_variable: str, 'SCORE': int})
                #calc stats grouped by type of seating
                temp_df = seatings_stats_df_baseforanalysis.groupby(grouping_variable)['SCORE'].mean().reset_index(name='mean')
                seatings_stats_df = temp_df
                temp_df = seatings_stats_df_baseforanalysis.groupby(grouping_variable)['SCORE'].median().reset_index(name='median')
                seatings_stats_df = pd.merge(seatings_stats_df, temp_df)
                temp_df = seatings_stats_df_baseforanalysis.groupby(grouping_variable)['SCORE'].agg(lambda x:x.value_counts().index[0]).to_frame().reset_index()
                temp_df = temp_df.rename(columns={'SCORE': 'mode'})
                seatings_stats_df = pd.merge(seatings_stats_df, temp_df)
                seatings_stats_df = seatings_stats_df.astype({grouping_variable: str, 'mean': int, 'mode': int, 'median': int})
                seatings_stats_df.to_csv(filespath + 'types_seating_stats.csv', index=False, encoding='utf-8') 
                #drop missing values
                zipcodes_stats_df = df_inspections.filter(["Zip Codes", "SCORE"], axis=1)
                zipcodes_stats_df = zipcodes_stats_df.replace(["NaN", 'NaT', None, ''''''], np.nan)
                zipcodes_stats_df = zipcodes_stats_df.dropna(
                    axis=0,
                    how='any',
                )          
                grouping_variable = 'Zip Codes'
                #convert SCORE to integer
                zipcodes_stats_df_baseforanalysis = zipcodes_stats_df.astype({grouping_variable: str, 'SCORE': int})
                #calc stats grouped by type of seating
                temp_df = zipcodes_stats_df_baseforanalysis.groupby(grouping_variable)['SCORE'].mean().reset_index(name='mean')
                zipcodes_stats_df = temp_df
                temp_df = zipcodes_stats_df_baseforanalysis.groupby(grouping_variable)['SCORE'].median().reset_index(name='median')
                zipcodes_stats_df = pd.merge(zipcodes_stats_df, temp_df)
                temp_df = zipcodes_stats_df_baseforanalysis.groupby(grouping_variable)['SCORE'].agg(lambda x:x.value_counts().index[0]).to_frame().reset_index()
                temp_df = temp_df.rename(columns={'SCORE': 'mode'})
                zipcodes_stats_df = pd.merge(zipcodes_stats_df, temp_df)
                zipcodes_stats_df = zipcodes_stats_df.astype({grouping_variable: str, 'mean': int, 'mode': int, 'median': int})
                zipcodes_stats_df.to_csv(filespath + 'zip_codes_stats.csv', index=False, encoding='utf-8') 
            
            dataframes = [df_violations, df_inventroy, df_inspections]
           
            ################Load trabsformed data to MongoDB and export json to folder####################################### 
    
            if skipstats == False:
                easygui.msgbox("Wait for backup to complete!", title="Backing up")
                bckup.backup_data.exportdata("violations", db, df_violations)
                bckup.backup_data.exportdata("inspections", db, df_inspections)
                bckup.backup_data.exportdata("inventroy", db, df_inventroy)
            
            if skipstats == False:
                easygui.msgbox("Processing done!", title="Processing done")
        
        else:
            easygui.msgbox("Please make sure all data is in the database, you might need to redo LOAD/UPDATE DATA", title="Missing Collection in MongoDB")
     
        return dataframes 
        
    
    def process_visual_viol(startrangerow:int, endrangerow:int):

        #4.	Produce a suitable graph that displays the number of establishments that have committed each type of violation. 
        #You may need to consider how you group this data to make visualisation feasible  
        filespath = mymo.mainpath()  
        client = MongoClient('localhost', 27017)
        db = client.Summative09
        plt.style.use('./MPLSTYLE.py')
   
        if ('violations' in db.list_collection_names()) == True:
             
            if startrangerow.isdigit() and endrangerow.isdigit():
                
                df_violations = process.process_data(True)[0]
                df_violations_baseforanalysis = df_violations.filter(["VIOLATION CODE"], axis=1) 
                if startrangerow == 'input start row' and endrangerow == 'input end row':
                    df_violations_baseforanalysis = df_violations_baseforanalysis.iloc[int(startrangerow):int(endrangerow)]
                
                zipcodes_visual_df = df_violations_baseforanalysis["VIOLATION CODE"].value_counts().to_frame().reset_index()
                zipcodes_visual_df.columns = ['VIOLATION CODE', 'FREQUENCY']
                zipcodes_visual_df.to_csv(filespath + 'violations_analysis.csv', index=False, encoding='utf-8') 
                #Create and save bar chart at path
                plot = zipcodes_visual_df.plot.bar(x='VIOLATION CODE', y='FREQUENCY', rot=76, title="Violations Chart")
                fig = plot.get_figure()
                fig.set_size_inches(20.5, 12.5)
                fig.savefig(filespath + 'violations_analysis_chart.png', dpi=120)
                plt.show()
                
                ######displaychart in new GUI window######################################################################
                fig.subplots_adjust(bottom=0.15)
                root = Tk()
                root.title("Chart1")
                root.geometry("1200x700")
                root.minsize("1200","700")
                figure = fig
                chart_type = FigureCanvasTkAgg(figure, root)
                chart_type.get_tk_widget().pack(padx=10, pady=10)
                ###########################################################################################################
                #easygui.msgbox("Wait for backup to complete!", title="Backing up")
                #bckup.backup_data.exportdata("violations", db, df_violations)       
                easygui.msgbox("Processing done!", title="Processing done")
            else:
                easygui.msgbox("Please input integers >= 0!", title="Wrong input")
        else:
            easygui.msgbox("Please make sure all data is in the database, you might need to redo LOAD/UPDATE DATA", title="Missing Collection in MongoDB")
     
       
        ######5. correlation analysis: number of violations committed per vendor and their zip code##########################################################################################################

    def process_visual_correl(startrangerow:int, endrangerow:int):
      
       filespath = mymo.mainpath() 
       client = MongoClient('localhost', 27017)
       db = client.Summative09
       plt.style.use('./MPLSTYLE.py')
       
       if ('violations' in db.list_collection_names()) == True and ('inspections' in db.list_collection_names()) == True:
       
           
           if startrangerow.isdigit() and endrangerow.isdigit():
           
               df_violations = process.process_data(True)[0] 
               df_inspections = process.process_data(True)[2] 
               
               correl_df = pd.merge(df_violations, df_inspections, on = 'SERIAL NUMBER')
               correl_df = correl_df.filter(['VIOLATION CODE','TYPE OF SEATING','Zip Codes'], axis=1)
               correl_df = correl_df.replace(["NaN", 'NaT', None, ''''''], np.nan)
               correl_df = correl_df.dropna(axis=0, how='any')
               
               correl_df_vendors = correl_df.filter(['TYPE OF SEATING'], axis=1)
               correl_df_vendors = correl_df_vendors['TYPE OF SEATING'].value_counts().to_frame().reset_index() 
               correl_df_vendors.columns = ['TYPE OF SEATING', 'VENDOR VIOLS COUNT']

               correl_df = pd.merge( correl_df, correl_df_vendors, on='TYPE OF SEATING')
               correl_df ['Zip Codes'] = correl_df ['Zip Codes'].astype(int)
               correl_df ['VENDOR VIOLS COUNT'] = correl_df ['VENDOR VIOLS COUNT'].astype(int)
               correl_df = correl_df.filter(['VENDOR VIOLS COUNT', 'Zip Codes'], axis=1)
    
               if startrangerow == 'input start row' and endrangerow == 'input end row':
                   correl_df = correl_df.iloc[int(startrangerow):int(endrangerow)]
               
               corrMatrix = correl_df.corr()
     
               ######displaychart in new GUI window and save png######################################################################
               
               root = Tk()
               root.title("Chart2")
               root.geometry("1200x700")
               root.minsize("1200","700") 
               f, ax = plt.subplots(figsize=(11, 9))
               fig = f
               canvas = FigureCanvasTkAgg(fig, master=root)
               canvas.draw()
               canvas.get_tk_widget().pack()  
               sn.heatmap(corrMatrix, annot=True)
               plt.show()
    
               matrix = sn.heatmap(corrMatrix, annot=True)
               figure = matrix.get_figure()    
               figure.set_size_inches(7, 5)
               
               figure.savefig(filespath + 'correlation_chart.png', dpi=120)
    
               #easygui.msgbox("Wait for backup to complete!", title="Backing up")
               #bckup.backup_data.exportdata("violations", db, df_violations)
               #bckup.backup_data.exportdata("inspections", db, df_inspections)
               easygui.msgbox("Processing done!", title="Processing done")
          
           else:
               easygui.msgbox("Please input integers >= 0!", title="Wrong input")
       
       else:
           easygui.msgbox("Please make sure all data is in the database, you might need to redo LOAD/UPDATE DATA", title="Missing Collection in MongoDB")
       
       
process()       
        
    
    
