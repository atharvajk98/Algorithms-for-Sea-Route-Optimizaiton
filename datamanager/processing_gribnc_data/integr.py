from dataDownloader import download_data
from pymongo import MongoClient
import datetime

def getDataFileRecord(source, requestedDate,requestedTime):
    currentDate = datetime.datetime.utcnow().strftime("%Y%m%d")
    difference = datetime.datetime.strptime(requestedDate,"%Y%m%d") - datetime.datetime.strptime(currentDate,"%Y%m%d")
    connection=MongoClient("localhost",27017)
    weather_data_db=connection.Weather_Data_db
    weather_meta_data=weather_data_db.Weather_Meta_Data

    if source == "ww3":
        if difference.days > 6:
            return "OUTOFRANGE"
        rec = weather_meta_data.find_one({"Fetching_Date":currentDate,"Issue_date":currentDate,"Source":source,"Date_Max":{"$gte":requestedDate}})
        if rec == None:
            download_data(currentDate,"00","ww3")
            rec = weather_meta_data.find_one({"Fetching_Date":currentDate,"Issue_date":currentDate,"Source":source,"Date_Max":{"$gte":requestedDate}})
        if rec == None:
            return "NOTFOUND"
        return rec


    if source == "gfs":
        if difference.days > 15:
            return "OUTOFRANGE"
        rec = weather_meta_data.find_one({"Fetching_Date":currentDate,"Issue_date":currentDate,"Source":source,"Date_Max":{"$gte":requestedDate},"Actual_date":requestedDate})
        if rec == None:
            download_data(currentDate,"00","gfs")
            rec = weather_meta_data.find_one({"Fetching_Date":currentDate,"Issue_date":currentDate,"Source":source,"Date_Max":{"$gte":requestedDate},"Actual_date":requestedDate})
        if rec == None:
            return "NOTFOUND"
        rec['File_Path'] = rec['File_Path'] + str(requestedTime).zfill(3)+".grib2"
        return rec

    if source == "copernicus":
        rec = weather_meta_data.find_one({"Fetching_Date":currentDate,"Issue_date":currentDate,"Source":source,"Date_Max":{"$gte":requestedDate}})
        if rec == None:
            download_data(currentDate,"00","copernicus")
        rec = weather_meta_data.find_one({"Fetching_Date":currentDate,"Issue_date":currentDate,"Source":source,"Date_Max":{"$gte":requestedDate}})
        if rec == None:
            return "NOTFOUND"
        return rec

