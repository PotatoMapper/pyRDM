import requests
import re
import datetime
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')
rdm = conf['RDM']

s = requests.session()

class pyRDM:
    def __init__(self, url=None, usr=None, pwd=None):
        self.url = url
        self.usr = usr
        self.pwd = pwd
        self.get_data = url + '/api/get_data'
        self.callDevices = self.get_data + '?=show_devices=true'
        self.callInstances = self.get_data + '?=show_instances=true'
        self.assign = url + '/dashboard/device/assign/'
        
    def getToken(self):
        
        try:
            resp = s.get(self.get_data, auth=(self.usr,self.pwd))
            exp = "(?<=CSRF-TOKEN=).*(?=;e)"
            self.CSRF = re.search(exp,str(resp.headers)).group()
            exp = "(?<=SESSION-TOKEN=).{36}"
            self.Session = re.search(exp,str(resp.headers)).group()
            if self.CSRF != None and self.Session != None:
                self.headers = {"Content-Type":"application/x-www-form-urlencoded","Origin": self.url, "Cookie": "SESSION-TOKEN="+self.Session+";CSRF-TOKEN="+self.CSRF}
                print("SESSION-TOKEN Set to {0} \nCSRF-TOKEN Set to {1}".format(self.Session,self.CSRF))
            else:
                print("The CSRF or Session Tokens are Null, Header Not Set")
        except requests.exceptions.RequestException as e:
            print(e)

    def Assign(self,device, instance):
        body = "instance="+ instance + "&_csrf="+ self.CSRF
        try:
            print("Assigning {0} to instance {1}".format(device,instance))
            resp = s.post(self.assign + device, headers=self.headers, data = body)
            print("Assigment change for {0} succeeded".format(device)) 
        except requests.exceptions.RequestException as e:
            print("Device Assignment Failed, Reference Error.\n")
            print(e)

    def multiAssign(self, assignments = [], *args):
        for assignment in assignments:
            self.Assign(assignment['device'],assignment['instance'])
            
    
    def getInstances(self):
        resp = s.get(self.callInstances, auth=(self.usr,self.pwd))
        data = resp.json()['data']['instances']
        for i in data:
            try:
                has_status = i['status'] != None
            except KeyError:
                has_status = False
                patchStatus(i)

            if has_status == False:
                i['status'] = "--"
            elif i['type'] == 'Pokemon IV':
                i['status'] = str(i['status']['iv_per_hour']) + " IV/HR"
            elif i['type'] == 'Circle Pokemon':
                i['status'] = str(i['status']['round_time']) + "s Round Time"
            elif i['type'] == 'Circle Raid':
                i['status'] = str(i['status']['round_time']) + "s Round Time"
            elif i['type'] == 'Auto Quest':
                pAttempts = '{0:.2%}'.format(i['status']['quests']['current_count_internal']/i['status']['quests']['total_count'])
                pSuccess = '{0:.2%}'.format(i['status']['quests']['current_count_db']/i['status']['quests']['total_count'])
                i['status'] = str(i['status']['quests']['current_count_internal']) + '|' + str(i['status']['quests']['current_count_db'])+ '/'+ str(i['status']['quests']['total_count']) + ' (' + str(pAttempts) + ')|(' + str(pSuccess) + ')'
        return (data)

    def getDevices(self):
        resp = s.get(self.callDevices, auth=(self.usr,self.pwd))
        data = resp.json()['data']['devices']
        
        for i in data:
            i['last_seen'] = formatTimestamp(i['last_seen']) 
        return (data)

 
def patchStatus(resp):
    key = 'status'
    if key in (resp):
        print('Key Exists')
    else:
        resp['status'] = None

def formatTimestamp(timestamp):
    timestamp = datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%H:%M:%S %m-%d-%y')
    return timestamp


