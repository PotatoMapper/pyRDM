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
                    cells.append(s2Cell(mapCell.s2_cell_id))
                return(wildPokemons,nearbyPokemons,forts,cells,gmo)
            except:
                print("Now you fucked up")
