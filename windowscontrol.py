# This script restarts the mainscript.py if the script is not running anymore

import psutil
import time
import os


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
 
    listOfProcessObjects = []
 
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in proc.name().lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
 
    return listOfProcessObjects;

#check if the main python script "mainscript" is running counting the running python process IDs, if not then start the mainscript.py

while(True):  
    if checkIfProcessRunning('py'):
        print('Yes a frame process was running')
    else:
        print('No frame process was running')
        

    listOfProcessIds = findProcessIdByName('py')
 
    if len(listOfProcessIds) > 0:
       print('Process Exists | PID and other details are')
       print(len(listOfProcessIds))
       for elem in listOfProcessIds:
           processID = elem['pid']
           processName = elem['name']
           processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
           print((processID ,processName,processCreationTime ))
        
    else :
       print('No Running Process found with given text')

#the len of process IDs to check is to configure, maybe there are other python processes running. 
    if len(listOfProcessIds) < 4:
      os.system('python mainscript.py')
