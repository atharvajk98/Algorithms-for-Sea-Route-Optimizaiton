#!/usr/bin/env python
# coding: utf-8
# pylint: disable=no-member


import pandas as pd 
import numpy as np 
import urllib.request #to make a http request 
import schedule       
import datetime 
import time
from datetime import date
import traceback
import platform
import sys
import os
import configparser
import logging
import logging.config
import optparse
from motu_utils import utils_configpath,utils_log,utils_messages,motu_api
# the config file to load from
CFG_FILE = '~/motuclient/motuclient-python.ini'
LOG_CFG_FILE = './motu_utils/cfg/log.ini'
SECTION = 'Main' #section in the configuration file 
LIBRARIES_PATH ="/home/omkar/anaconda3/envs/shipr/lib/python3.8/site-packages/motu_utils" #(optional)path to the library used-motu-client library 
sys.path.append(LIBRARIES_PATH)


# error code to use when exiting after exception catch
ERROR_CODE_EXIT=1

# shared variables to download
_variables = []


# In[3]:


def check(date,time,source):
    """function to  check the data enterted is valid """
    
    if source != None :
        source.replace(" ","")
        if source != "gfs" and source!= "ww3" and source != "copernicus" :
            raise Exception("Source should be gfs or ww3 or copernicus")
    #check the valid date is entered and in correct format 
    if date==None:
        raise Exception("date cannot be empty")
    else:
        
        try:
            date_obj=datetime.datetime.strptime(date, '%Y%m%d')
            if source == 'gfs' or source=='ww3':
                if source == 'gfs':
                    date_max=date_obj + datetime.timedelta(days=15)
                if source == 'ww3':
                    date_max=date_obj + datetime.timedelta(days=6)
                date_obj=date_obj.strftime("%Y%m%d")
                date_max=date_max.strftime("%Y%m%d")
            if source =='copernicus':
                date_max = date_obj + datetime.timedelta(days=9)
                date_obj=date_obj.strftime("%Y-%m-%d")
                date_max=date_max.strftime("%Y-%m-%d")
                print(date_max)
        except ValueError:
            raise ValueError("Incorrect data format")
    
    
    if time != None:
        if time!="00" and time!="06" and time!="12" and time!= "18":
            raise Exception("Time should be 00,06,12,18 any other values are not accepted")
   
    
    
    return date_obj,date_max,True 


# In[4]:




def create_config_file(date_min,date_max):
    '''function to generate configuration file'''
    
    
    Config = configparser.ConfigParser()
    path="/home/omkar/weatherData/date_min-"+date_min+"date_max-"+date_max+"-netcdf_config.ini"
    cfgfile=open("/home/omkar/weatherData/date_min-"+date_min+"date_max-"+date_max+"-netcdf_config.ini",'w') #specifiy the path 
    Config.add_section('Main')
    Config.set('Main','user','nkulkarni')
    Config.set('Main','pwd','Shridhar321!!')
    Config.set('Main','motu','http://nrt.cmems-du.eu/motu-web/Motu ')
    Config.set('Main','service_id','GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS ')
    Config.set('Main','product_id','global-analysis-forecast-phy-001-024')
    Config.set('Main','date_min',date_min)
    Config.set('Main','date_max',date_max)
    Config.set('Main','latitude_min',"-80")
    Config.set('Main','latitude_max',"90")
    Config.set('Main','longitude_min',"-180")
    Config.set('Main','longitude_max',"179")
    Config.set('Main','depth_min','0.493')
    Config.set('Main','depth_max','0.4942')
    Config.set('Main','variable','thetao,uo,vo,siconc,sithick' )
    Config.set('Main','out_dir','/home/omkar/weatherData/')
    Config.set('Main','out_name','test.nc')
    Config.set('Main','socket_timeout','120000')
    Config.write(cfgfile)
    cfgfile.close()
    return path 
    
    


# In[5]:



