import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request,\
	make_response, send_from_directory, json, redirect, session
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
                print("we parsed Fine")
    ## Fun stuff happens here now. Look for all the data we need to see if it is present
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

            





raw_resp = {"protos":[{"GetMapObjects":"ChIIgICAgKTS54uIARD5hYPchi0KEgiAgICArNLni4gBEPmFg9yGLQoSCICAgICc0ueLiAEQ+YWD3IYtChIIgICAgPzL54uIARD5hYPchi0KEgiAgICA5Mvni4gBEPmFg9yGLQoSCICAgID00eeLiAEQ+YWD3IYtChIIgICAgPzR54uIARD5hYPchi0KvwMIgICAgOTR54uIARD5hYPchi0aRQojNDlhMWFhMzhmNzBiNGVlOTk3OGQ0ZDEzNGE0M2I0MTAuMTYQyKWugIYtGZuqe2RzG0VAIas\/wjBgY1XAQAFIAbABAVqwAQiUAhViIOFDGZMv4u2wo9hbIiM0OWExYWEzOGY3MGI0ZWU5OTc4ZDRkMTM0YTQzYjQxMC4xNip0aHR0cDovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vRHpyY1JVX3lOUXhGbUh1VmpSQ012cjROVEd3RUtXSGE5b3NsWjladlBpNjh5V0gxd0tUeUdSM3FxWVk4ZlR0aHpueUk1M1ZfSEpiTUNBdmltcWMyAhACWrABCJ0CFWIg4UMZGUfSxMdQUjYiIzQ5YTFhYTM4ZjcwYjRlZTk5NzhkNGQxMzRhNDNiNDEwLjE2KnRodHRwOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9EenJjUlVfeU5ReEZtSHVWalJDTXZyNE5UR3dFS1dIYTlvc2xaOVp2UGk2OHlXSDF3S1R5R1IzcXFZWThmVHRoem55STUzVl9ISmJNQ0F2aW1xYzICEAEKEgiAgICA7NHni4gBEPmFg9yGLQoSCICAgIDU0eeLiAEQ+YWD3IYtChIIgICAgNzR54uIARD5hYPchi0KEgiAgICAxNHni4gBEPmFg9yGLQoSCICAgIDM0eeLiAEQ+YWD3IYtCkgIgICAgLTR54uIARD5hYPchi1aEAjrAhlpfaxy2874UjICEAFaEAiRAhkRaXKja58GLTICEAJaEAiwAhmHSnXs560GPDICEAEKgAYIgICAgLzR54uIARD5hYPchi0qRAl1tu0rhEI8jxD5hYPchi0ZgAzXd0obRUAhrZiJur5jVcAqCzg4MTc5ZThiYjUxOggQuAKiAgIQAliG+vyj+f\/\/\/\/8BKkQJqNoPmeAyA\/kQ+YWD3IYtGZkpW\/1MG0VAIa2Yibq+Y1XAKgs4ODE3OWU4YmI1NzoIEIkCogICEAFYhvr8o\/n\/\/\/\/\/ASo9CXKX88legEd2EPmFg9yGLRl4TLYhRxtFQCFMxUEwtGNVwCoLODgxNzllOGJiOWI6CBCUAqICAhACWNPvAypECRKKnOpXwCLdEPmFg9yGLRkPEeaNVBtFQCGtmIm6vmNVwCoLODgxNzllOGJjYjE6CBC+AqICAhABWIb6\/KP5\/\/\/\/\/wEqRAnMAKECPIx3YBD5hYPchi0ZgiPsmFkbRUAhrZiJur5jVcAqCzg4MTc5ZThiY2M5OggQ1QKiAgIQAViG+vyj+f\/\/\/\/8BUjoKCzg4MTc5ZThiYjUxEXW27SuEQjyPGLgCIP\/\/\/\/\/\/\/\/\/\/\/wEpgAzXd0obRUAxrZiJur5jVcA6AhACUjoKCzg4MTc5ZThiYjU3EajaD5ngMgP5GIkCIP\/\/\/\/\/\/\/\/\/\/\/wEpmSlb\/UwbRUAxrZiJur5jVcA6AhABUjYKCzg4MTc5ZThiYjliEXKX88legEd2GJQCIMz1htyGLSl4TLYhRxtFQDFMxUEwtGNVwDoCEAJSOgoLODgxNzllOGJjYjEREoqc6lfAIt0YvgIg\/\/\/\/\/\/\/\/\/\/\/\/ASkPEeaNVBtFQDGtmIm6vmNVwDoCEAFSOgoLODgxNzllOGJjYzkRzAChAjyMd2AY1QIg\/\/\/\/\/\/\/\/\/\/\/\/ASmCI+yYWRtFQDGtmIm6vmNVwDoCEAFaEQgrGVQJ+biUvxaMMgQQAigEWhAIqwIZ+ES1LqODtPwyAhABWhAIvgIZGXz0YpTvo8oyAhACWhIIuwIZ5M1o+znzOAUyBBABKARaEAiHAhmaYWuRmul64jICEAFaEAiCAhlQug+mOIloOzICEAEKgQIIgICAgKTR54uIARD5hYPchi0aRQojNzA1NWQ3ZTdlZmM3NDdhY2JiZmUyYzAyMGZjM2QxNTUuMTYQvdio7PcsGbCryVNWG0VAIVsiF5zBY1XAQAFIAbABAVqlAQjVAhU4u0RCGe8pDwRk5ypCIiM3MDU1ZDdlN2VmYzc0N2FjYmJmZTJjMDIwZmMzZDE1NS4xNippaHR0cDovL2xoNi5nZ3BodC5jb20vQW1kNVVLTGlzb0ZsQkN4VjlMSEpYaFU5cnZkc0JhR0FmMU52azN6SkdTaFF1WV9EWFV2Q00tS3gxNTN4MFl0NWw5bmlXaVJZeGdJVU94OFJBZS11MgIQAgoSCICAgICs0eeLiAEQ+YWD3IYtClwIgICAgJTR54uIARD5hYPchi1aEAjCAhk6\/pEjgQ9MUzICEAJaEAjrAhmP0iuVqXY5SjICEAJaEAiwAhkhd6HWXOOJ9TICEAJaEgjfAhnJVWoLPmBJUTIEEAIgHQoSCICAgICc0eeLiAEQ+YWD3IYtChIIgICAgITR54uIARD5hYPchi0KEgiAgICAjNHni4gBEPmFg9yGLQoSCICAgIDU3ueLiAEQ+YWD3IYtChIIgICAgMze54uIARD5hYPchi0KEgiAgICAtN7ni4gBEPmFg9yGLQoSCICAgICs3ueLiAEQ+YWD3IYtChIIgICAgLTM54uIARD5hYPchi0KEgiAgICAvMzni4gBEPmFg9yGLQoSCICAgICkzOeLiAEQ+YWD3IYtChIIgICAgKzM54uIARD5hYPchi0KEgiAgICAnMzni4gBEPmFg9yGLQoSCICAgICUzOeLiAEQ+YWD3IYtChIIgICAgITM54uIARD5hYPchi0KEgiAgICAjMzni4gBEPmFg9yGLRABGAEiGgiAgICAgODni4gBEgcIAhgBMOcCGgIIBCIA"}],"submit_version":3,"longitude":"0.000000","uuid":"C762C5D3-DB4B-48DF-A66B-C28858B9B81D","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"0.000000","trainerlvl":30,"timestamp":1547991827.354331}
