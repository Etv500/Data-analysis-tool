import os
import easygui
import IMPORT_DATA as mymo 

class backup_data:

    def exportdata(collectname: str, db, df):
        filespath = mymo.mainpath()  
        collectname = collectname
        df=df
        db[collectname].drop() 
        coll = db[collectname]
        coll.insert_many(df.to_dict(orient='records'))
        os.system('cmd /c "mongoexport --host="localhost" --port=27017 --collection='+collectname+' --db=Summative09 --out='+collectname+'.json"')
     
backup_data()