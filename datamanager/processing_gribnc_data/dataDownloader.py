#!/usr/bin/env python
# coding: utf-8
# pylint: disable=no-member


import pandas as pd 
import numpy as np 
import urllib.request 
import schedule       
import datetime 
import time
from downloadUtils import check,create_record,create_config_file,load_options
from motu_utils import motu_api,utils_log,utils_messages,utils_configpath
import logging
import logging.config
import sys
import traceback

# In[20]:


def download_data(date,time,source):
    """function to download the parameter data in  format"""
    ERROR_CODE_EXIT=1
    #Validating the entered data 
    date,date_max,rs= check(date,time,source)
    print(type(date))
    if rs== True:
        print('downloading')
        
    source=source.replace(" ","")
    #date=datetime.strptime(date)
    f_path="/home/omkar/weatherData"    
    #urls for downloading the data  
    if source== "gfs":
        
        date_cal=datetime.datetime.strptime(date, '%Y%m%d')
        for cnt in range(0,384,3):
            if cnt!=0 and cnt %24== 0:
                date_cal=date_cal + datetime.timedelta(days=1)
            actual_date=date_cal.strftime("%Y%m%d")
            filename="source-"+source+"-date-"+str(actual_date)+"-time-"+time+"-f"+str(cnt%24).zfill(3)+".grib2"
            gfs="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?file=gfs.t"+time+"z.pgrb2full.0p50.f"+str(cnt).zfill(3)+"&lev_500_mb=on&lev_surface=on&var_VIS=on&var_PRES=on&var_UGRD=on&var_VGRD=on&subregion=&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."+str(date)+"%2F"+time
            urllib.request.urlretrieve(gfs,f_path+"/gfs/"+filename)
            if cnt %24== 0:
                today=datetime.datetime.utcnow()                
                today=today.strftime("%Y%m%d")
                recordFilename="source-"+source+"-date-"+str(actual_date)+"-time-"+time+"-f"
                create_record(f_path+"/gfs/"+recordFilename,date,date_max,actual_date,today,time,".50",source)
            
            

    if source== "ww3":
        
        filename="source-"+source+"-date-"+str(date)+"-time-"+time+".grib2"     
        waves="https://nomads.ncep.noaa.gov/cgi-bin/filter_wave.pl?file=multi_1.nww3.t"+time+"z.grib2&lev_surface=on&all_var=on&subregion=&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fmulti_1."+str(date)
        urllib.request.urlretrieve(waves,f_path+"/ww3/"+filename)        
        today=datetime.datetime.utcnow()                
        today=today.strftime("%Y%m%d")
        create_record(f_path+"/ww3/"+filename,date,date_max,None,today,time,".50",source)
    
    if source== "copernicus":
        
        path=create_config_file(date,date_max)
        filename="source-"+source+"-date_min-"+date+"-date_max-"+date_max+".nc"
        date=''.join(e for e in date if e.isalnum())
        date_max=''.join(e for e in date_max if e.isalnum())
        today1=datetime.datetime.utcnow()               
        today1=today1.strftime("%Y%m%d")   
        
        try:
            # we prepare options we want
            _options = load_options(path)[0]
            #_options['out_name']="test.nc"
            #print(_options)
            
            if _options.log_level != None:
                logging.getLogger().setLevel(int(_options.log_level))
       
            #call for the downloading the data from the URl 
            motu_api.execute_request(_options)
            create_record(f_path+filename,date,date_max,today1,date,"12",".33",source)
        except Exception as e:
            print( "Execution failed: %s", e )
            if hasattr(e, 'reason'):
                print( ' . reason: %s', e.reason )
            if hasattr(e, 'code'):
                print( ' . code  %s: ', e.code )
            if hasattr(e, 'read'):
                print( utils_log.TRACE_LEVEL, ' . detail:\n%s', e.read() )
      
            sys.exit(ERROR_CODE_EXIT)

        finally:
            print("sucess")
        
        




