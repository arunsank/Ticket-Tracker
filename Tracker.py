
#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Created on Wed Apr  6 19:08:33 2017

@author: Arun Ram

This code block is a simple Ticket tracker to track the inflow of tickets on a continuous
basis. This ticket tracker can be extended to track tickets that are active.
Tickets that are assigned to a specific user and also to look at the names 
or IDs of the people who are working on a ticket



"""

#Tested in Python 2.7

#------References for Zendesk---------
#Token -API Key
#NPaR4ifzNpt4Fk0ZlJ3N0J6C6oQU9zowZ9lpGWS9



import sys
"""if int(sys.argv[1]) == 1:
    from pyspark.sql import SparkSession"""

import requests
import subprocess
import pandas as pd
import numpy as np
import json
import os
import threading
from pandas.io.json import json_normalize
import flask
from flask import request
import requests
from requests.auth import HTTPBasicAuth
import ast
import csv
from collections import defaultdict
import time,sched
import datetime


ckr =0 
wdir = os.getcwd()
os.chdir(wdir)
    


def main(argv):
    
    ses = requests.Session()
    
    
    """ MAIN FUNCTION"""
    
    subdomain =sys.argv[1]
    username = sys.argv[2]
    pwd =sys.argv[3]
    
    #recursive (subdomain,username,pwd)
    
    conn_checker = ses.get('https://'+subdomain+'.zendesk.com/api/v2/views.json',auth=(username, pwd))
    
    if (str(conn_checker) == '<Response [200]>'):
        title_dic= get_view_id(subdomain,username,pwd)
        get_view_count(title_dic,subdomain,username,pwd)
    else:
        print ("Authorization restricted, Please check your credentials")
        
        
    ses.close()
    

    
    
def get_view_id(subdomain,username, pwd):
    
    
    """ 
    Input : Subdomain, The domain under which you are going to work in
    
    
    Significant Variables Used - Purpose 
    ses- Session Variable
    resp_view - Response got from views.json
    resp_vtxt - Text from resp_view
    tempV_ls - list containing all views
    Vid_ls - IDs of views in list format 
    
    Ouput :
    
    V_ls - Dictionary containing view keys and  titles as values
       
    """
    
    ses = requests.Session()
    resp_view = ses.get('https://'+subdomain+'.zendesk.com/api/v2/views.json',auth=(username, pwd))
    
    resp_vtxt = resp_view.text
    view_dict = json.loads(resp_vtxt)
   
    tempV_ls =  view_dict['views']
    #Vid_ls = []
    #tup =()
    title_dict= {}
    #ids=[]
    
    
    for i in range (0,len(tempV_ls)):
        temp_V={}
        temp_V= tempV_ls[i]
        title_dict[temp_V['id']] = str(temp_V['raw_title']).strip('{}')
        #tup= (temp_V['id'],str(temp_V['raw_title']).strip('{}'))
        
        
    ses.close()
    return title_dict



def get_view_count(Vid_ls,subdomain,username,pwd):
    
    
    """ Significant Variables Used - Purpose 
    Input : 
    Vid_ls - Dictionary containing View keys and vakues
    sub domain- The domain where Zendesk logs in
    ---------------------------------------------
    id_str - View ids as strings
    resp - response got for count_many.json 
    view_dict - Dictionary format of content from count_many.json
    dict_count - Dictionary containing Views and their respective counts
    
    ---------------------------------------------

    Output 
    The output is the csv file containing view counts
    
    """
    
    ses = requests.Session()
    id_str = list(Vid_ls.keys())
    id_str = str(id_str)
    id_str = id_str.strip('[]')
    resp = ses.get('https://'+subdomain+'.zendesk.com/api/v2/views/count_many.json?ids='+id_str,auth=(username, pwd))
    
    resp_txt = resp.text
    view_dict = json.loads(resp_txt)
    
    dict_count= {}
    Count_ls = view_dict['view_counts']
    
    
    for i in range (0,len(Count_ls)):
        temp_map={}
        temp_map = Count_ls[i]
        dict_count[temp_map['view_id']] =temp_map['value']
        
    #tup= (temp_V['id'],str(temp_V['raw_title']).strip('{}'))
    dict_lookup = defaultdict(list)     
    
    for i in (Vid_ls, dict_count):
        for k, v in i.items():
            dict_lookup[k].append(v)
    
   
            
    
    #Printing for outputting processed file
    with open('Count.csv','w') as file:
        writ= csv.writer(file,delimiter=',')
        writ.writerow(['ViewID','View Title','value'])
        for k, v in dict_lookup.items():
            writ.writerow([k,v[0],v[1]])
        
    
    ses.close()
       
 


if __name__  == "__main__":
    
    if (len(sys.argv)==4):
        main(sys.argv)
    else:
        print (" All inputs are mandatory. Please enter your Subdomain, Username and your password")
    