def get_client_version():
    """Return the version (as a string) of this client.

    The value is automatically set by the maven processing build, so don't
    touch it unless you know what you are doing."""
    return motu_api.get_client_version()

def get_client_artefact():
    """Return the artifact identifier (as a string) of this client.

    The value is automatically set by the maven processing build, so don't
    touch it unless you know what you are doing."""
    return motu_api.get_client_artefact()

def option_callback_variable(option, opt, value, parser):
    global _variables
    _variables.append(value)
    setattr(parser.values, option.dest, _variables)


# In[6]:


def load_options(path_to_config_file):
    """load options to handle"""
    import configparser
    _options = None

    # create option parser
    parser = optparse.OptionParser(version=get_client_artefact() + ' v' + get_client_version())

    # add available options
    parser.add_option( '--quiet', '-q',
                       help = "prevent any output in stdout",
                       action = 'store_const',
                       const = logging.WARN,
                       dest='log_level')

    parser.add_option( '--verbose',
                       help = "print information in stdout",
                       action='store_const',
                       const = logging.DEBUG,
                       dest='log_level')

    parser.add_option( '--noisy',
                       help = "print more information (traces) in stdout",
                       action='store_const',
                       const = utils_log.TRACE_LEVEL,
                       dest='log_level')

    parser.add_option( '--user', '-u',
                       help = "the user name (string)")

    parser.add_option( '--pwd', '-p',
                       help = "the user password (string)")

    parser.add_option( '--auth-mode',
                       default = motu_api.AUTHENTICATION_MODE_CAS,
                       help = "the authentication mode: '" + motu_api.AUTHENTICATION_MODE_NONE  +
                              "' (for no authentication), '"+ motu_api.AUTHENTICATION_MODE_BASIC +
                              "' (for basic authentication), or '"+motu_api.AUTHENTICATION_MODE_CAS +
                              "' (for Central Authentication Service) [default: %default]")

    parser.add_option( '--proxy-server',
                       help = "the proxy server (url)")

    parser.add_option( '--proxy-user',
                       help = "the proxy user (string)")

    parser.add_option( '--proxy-pwd',
                       help = "the proxy password (string)")

    parser.add_option( '--motu', '-m',
                       help = "the motu server to use (url)")

    parser.add_option( '--service-id', '-s',
                       help = "The service identifier (string)")

    parser.add_option( '--product-id', '-d',
                       help = "The product (data set) to download (string)")

    parser.add_option( '--date-min', '-t',
                       help = "The min date with optional hour resolution (string following format YYYY-MM-DD [HH:MM:SS])")

    parser.add_option( '--date-max', '-T',
                       help = "The max date with optional hour resolution (string following format YYYY-MM-DD [HH:MM:SS])",
                       default = datetime.date.today().isoformat())

    parser.add_option( '--latitude-min', '-y',
                       type = 'float',
                       help = "The min latitude (float in the interval [-90 ; 90])")

    parser.add_option( '--latitude-max', '-Y',
                       type = 'float',
                       help = "The max latitude (float in the interval [-90 ; 90])")

    parser.add_option( '--longitude-min', '-x',
                       type = 'float',
                       help = "The min longitude (float in the interval [-180 ; 180])")

    parser.add_option( '--longitude-max', '-X',
                       type = 'float',
                       help = "The max longitude (float in the interval [-180 ; 180])")

    parser.add_option( '--depth-min', '-z',
                       type = 'string',
                       help = "The min depth (float in the interval [0 ; 2e31] or string 'Surface')")

    parser.add_option( '--depth-max', '-Z',
                       type = 'string',
                       help = "The max depth (float in the interval [0 ; 2e31] or string 'Surface')")

    parser.add_option( '--variable', '-v',
                       help = "The variable (list of strings)",
                       callback=option_callback_variable,
                       dest="variable",
                       type="string",
                       action="callback")

    parser.add_option( '--sync-mode', '-S',
                       help = "Sets the download mode to synchronous (not recommended)",
                       action='store_true',
                       dest='sync')

    parser.add_option( '--describe-product', '-D',
                       help = "Get all updated information on a dataset. Output is in XML format",
                       action='store_true',
                       dest='describe')

    parser.add_option( '--size',
                       help = "Get the size of an extraction. Output is in XML format",
                       action='store_true',
                       dest='size')

    parser.add_option( '--out-dir', '-o',
                       help = "The output dir where result (download file) is written (string). If it starts with 'console', behaviour is the same as with --console-mode. ",
                       default=".")

    parser.add_option( '--out-name', '-f',
                       help = "The output file name (string)",
                       default="data.nc")

    parser.add_option( '--block-size',
                       type = 'int',
                       help = "The block used to download file (integer expressing bytes)",
                       default="65536")

    parser.add_option( '--socket-timeout',
                       type = 'float',
                       help = "Set a timeout on blocking socket operations (float expressing seconds)")
    parser.add_option( '--user-agent',
                       help = "Set the identification string (user-agent) for HTTP requests. By default this value is 'Python-urllib/x.x' (where x.x is the version of the python interpreter)")

    parser.add_option( '--outputWritten',
                       help = "Optional parameter used to set the format of the file returned by the download request: netcdf or netcdf4. If not set, netcdf is used.")

    parser.add_option( '--console-mode',
                       help = "Optional parameter used to display result on stdout, either URL path to download extraction file, or the XML content of getSize or describeProduct requests.",
                       action='store_true',
                       dest='console_mode')

    parser.add_option( '--config-file',
                       help = "Path of the optional configuration file [default: %s]" % CFG_FILE,
                       action='append',
                       dest="config_file",
                       type="string")

    # create config parser
    conf_parser = configparser.ConfigParser()

    # read configuration file name from cli arguments or use default
    # cant set default in parser.add_option due to optparse/argparse bug:
    # https://bugs.python.org/issue16399
    
    config_file =path_to_config_file #parser.parse_args()[0].config_file
    
    conf_parser.read(config_file)

    # set default values by picking from the configuration file
    default_values = {}
    default_variables = []
    for option in parser.option_list:
        if (option.dest != None) and conf_parser.has_option(SECTION, option.dest):
            if option.dest == "variable":
                variablesInCfgFile = conf_parser.get(SECTION, option.dest)
                if (not variablesInCfgFile is None) and variablesInCfgFile.strip():
                    allVariablesArray = variablesInCfgFile.split(",")
                    default_variables = default_variables + allVariablesArray
                    default_values[option.dest] = default_variables
            else:
                default_values[option.dest] = conf_parser.get(SECTION, option.dest)
    print(default_values)
    parser.set_defaults( **default_values )
    date_min=conf_parser.get('Main','date_min')
    date_max=conf_parser.get('Main','date_max')
    
    args = ["--out-name", "date_min-"+date_min+"date_max-"+date_max+".nc"] #add the name of the file to which data is to downloaded
    
    return parser.parse_args(args)


# In[8]:


from pymongo import MongoClient
def create_record(filepath,date_min,date_max,actual_date,fetch_date,time,degree,source):
    #create the connection to the dataBase 
    connection=MongoClient("localhost",27017)
    
    
    #connect to weather data database 
    weather_data_db=connection.Weather_Data_db
    
    
    weather_meta_data=weather_data_db.Weather_Meta_Data
    
    
    #create the record to be stored 
    record={
            "File_Path":filepath,
            "Issue_date":date_min,
            "Actual_date":actual_date,
            "Date_Max":date_max,
            "Fetching_Date":fetch_date,
            "Time":time,
            "Data_Resolution":degree,
            "Source":source
        
           }
    print(record)
    weather_meta_data.insert_one(record)
    print("successful")


# In[ ]:




