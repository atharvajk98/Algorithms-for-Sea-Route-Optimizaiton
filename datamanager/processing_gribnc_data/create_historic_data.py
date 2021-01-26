#!/usr/bin/env python
# coding: utf-8

# In[12]:


import schedule
import time
from datetime import date
import os 
from glob import glob
    


# In[21]:


def transfer_to_historic():
    
    s_path="D:/internship/Data/latest/"
    d_path='D:/internship/Data/historic/'
    dir=os.listdir(s_path)
    print(dir)
    
    if len(dir)==0:
        print("directory is empty nothing to transfer ")
    else:
        for f in range(len(dir)):
            os.rename((s_path+dir[f]), (d_path+dir[f]))


# In[23]:


schedule.every().day.at("22:40").do(transfer_to_historic)


# In[ ]:


while True:                       
    schedule.run_pending()     # to run the pending tasks if any 
    time.sleep(1)


# In[ ]:




