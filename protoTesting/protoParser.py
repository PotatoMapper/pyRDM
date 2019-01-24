from datetime import datetime, timedelta
import json
import s2sphere
import numpy as np


from base64 import b64decode
from google.protobuf.json_format import MessageToJson

from pogoprotos.networking.responses.get_map_objects_response_pb2 import GetMapObjectsResponse
from pogoprotos.networking.responses.encounter_response_pb2 import EncounterResponse
from pogoprotos.networking.responses.fort_search_response_pb2 import FortSearchResponse
from pogoprotos.networking.responses.fort_details_response_pb2 import FortDetailsResponse
from pogoprotos.networking.responses.gym_get_info_response_pb2 import GymGetInfoResponse

class s2cell:
    def __init__(self, cell_id):
        self.cell_id = cell_id
        self.cell_level = s2sphere.CellId(self.cell_id).level()
        self.cell_lat = s2sphere.CellId(self.cell_id).to_lat_lng().lat().degrees
        self.cell_lon = s2sphere.CellId(self.cell_id).to_lat_lng().lng().degrees



def getData(raw_resp):
    latTarget = raw_resp['latitude']
    lonTarget = raw_resp['longitude']
    level = raw_resp['trainerlvl']
    time_recieved = raw_resp['timestamp']

    #Create a list of Dictionarys for each possible response situation, and populate them as needed
    wildPokemons = []
    nearbyPokemons = []
    forts = []
    fortDetails = []
    quests = []
    encounters = []
    cells = [] 

    proto_list = raw_resp['protos']
    ## Protos becomes a list of dictionarys containing (ProtoType):(raw Proto String)
    for proto in proto_list:
        if "GetMapObjects" in proto:
            try:
                gmo_raw = proto['GetMapObjects']
                gmo_string = b64decode(gmo_raw)
                GMO = GetMapObjectsResponse()
                gmo = GMO.FromString(gmo_string)

                for mapCell in gmo.map_cells:
                    for wild_Pokemons in mapCell.wild_pokemons:
                        wildPokemons.append({'cell': mapCell.s2_cell_id, 'data': wild_Pokemons})
                    for nearby_Pokemons in mapCell.nearby_pokemons:
                        nearbyPokemons.append({'cell': mapCell.s2_cell_id, 'data': nearby_Pokemons})
                    for fort in mapCell.forts:
                        forts.append({'cell': mapCell.s2_cell_id, 'data': fort})
                    cells.append(mapCell.s2_cell_id)
                return(wildPokemons,nearbyPokemons,forts,cells,gmo)
            except:
                print("Now you fucked up")

