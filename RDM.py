import requests, re, datetime
from requests.auth import HTTPBasicAuth

s = requests.session()

class RDM:
    def __init__(self, url=None, usr=None, pwd=None):
        self.url = url
        self.usr = usr
        self.pwd = pwd
        self.get_data = url + '/api/get_data'
        self.devices = self.get_data + '?=show_devices=true'
        self.instances = self.get_data + '?=show_instances=true'
        self.queue = self.get_data +'?=show_ivqueue=true'
        self.assign = url + '/dashboard/device/assign/'
        
    def setHeaders(self):
        try:
            resp = s.get(self.get_data, auth=(self.usr,self.pwd))
            exp = "(?<=CSRF-TOKEN=).{36}"
            self.csrf = re.search(exp, str(resp.headers)).group()
            exp = "(?<=SESSION-TOKEN=).{36}"
            self.session = re.search(exp,str(resp.headers)).group()
            if self.csrf != None and self.session != None:
                self.mockHeaders = {"Content-Type":"application/x-www-form-urlencoded","Origin": self.url, "Cookie": "SESSION-TOKEN="+self.session+";CSRF-TOKEN="+self.csrf}
                self.realHeaders = {"Content-Type":"application/json","Origin": self.url, "Cookie": "SESSION-TOKEN="+self.session+";CSRF-TOKEN="+self.csrf}
                print("SESSION-TOKEN Set to {0} \nCSRF-TOKEN Set to {1}".format(self.session,self.csrf))
            else:
                print("CSRF and Session Tokens are Null, Somethings fucked, Headers not set")
        except requests.exceptions.RequestException as e:
            print(e)

    def show_devices(self):
        resp = s.get(self.devices, auth=(self.usr,self.pwd))
        data = resp.json()['data']['devices']
        for i in data:
            i['last_seen'] = formatTimestamp(i['last_seen'])
        return(data)
        
    def show_instances(self):
        resp = s.get(self.instances, auth = (self.usr,self.pwd))
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

    def show_ivqueue(self, instance, formatted="false"):
        resp = s.get(self.queue + "&formatted=" + str(formatted) + "&instance=" + str(instance), auth=(self.usr,self.pwd))
        data = resp.json()
        ### Forgot and deleted all my temp IV Instances, will finish this once i remember to make a dummy one ####
        return data
        

    def assignDevice(self,device,instance):
        body = "instance=" + instance + "&_csrf=" + self.csrf
        try:
            print("Assigning {0} to instance {1}".format(device,instance_))
            resp = s.post(self.assign + device, headers=self.mockHeaders, data = body)
            print("Assignment change for {0} succeeded".format(device))
        except requests.exceptions.RequestException as e:
            print("Device Assignment Failed, Reference Error. \n")
            print(e)

    def assignDevices(self, assignments = [], *args):
        for assignment in assignments:
            self.assignDevice(assignment['device'],assignment['instance'])
			
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
