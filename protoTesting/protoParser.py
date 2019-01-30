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

    #Create a list of GMO Objects for each possible response situation, and populate them
    forts = []
    cells = []
    quests = []
    encounters = []
    fortDetails = []
    wildPokemons = []
    nearbyPokemons = []
    catchablePokemons = []

    proto_list = raw_resp['protos']
    ## Protos becomes a list of dictionarys containing (ProtoType):(raw Proto String)
    for proto in proto_list:
        if "GetMapObjects" in proto:
            try:
                raw_gmo = proto['GetMapObjects']
                gmo_string = b64decode(raw_gmo)
                GMO = GetMapObjectsResponse()
                gmo = GMO.FromString(gmo_string)

                for mapCell in gmo.map_cells:
                    for wild_Pokemons in mapCell.wild_pokemons:
                        wildPokemons.append({'cell': mapCell.s2_cell_id, 'data': wild_Pokemons})
                    for nearby_Pokemons in mapCell.nearby_pokemons:
                        nearbyPokemons.append({'cell': mapCell.s2_cell_id, 'data': nearby_Pokemons})
                    for fort in mapCell.forts:
                        forts.append({'cell': mapCell.s2_cell_id, 'data': fort})
                    for catchable_Pokemon in mapCell.catchable_pokemons:
                        catchablePokemons.append({'cell': mapCell.s2_cell_id, 'data': catchable_Pokemon})
                    cells.append(mapCell.s2_cell_id)
                return(wildPokemons,nearbyPokemons,catchablePokemons,forts,cells)
            except:
                print("Broke Something in GMO Parsing")
                
        elif "EncounterResponse" in proto:
            try:
                raw_enc = proto['EncounterResponse']
                enc_string = b64decode(raw_enc)
                EncResp = EncounterResponse()
                encounter = EncounterResponse.FromString(enc_string)
        ## This part Is entirely optional, There won't ever be a situation where there are multiple
        ## encounters in a single response, So its only put into an array for consistency in syntax
                encounters.append(encounter)
                return(encounters)
            except:
                print('Broke something in Encounter Response')


                
