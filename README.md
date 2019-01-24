# pyRDM
WIP Module for RDM API Calls and Some extra Non API related interactions (Single/Multi Device Assignment swaps, etc)
Additionally playing with some raw Proto Handling for debugging and investigating useful info for RDM integration

## What and Why?
The pyRDM module is designed to provide a python base RDM class and appropriate methods for easy developement around RDMs current features.

the *requests* package is the only external requirement for pyRDM. All other requirements in the requirements.txt are related to the WIP Proto endpoints.

# Current Support as of 01/23/2019
**Initiate pyRDM object**
``` rdm = RDM(url,usr,pwd) ```
> Where url = http://rdmip:9000, usr = RDM Username, pwd = RDM password

## Available API Calls
- Get Device Status = returns device status 
  - ```devices = RDM.show_devices()```
- Get instance Status = retunes instance status
  - ```instances = RDM.show_instances()```
- Get Instance IV Queue = returns current Queue information
  - ``` Queue = RDM.show_ivqueue(instance as str, formatted as str([boolean])) ```
  -**_Formatted defaults to false, and should be used this way, unless you intend to use a flask template with static image locations that mirror RDM's_**

## Available Non API RDM Controls
**_These calls work by capturing the CSRF and Session Token on Auth with RDM, and then use these to post to particular web endpoints_**
- Before using anything of these calls you must set the header with the following method
  - ```RDM.setHeaders()```
- Change device assignment = pass device name/uuid and instance name as strings
  - ```RDM.assignDevice(device, instance) ```
- Change Multiple Devices Assignments = Pass a list assignments=[] of Dict() in format { 'device': "deviceName/uuid" , 'instance': "InstanceName" }
  - ```RDM.assignDevices(assignments) ```
  
## To Do for pyRDM calls:
- Additional support for RDM Controls
  - Remove device from RDM Backend
  - Clear Quests
  - Add or Remove Auto-Assignments (For those who desire multiple sets of autoassignments for particular days/events/etc)
  - Integrate modified version of Racinels TSP solution ```RDM.TSP(instance, type, minlvl, maxlvl)```
    - The solution will allow you to select existing Instance and type, and perform TSP solution on the route. Prompt provides the ability to automatically add the new instance to RDM with minlvl and maxlvl settings if provided on call
