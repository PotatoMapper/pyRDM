import json

import sys, os
sys.path.append(os.path.realpath('..'))

import Utilities.TSP_Solver
from Utilities.TSP import TSP
from Handlers.DB_Handler import DB_Handler
from Settings import Config
from Misc import get_logger

class Instance(object):

    def __init__(self,*args, **kwargs):
        self.name = kwargs.get('name',None)
        self.type = kwargs.get('type',None)
        self.data = kwargs.get('data',None)
        self.min_level = kwargs.get('min_level',None)
        self.max_level = kwargs.get('max_level',None)
        self.timezone_offset = kwargs.get('timezone_offset',None)
        self.area = kwargs.get('area',None)

    def getByName(self, name=None):

        db = DB_Handler()
        sql = "SELECT * FROM instance WHERE name LIKE \'%{}%\'"

        if not self.name and name:
            params = (str(name))
        elif self.name:
            params = (str(self.name))
        elif not self.name and not name:
            print("You dun goofed Fam, Define Instance().name or pass arg name=''")
            return

        sql = sql.format(params)

        r = db.Query(sql)
        if len(r) == 0:
           print("Error, no instances returned")
           return(None)
        
        elif len(r) == 1:
           name = r['name']
           type = r['type']
           data = r['data']
           min_level = data['min_level']
           max_level = data['max_level']
           timezone_offset = data['timezone_offset']
           area = data['area']
        
           return(Instance(name=name,type=type,data=data,min_level=min_level,max_level=max_level,timezone_offset=timezone_offset,area=area))

        print(sql)
        
    def getAll(self):

        db = DB_Handler()
        all_instances = list()
        sql = "SELECT * FROM instance"

        r = db.Query(sql)
        if len(r) == 0:
           print("Error, no instances returned")
           return(None)
        
        for i in r:
           name = r['name']
           type = r['type']
           data = r['data']
           min_level = data['min_level']
           max_level = data['max_level']
           timezone_offset = data['timezone_offset']
           area = data['area']
        
           tmp = Instance(name=name,type=type,data=data,min_level=min_level,max_level=max_level,timezone_offset=timezone_offset,area=area)
           all_instances.append(tmp)
        
        return(all_instance)

    def TSP(self, plot=False):

        if self.type == "auto_quest":
            print("You can not TSP Auto_Quest or IV_instances")
            return

        points = []

        for i in self.area:
            (lat,lon) = (i['lat'],i['lon'])
            points.append((lat,lon))
        
        solver = TSP(points)
        self.area = solver.Solve()
        self.solver=solver
        print("self.area now TSP'd")
        
                
        

        
        