testGMO = {"protos":[{"GetMapObjects":"ChIIgICAgPSz54uIARCmz8HEhy0KEgiAgICA\/LPni4gBEKbPwcSHLQpKCICAgIDss+eLiAEQps\/BxIctWhII3wIZYiC5FFRDhwsyBBACIB1aEAjNAhmOzj5Bu6RW7jICEAJaEAiwAhlNmxd1MYZjwTICEAEKEgiAgICA5LPni4gBEKbPwcSHLQoSCICAgIDcs+eLiAEQps\/BxIctChIIgICAgNSz54uIARCmz8HEhy0KvgEIgICAgMSz54uIARCmz8HEhy0qRgkfURjfZfQH4BCmz8HEhy0ZFHkmMxEiRUAhTngiUpJlVcAqCzg4MTc5ZDljMjAzOgoQ3wKiAgQQASAdWNmwvrv4\/\/\/\/\/wFSPAoLODgxNzlkOWMyMDMRH1EY32X0B+AY3wIg\/\/\/\/\/\/\/\/\/\/\/\/ASkUeSYzESJFQDFOeCJSkmVVwDoEEAEgHVoSCN8CGR9RGN9l9AfgMgQQASAdWhAIvgIZXAueZspFghUyAhACChIIgICAgMyz54uIARCmz8HEhy0KEgiAgICAtLPni4gBEKbPwcSHLQo2CICAgIC8s+eLiAEQps\/BxIctWhAIiQIZFSZxPihAIf0yAhABWhAI4QIZVbozeHzWJRMyAhABChIIgICAgKSz54uIARCmz8HEhy0KEgiAgICArLPni4gBEKbPwcSHLQoSCICAgICUs+eLiAEQps\/BxIctChIIgICAgJyz54uIARCmz8HEhy0KEgiAgICAhLPni4gBEKbPwcSHLQoSCICAgICMs+eLiAEQps\/BxIctChIIgICAgNSw54uIARCmz8HEhy0KEgiAgICAzLDni4gBEKbPwcSHLQoSCICAgIDEsOeLiAEQps\/BxIctChIIgICAgLSw54uIARCmz8HEhy0KEgiAgICAvLDni4gBEKbPwcSHLQpZCICAgICksOeLiAEQps\/BxIctGkUKI2I1ZDY2N2IwMGI4NDQ1YzU5Yjg2ZGQzYTE4ODQ4OTRiLjEyEMS+mKf6LBld\/G1PkCJFQCFIpdjROGZVwEABSAGwAQEKEgiAgICArLDni4gBEKbPwcSHLQoSCICAgICsoeeLiAEQps\/BxIctChIIgICAgPyu54uIARCmz8HEhy0K1gMIgICAgOSu54uIARCmz8HEhy0aYwojMTAxMTM1MGFhZmJlNDY1NGExYzgwZTViYTk1ODFkODkuMTYQ0s7Ms4ctGei+nNmuIkVAIZ30vvG1ZVXAKAMw0wJAAZIBAhABmAEBqgEIELIXKJmAwzW4AbibnI+HLfgBARpFCiM2NWYxMjk1MTQ1MTQ0OTllOWMxMzI3ZWVlYzIyYjk3ZC4xNhDtnfijhC0ZSl0yjpEiRUAhPbX66qplVcBAAUgBsAEBIhIRtA+j1JgiRUAZE6cx+a1lVcAiEhHHPsxPliJFQBkTpzH5rWVVwCISEdYsErGTIkVAGVzYGaisZVXAIhIRzVtGwY4iRUAZE6cx+a1lVcAiEhGs\/Av1jiJFQBnv4GCbsGVVwCISERSWbCWoIkVAGe\/gYJuwZVXAIhIRhjhPP6giRUAZFEx47LFlVcAiEhHqDgMipiJFQBm\/rNQwt2VVwCISESjzIAimIkVAGV7Gvd+1ZVXAIhIREJmtK6siRUAZv6zUMLdlVcAiEhGPcLDnryJFQBkIlo89s2VVwCISES7RkgGwIkVAGcu+po60ZVXAIhIRJKEWL60iRUAZ7+Bgm7BlVcAiEhGfSuuzryJFQBnv4GCbsGVVwAoSCICAgIDUrueLiAEQps\/BxIctChIIgICAgNyu54uIARCmz8HEhy0KfQiAgICAhK\/ni4gBEKbPwcSHLRppCiNiY2VkMmQ4YmQyODI0NzM2OTU0N2JlZDBlNjI1YjJhYy4xNhCV1LfChy0Z84++SdMiRUAhTPvm\/uplVcAoAjD4AUABkgECEAGYAQGqAREQg18ZAAAA4Osn2z8og4rJFbgBlJ6Ur4ctChIIgICAgKS054uIARCmz8HEhy0KJgiAgICAnLTni4gBEKbPwcSHLSISEbtr7QIZIkVAGU+FuZQSZVXAChIIgICAgIS054uIARCmz8HEhy0QARgCIhgIgICAgICg54uIARIFCAMwqQEaAggEIgA="}],"submit_version":3,"longitude":"-85.587710","uuid":"39E1811B-CA17-4D63-8988-6969F4k3DEETS","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.266056","trainerlvl":30,"timestamp":1548210956.3161368}
testEncounterResponse = {"protos":[{"EncounterResponse":"Cl8JeVPLVxlbO3sQ76fP54ktGRCHoQ98IUVAIQWGnLyLZVXAKgs4ODE3OWQ5OTg5MzouELwCGIQDIGUoZTDeATgSfTj14T6FAQqMQEGIAQSQAQiYAQKlATsQFT+iAgIQARgBIhMKAwECAxIMcNPbPsOkET+Uoiw\/MAU="}],"submit_version":3,"longitude":"-85.586878","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.261910","trainerlvl":27,"timestamp":1548821452.035928}
testFortDetailsResponse = {"protos":[{"FortDetailsResponse":"CiM0M2QzOGMzYjg3YTM0ZTliYTkwM2IwZjU4ZmJkMWY2ZS4xNiIXVHJpbml0eSBSZWZvcm1lZCBDaHVyY2gqaGh0dHA6Ly9saDUuZ2dwaHQuY29tL1dXQXFDV185Q3dVanFFeUhQaFVLd3p5S3o5OHFCZ05GSUZfclhNVnR2TE9TY1hhdXJoVXpfeGRGcTZfMFRDSU5oMDBDc1d0dTBhaDhIdk5rOFJzSAFR9x3DYz8hRUBZDaZh+IhlVcBiP1RyaW5pdHkgcmVmb3JtZWQgY2h1cmNoLiBPcmdhbml6ZWQgaW4gMTkyOSBhbmQgZXJlY3RlZCBpbiAxOTU1LoIBAA=="}],"submit_version":3,"longitude":"-85.586450","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.259965","trainerlvl":27,"timestamp":1548821618.3672929}
testFortSearchResponse = {"protos":[{"FortSearchResponse":"CAESBAgBEAESBAgBEAESBAgBEAESBAgBEAEoMjCg2e\/niS04AUoGCgQIASgEaiM0M2QzOGMzYjg3YTM0ZTliYTkwM2IwZjU4ZmJkMWY2ZS4xNnL\/AQq0AQgEIgCiBi5DSEFMTEVOR0VfQ0FUQ0hfRUFTWV9QS01OOi03MjAwNjk3MDU3NzY0NDM0NTk5qAbZuoDG1IX\/iJwBsAYCugYZQ0hBTExFTkdFX0NBVENIX0VBU1lfUEtNTsoGAhAK0AYB2gYHCAdCAwiBAeAGxLHd54kt6AbEsd3niS36BiM0M2QzOGMzYjg3YTM0ZTliYTkwM2IwZjU4ZmJkMWY2ZS4xNpgHgICAgICg54uIARJGEgoKAS4QARoBLiABGhpxdWVzdF9jYXRjaF9wb2tlbW9uX3BsdXJhbCIacXVlc3RfY2F0Y2hfcG9rZW1vbl9wbHVyYWwoAQ=="}],"submit_version":3,"longitude":"-85.586430","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.260006","trainerlvl":27,"timestamp":1548821682.6647511}
testGymGetInfoResponse = {"protos":[{"GymGetInfoResponse":"CrkMCm4KIzEwMTEzNTBhYWZiZTQ2NTRhMWM4MGU1YmE5NTgxZDg5LjE2EL2+oOaJLRnovpzZriJFQCGd9L7xtWVVwCgBMMwDQAGSAQIQApgBAaoBExCqFRkAAADg047uPyADKOfimwO4AeGq8OSJLfgBARL1AwrFAQpUCXguyI1tSWmLEJQBGK8FIKgBKKgBMMwBOA1KCU1hc3RyaW9sYX3dsVtAhQEmUydBkAEGmAEEpQEBnAc\/qAED0AGx8fPLnCzoAQH4AQGiAgQQARgBELvK0uSJLRi7BSEAAABg\/VTvPyivBTWamRk+QgoNoAKrPBAMGMAFQgoNoAKrPBAMGMIFQgoNoAKrPBAMGL0FQgoNoAKrPBAMGMQFQgoNoAKrPBAMGMEFQgoNoAKrPBAMGL8FQgoNoAKrPBAMGL4FEgcIAyDn4psDGqECCglNYXN0cmlvbGEQKBqEAloXQVZBVEFSX21faGFpcl9kZWZhdWx0XzFiF0FWQVRBUl9tX3NoaXJ0X2dlbmdhcl8wahtBVkFUQVJfbV9wYW50c190ZWFtcm9ja2V0XzByHEFWQVRBUl9tX2hhdF90ZWFtbGVhZGVyY2FwXzJ6GEFWQVRBUl9tX3Nob2VzX2RlZmF1bHRfM4IBD0FWQVRBUl9tX2V5ZXNfNIoBGkFWQVRBUl9tX2JhY2twYWNrX2dlbmdhcl8wkgEYQVZBVEFSX21fZ2xvdmVzX2pvZ2dlcl8wmgEUQVZBVEFSX21fc29ja3NfZW1wdHmqARlBVkFUQVJfbV9nbGFzc2VzX2pvZ2dlcl8wIAEowrUBQARQxtKTKhKXBArFAQpUCV1GMlf+A\/2zEJMBGKwEIJYBKJYBMMwBOA1KCTQyMExhYlJhdH1DogZAhQFWAJNAiAEPkAEKmAEEpQEekRs\/qAED0AHsuaTOnCzoAQGiAgQQARgBEK\/L0+SJLRi0BCEAAAAgYWrvPyisBDWamRk+QgoN4J6VPBAIGMAFQgoN4J6VPBAIGMIFQgoN4J6VPBAIGL0FQgoN4J6VPBAIGMQFQgoN4J6VPBAIGMEFQgoN4J6VPBAIGL8FQgoN4J6VPBAIGL4FEgcIAiDz4ZoDGsMCCgk0MjBMYWJSYXQQKBqmAkABWhdBVkFUQVJfZl9oYWlyX2RlZmF1bHRfMGIXQVZBVEFSX2Zfc2hpcnRfZ2VuZ2FyXzBqG0FWQVRBUl9mX3BhbnRzX3RlYW1yb2NrZXRfMHIVQVZBVEFSX2ZfaGF0X2dlbmdhcl8wehtBVkFUQVJfZl9zaG9lc190ZWFtcm9ja2V0XzCCAQ9BVkFUQVJfZl9leWVzXzCKARpBVkFUQVJfZl9iYWNrcGFja19nZW5nYXJfMJIBHEFWQVRBUl9mX2dsb3Zlc190ZWFtcm9ja2V0XzCaARhBVkFUQVJfZl9zb2Nrc19kZWZhdWx0XzGiARpBVkFUQVJfZl9iZWx0X3RlYW1yb2NrZXRfMLIBGEFWQVRBUl9mX25lY2tsYWNlX3N0YXJfMCABKMGDAUAEUJCSiSEStAMKwgEKUQkDNEquP8S5yRDMAxjPCyCgAiigAjDXATgoSgt4WHhVck0wTXhYeH0bbgtAhQHv2O5CiAEGkAECmAEOpQFh0yc\/qAEC0AGnoNPiiS2iAgIQAhD2haDmiS0YhwwhAAAA4NOO7j8ozws1mpkZPkIKDRCWOD0QOBjABUIKDRCWOD0QOBjCBUIKDRCWOD0QOBi9BUIKDRCWOD0QOBjEBUIKDRCWOD0QOBjBBUIKDRCWOD0QOBi\/BUIKDRCWOD0QOBi+BRIHCAIgrKfOARrjAQoLeFh4VXJNME14WHgQGRrGASADMAQ4A0gCUANiGEFWQVRBUl9tX3NoaXJ0X2RlZmF1bHRfM2oYQVZBVEFSX21fcGFudHNfZGVmYXVsdF8wchZBVkFUQVJfbV9oYXRfbWltaWt5dV8wigEbQVZBVEFSX21fYmFja3BhY2tfZGVmYXVsdF8zkgEZQVZBVEFSX21fZ2xvdmVzX2RlZmF1bHRfM5oBGEFWQVRBUl9tX3NvY2tzX2RlZmF1bHRfM6oBGEFWQVRBUl9tX2dsYXNzZXNfdGhpY2tfMyABKLMBQAFQ0PM2EgpDcmFuZSBQYXJrGmtodHRwOi8vbGg2LmdncGh0LmNvbS9NTU94WHVCVkZlZHlUb3VYaFAwbTRnX2R0Qi1WRTYtcjlFWXpIc29hV3gtOUpucElNOHVQSlVYcVpGMVNDWVJVaVc3U1RkZm9SdmhyNTE2Uk1DMkRzdyABSgBSCQgDGAEgAzCGAg=="}],"submit_version":3,"longitude":"-85.587938","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.266441","trainerlvl":27,"timestamp":1548821961.6068799}