testGMO = {"protos":[{"GetMapObjects":"ChIIgICAgPSz54uIARCmz8HEhy0KEgiAgICA\/LPni4gBEKbPwcSHLQpKCICAgIDss+eLiAEQps\/BxIctWhII3wIZYiC5FFRDhwsyBBACIB1aEAjNAhmOzj5Bu6RW7jICEAJaEAiwAhlNmxd1MYZjwTICEAEKEgiAgICA5LPni4gBEKbPwcSHLQoSCICAgIDcs+eLiAEQps\/BxIctChIIgICAgNSz54uIARCmz8HEhy0KvgEIgICAgMSz54uIARCmz8HEhy0qRgkfURjfZfQH4BCmz8HEhy0ZFHkmMxEiRUAhTngiUpJlVcAqCzg4MTc5ZDljMjAzOgoQ3wKiAgQQASAdWNmwvrv4\/\/\/\/\/wFSPAoLODgxNzlkOWMyMDMRH1EY32X0B+AY3wIg\/\/\/\/\/\/\/\/\/\/\/\/ASkUeSYzESJFQDFOeCJSkmVVwDoEEAEgHVoSCN8CGR9RGN9l9AfgMgQQASAdWhAIvgIZXAueZspFghUyAhACChIIgICAgMyz54uIARCmz8HEhy0KEgiAgICAtLPni4gBEKbPwcSHLQo2CICAgIC8s+eLiAEQps\/BxIctWhAIiQIZFSZxPihAIf0yAhABWhAI4QIZVbozeHzWJRMyAhABChIIgICAgKSz54uIARCmz8HEhy0KEgiAgICArLPni4gBEKbPwcSHLQoSCICAgICUs+eLiAEQps\/BxIctChIIgICAgJyz54uIARCmz8HEhy0KEgiAgICAhLPni4gBEKbPwcSHLQoSCICAgICMs+eLiAEQps\/BxIctChIIgICAgNSw54uIARCmz8HEhy0KEgiAgICAzLDni4gBEKbPwcSHLQoSCICAgIDEsOeLiAEQps\/BxIctChIIgICAgLSw54uIARCmz8HEhy0KEgiAgICAvLDni4gBEKbPwcSHLQpZCICAgICksOeLiAEQps\/BxIctGkUKI2I1ZDY2N2IwMGI4NDQ1YzU5Yjg2ZGQzYTE4ODQ4OTRiLjEyEMS+mKf6LBld\/G1PkCJFQCFIpdjROGZVwEABSAGwAQEKEgiAgICArLDni4gBEKbPwcSHLQoSCICAgICsoeeLiAEQps\/BxIctChIIgICAgPyu54uIARCmz8HEhy0K1gMIgICAgOSu54uIARCmz8HEhy0aYwojMTAxMTM1MGFhZmJlNDY1NGExYzgwZTViYTk1ODFkODkuMTYQ0s7Ms4ctGei+nNmuIkVAIZ30vvG1ZVXAKAMw0wJAAZIBAhABmAEBqgEIELIXKJmAwzW4AbibnI+HLfgBARpFCiM2NWYxMjk1MTQ1MTQ0OTllOWMxMzI3ZWVlYzIyYjk3ZC4xNhDtnfijhC0ZSl0yjpEiRUAhPbX66qplVcBAAUgBsAEBIhIRtA+j1JgiRUAZE6cx+a1lVcAiEhHHPsxPliJFQBkTpzH5rWVVwCISEdYsErGTIkVAGVzYGaisZVXAIhIRzVtGwY4iRUAZE6cx+a1lVcAiEhGs\/Av1jiJFQBnv4GCbsGVVwCISERSWbCWoIkVAGe\/gYJuwZVXAIhIRhjhPP6giRUAZFEx47LFlVcAiEhHqDgMipiJFQBm\/rNQwt2VVwCISESjzIAimIkVAGV7Gvd+1ZVXAIhIREJmtK6siRUAZv6zUMLdlVcAiEhGPcLDnryJFQBkIlo89s2VVwCISES7RkgGwIkVAGcu+po60ZVXAIhIRJKEWL60iRUAZ7+Bgm7BlVcAiEhGfSuuzryJFQBnv4GCbsGVVwAoSCICAgIDUrueLiAEQps\/BxIctChIIgICAgNyu54uIARCmz8HEhy0KfQiAgICAhK\/ni4gBEKbPwcSHLRppCiNiY2VkMmQ4YmQyODI0NzM2OTU0N2JlZDBlNjI1YjJhYy4xNhCV1LfChy0Z84++SdMiRUAhTPvm\/uplVcAoAjD4AUABkgECEAGYAQGqAREQg18ZAAAA4Osn2z8og4rJFbgBlJ6Ur4ctChIIgICAgKS054uIARCmz8HEhy0KJgiAgICAnLTni4gBEKbPwcSHLSISEbtr7QIZIkVAGU+FuZQSZVXAChIIgICAgIS054uIARCmz8HEhy0QARgCIhgIgICAgICg54uIARIFCAMwqQEaAggEIgA="}],"submit_version":3,"longitude":"-85.587710","uuid":"39E1811B-CA17-4D63-8988-6969F4k3DEETS","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.266056","trainerlvl":30,"timestamp":1548210956.3161368}
