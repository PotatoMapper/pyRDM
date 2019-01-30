from datetime import datetime, timedelta
import s2sphere
import numpy as np
from base64 import b64decode

from pogoprotos.networking.responses.get_map_objects_response_pb2 import GetMapObjectsResponse
from pogoprotos.networking.responses.encounter_response_pb2 import EncounterResponse
from pogoprotos.networking.responses.fort_search_response_pb2 import FortSearchResponse
from pogoprotos.networking.responses.fort_details_response_pb2 import FortDetailsResponse
from pogoprotos.networking.responses.gym_get_info_response_pb2 import GymGetInfoResponse

# Started playing with giving everything a dedicated object as I was trying to familiarize myself with SQLAlchemy
# This is more or less useless here, do as you wish
class s2cell:
    def __init__(self, cell_id):
        self.cell_id = cell_id
        self.cell_level = s2sphere.CellId(self.cell_id).level()
        self.cell_lat = s2sphere.CellId(self.cell_id).to_lat_lng().lat().degrees
        self.cell_lon = s2sphere.CellId(self.cell_id).to_lat_lng().lng().degrees



def parseProtos(raw_resp):
    #Always returned after 'Protos': key-pair#
    latTarget = raw_resp['latitude']
    lonTarget = raw_resp['longitude']
    level = raw_resp['trainerlvl']

    # Dont use this for anything, honestly. It appears to be tacked on when sent from ++, compare it to timestamps in protos
    # significant enough delay to say fuck this thing. 
    time_recieved = raw_resp['timestamp']
    #-#
    forts = []
    cells = []
    encounters = []
    wildPokemons = []
    nearbyPokemons = []
    catchablePokemons = []
    #-#
    proto_list = raw_resp['protos']
    #-#
    for proto in proto_list:
        if "GetMapObjects" in proto:
            try:
                raw_gmo = proto['GetMapObjects']
                gmo_str = b64decode(raw_gmo)
                GMO = GetMapObjectsResponse()
                gmo = GMO.FromString(gmo_str)

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
                return(wildPokemons,nearbyPokemons,catchablePokemons,forts,cells, gmo)
            except:
                print("Broke Something in GMO Parsing, seriously, add real debug you cunt")
                
        elif "EncounterResponse" in proto:
            try:
                raw_enc = proto['EncounterResponse']
                enc_str = b64decode(raw_enc)
                EncResp = EncounterResponse()
                encounter = EncounterResponse.FromString(enc_str)
           
                return(encounter)
            except:
                print('Broke something in Encounter Response parsing. You are adopted and no one loves you')

        elif "FortDetailsResponse" in proto:
            try:
                raw_fdr = proto['FortDetailsResponse']
                fdr_str = b64decode(raw_fdr)
                FDR = FortDetailsResponse()
                fdr = FDR.FromString(fdr_str)

                return(fdr)
            except:
                print("broke something in FortDetailsResponse parsing, go add real debug you ugly fuck")

        elif "FortSearchResponse" in proto:
            try:
                raw_fsr = proto['FortSearchResponse']
                fsr_str = b64decode(raw_fsr)
                FSR = FortSearchResponse()
                fsr = FSR.FromString(fsr_str)
                
                return(fsr)
            except:
                print('yada yada Fort Search Response parsing broken, yada yada add debug')
                
        elif "GymGetInfoResponse" in proto:
            try:
                raw_ggir = proto['GymGetInfoResponse']
                ggir_str = b64decode(raw_ggir)
                GGIR = GymGetInfoResponse()
                ggir = GGIR.FromString(ggir_str)

                return(ggir)
            except:
                print('Giggity GymGetInfoResponse parsing is facked')
                
testGMO1 = {"protos":[{"GetMapObjects":"ChIIgICAgKTS54uIARCplsz3iS0KEgiAgICArNLni4gBEKmWzPeJLQoSCICAgICc0ueLiAEQqZbM94ktChIIgICAgPzL54uIARCplsz3iS0KEgiAgICA\/NDni4gBEKmWzPeJLQoSCICAgIDk0OeLiAEQqZbM94ktChIIgICAgPTR54uIARCplsz3iS0KEgiAgICA\/NHni4gBEKmWzPeJLQryBAiAgICA5NHni4gBEKmWzPeJLRpFCiM0OWExYWEzOGY3MGI0ZWU5OTc4ZDRkMTM0YTQzYjQxMC4xNhD9wvb3hy0Zm6p7ZHMbRUAhqz\/CMGBjVcBAAUgBsAEBWrABCKMBFTXP1kMZDxXF65BsnbQiIzQ5YTFhYTM4ZjcwYjRlZTk5NzhkNGQxMzRhNDNiNDEwLjE2KnRodHRwOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9EenJjUlVfeU5ReEZtSHVWalJDTXZyNE5UR3dFS1dIYTlvc2xaOVp2UGk2OHlXSDF3S1R5R1IzcXFZWThmVHRoem55STUzVl9ISmJNQ0F2aW1xYzICEAFasAEIhQIVNc\/WQxmSDlOX5OauByIjNDlhMWFhMzhmNzBiNGVlOTk3OGQ0ZDEzNGE0M2I0MTAuMTYqdGh0dHA6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL0R6cmNSVV95TlF4Rm1IdVZqUkNNdnI0TlRHd0VLV0hhOW9zbFo5WnZQaTY4eVdIMXdLVHlHUjNxcVlZOGZUdGh6bnlJNTNWX0hKYk1DQXZpbXFjMgIQAVqwAQibAhU1z9ZDGfoo9f2\/Pk8GIiM0OWExYWEzOGY3MGI0ZWU5OTc4ZDRkMTM0YTQzYjQxMC4xNip0aHR0cDovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vRHpyY1JVX3lOUXhGbUh1VmpSQ012cjROVEd3RUtXSGE5b3NsWjladlBpNjh5V0gxd0tUeUdSM3FxWVk4ZlR0aHpueUk1M1ZfSEpiTUNBdmltcWMyAhACCiQIgICAgOzR54uIARCplsz3iS1aEAjTAhmSrnvO9IGZ+zICEAIKEgiAgICA1NHni4gBEKmWzPeJLQoSCICAgIDc0eeLiAEQqZbM94ktCiQIgICAgMTR54uIARCplsz3iS1aEAjYARn3eWtqPncEWzICEAIKEgiAgICAzNHni4gBEKmWzPeJLQokCICAgIC00eeLiAEQqZbM94ktWhAIxgEZxrO16YMGguwyAhABCogECICAgIC80eeLiAEQqZbM94ktKj4JiIE2pnNUkvAQqZbM94ktGQ8R5o1UG0VAIa2Yibq+Y1XAKgs4ODE3OWU4YmNiMToHEEWiAgIQAVjW6bOIBio\/CXoLM5q1Au6lEKmWzPeJLRkxi5XdVxtFQCGxD6dUqGNVwCoLODgxNzllOGJlOTc6CBDTAqICAhABWNbps4gGUjkKCzg4MTc5ZThiY2IxEYiBNqZzVJLwGEUg\/\/\/\/\/\/\/\/\/\/\/\/ASkPEeaNVBtFQDGtmIm6vmNVwDoCEAFSOgoLODgxNzllOGJlOTcRegszmrUC7qUY0wIg\/\/\/\/\/\/\/\/\/\/\/\/ASkxi5XdVxtFQDGxD6dUqGNVwDoCEAFaEAjjAhlfJFmE1D4gDzICEAJaDwhWGYvZLUDUAa4ZMgIQAVoPCBcZTr0G6Hk6m8YyAhACWhAIhgMZG8OTHvJKny0yAhABWqQBCEUVE++NQhmIgTamc1SS8CIjNzA1NWQ3ZTdlZmM3NDdhY2JiZmUyYzAyMGZjM2QxNTUuMTYqaWh0dHA6Ly9saDYuZ2dwaHQuY29tL0FtZDVVS0xpc29GbEJDeFY5TEhKWGhVOXJ2ZHNCYUdBZjFOdmszekpHU2hRdVlfRFhVdkNNLUt4MTUzeDBZdDVsOW5pV2lSWXhnSVVPeDhSQWUtdTICEAFaDwgwGW2Fk1qjuWhpMgIQAgqAAgiAgICApNHni4gBEKmWzPeJLRpFCiM3MDU1ZDdlN2VmYzc0N2FjYmJmZTJjMDIwZmMzZDE1NS4xNhC92Kjs9ywZsKvJU1YbRUAhWyIXnMFjVcBAAUgBsAEBWqQBCG8VE++NQhmmcirQA\/dxZCIjNzA1NWQ3ZTdlZmM3NDdhY2JiZmUyYzAyMGZjM2QxNTUuMTYqaWh0dHA6Ly9saDYuZ2dwaHQuY29tL0FtZDVVS0xpc29GbEJDeFY5TEhKWGhVOXJ2ZHNCYUdBZjFOdmszekpHU2hRdVlfRFhVdkNNLUt4MTUzeDBZdDVsOW5pV2lSWXhnSVVPeDhSQWUtdTICEAIKEgiAgICArNHni4gBEKmWzPeJLQqDAQiAgICAlNHni4gBEKmWzPeJLVoQCIABGZTSQQ8j9LFCMgIQAVoQCKUBGfAXttxzjkSlMgIQAloPCDAZnqlEDBi0r3wyAhABWhII3AEZNUzTq+uJJmIyBBACKAZaEgjrAhlH1ss\/nL79\/zIEEAIoBloSCOsCGUGI3eBkjdSbMgQQAigGChIIgICAgJzR54uIARCplsz3iS0KEgiAgICAhNHni4gBEKmWzPeJLQoSCICAgICM0eeLiAEQqZbM94ktChIIgICAgNTe54uIARCplsz3iS0KEgiAgICAzN7ni4gBEKmWzPeJLQoSCICAgIC03ueLiAEQqZbM94ktChIIgICAgKze54uIARCplsz3iS0KEgiAgICAtMzni4gBEKmWzPeJLQoSCICAgIC8zOeLiAEQqZbM94ktChIIgICAgKTM54uIARCplsz3iS0KEgiAgICArMzni4gBEKmWzPeJLQoSCICAgICUzOeLiAEQqZbM94ktChIIgICAgJzM54uIARCplsz3iS0KEgiAgICAhMzni4gBEKmWzPeJLQoSCICAgICMzOeLiAEQqZbM94ktEAEYASIgCICAgICA4OeLiAESCQgDGAEgAjDvARoCCAYiBAgBEAE="}],"submit_version":3,"longitude":"-85.557889","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.213811","trainerlvl":27,"timestamp":1548854954.9028978}            
testGMO = {"protos":[{"GetMapObjects":"ChIIgICAgPSz54uIARCmz8HEhy0KEgiAgICA\/LPni4gBEKbPwcSHLQpKCICAgIDss+eLiAEQps\/BxIctWhII3wIZYiC5FFRDhwsyBBACIB1aEAjNAhmOzj5Bu6RW7jICEAJaEAiwAhlNmxd1MYZjwTICEAEKEgiAgICA5LPni4gBEKbPwcSHLQoSCICAgIDcs+eLiAEQps\/BxIctChIIgICAgNSz54uIARCmz8HEhy0KvgEIgICAgMSz54uIARCmz8HEhy0qRgkfURjfZfQH4BCmz8HEhy0ZFHkmMxEiRUAhTngiUpJlVcAqCzg4MTc5ZDljMjAzOgoQ3wKiAgQQASAdWNmwvrv4\/\/\/\/\/wFSPAoLODgxNzlkOWMyMDMRH1EY32X0B+AY3wIg\/\/\/\/\/\/\/\/\/\/\/\/ASkUeSYzESJFQDFOeCJSkmVVwDoEEAEgHVoSCN8CGR9RGN9l9AfgMgQQASAdWhAIvgIZXAueZspFghUyAhACChIIgICAgMyz54uIARCmz8HEhy0KEgiAgICAtLPni4gBEKbPwcSHLQo2CICAgIC8s+eLiAEQps\/BxIctWhAIiQIZFSZxPihAIf0yAhABWhAI4QIZVbozeHzWJRMyAhABChIIgICAgKSz54uIARCmz8HEhy0KEgiAgICArLPni4gBEKbPwcSHLQoSCICAgICUs+eLiAEQps\/BxIctChIIgICAgJyz54uIARCmz8HEhy0KEgiAgICAhLPni4gBEKbPwcSHLQoSCICAgICMs+eLiAEQps\/BxIctChIIgICAgNSw54uIARCmz8HEhy0KEgiAgICAzLDni4gBEKbPwcSHLQoSCICAgIDEsOeLiAEQps\/BxIctChIIgICAgLSw54uIARCmz8HEhy0KEgiAgICAvLDni4gBEKbPwcSHLQpZCICAgICksOeLiAEQps\/BxIctGkUKI2I1ZDY2N2IwMGI4NDQ1YzU5Yjg2ZGQzYTE4ODQ4OTRiLjEyEMS+mKf6LBld\/G1PkCJFQCFIpdjROGZVwEABSAGwAQEKEgiAgICArLDni4gBEKbPwcSHLQoSCICAgICsoeeLiAEQps\/BxIctChIIgICAgPyu54uIARCmz8HEhy0K1gMIgICAgOSu54uIARCmz8HEhy0aYwojMTAxMTM1MGFhZmJlNDY1NGExYzgwZTViYTk1ODFkODkuMTYQ0s7Ms4ctGei+nNmuIkVAIZ30vvG1ZVXAKAMw0wJAAZIBAhABmAEBqgEIELIXKJmAwzW4AbibnI+HLfgBARpFCiM2NWYxMjk1MTQ1MTQ0OTllOWMxMzI3ZWVlYzIyYjk3ZC4xNhDtnfijhC0ZSl0yjpEiRUAhPbX66qplVcBAAUgBsAEBIhIRtA+j1JgiRUAZE6cx+a1lVcAiEhHHPsxPliJFQBkTpzH5rWVVwCISEdYsErGTIkVAGVzYGaisZVXAIhIRzVtGwY4iRUAZE6cx+a1lVcAiEhGs\/Av1jiJFQBnv4GCbsGVVwCISERSWbCWoIkVAGe\/gYJuwZVXAIhIRhjhPP6giRUAZFEx47LFlVcAiEhHqDgMipiJFQBm\/rNQwt2VVwCISESjzIAimIkVAGV7Gvd+1ZVXAIhIREJmtK6siRUAZv6zUMLdlVcAiEhGPcLDnryJFQBkIlo89s2VVwCISES7RkgGwIkVAGcu+po60ZVXAIhIRJKEWL60iRUAZ7+Bgm7BlVcAiEhGfSuuzryJFQBnv4GCbsGVVwAoSCICAgIDUrueLiAEQps\/BxIctChIIgICAgNyu54uIARCmz8HEhy0KfQiAgICAhK\/ni4gBEKbPwcSHLRppCiNiY2VkMmQ4YmQyODI0NzM2OTU0N2JlZDBlNjI1YjJhYy4xNhCV1LfChy0Z84++SdMiRUAhTPvm\/uplVcAoAjD4AUABkgECEAGYAQGqAREQg18ZAAAA4Osn2z8og4rJFbgBlJ6Ur4ctChIIgICAgKS054uIARCmz8HEhy0KJgiAgICAnLTni4gBEKbPwcSHLSISEbtr7QIZIkVAGU+FuZQSZVXAChIIgICAgIS054uIARCmz8HEhy0QARgCIhgIgICAgICg54uIARIFCAMwqQEaAggEIgA="}],"submit_version":3,"longitude":"-85.587710","uuid":"39E1811B-CA17-4D63-8988-6969F4k3DEETS","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.266056","trainerlvl":30,"timestamp":1548210956.3161368}
testEncounterResponse = {"protos":[{"EncounterResponse":"Cl8JeVPLVxlbO3sQ76fP54ktGRCHoQ98IUVAIQWGnLyLZVXAKgs4ODE3OWQ5OTg5MzouELwCGIQDIGUoZTDeATgSfTj14T6FAQqMQEGIAQSQAQiYAQKlATsQFT+iAgIQARgBIhMKAwECAxIMcNPbPsOkET+Uoiw\/MAU="}],"submit_version":3,"longitude":"-85.586878","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.261910","trainerlvl":27,"timestamp":1548821452.035928}
testFortDetailsResponse = {"protos":[{"FortDetailsResponse":"CiM0M2QzOGMzYjg3YTM0ZTliYTkwM2IwZjU4ZmJkMWY2ZS4xNiIXVHJpbml0eSBSZWZvcm1lZCBDaHVyY2gqaGh0dHA6Ly9saDUuZ2dwaHQuY29tL1dXQXFDV185Q3dVanFFeUhQaFVLd3p5S3o5OHFCZ05GSUZfclhNVnR2TE9TY1hhdXJoVXpfeGRGcTZfMFRDSU5oMDBDc1d0dTBhaDhIdk5rOFJzSAFR9x3DYz8hRUBZDaZh+IhlVcBiP1RyaW5pdHkgcmVmb3JtZWQgY2h1cmNoLiBPcmdhbml6ZWQgaW4gMTkyOSBhbmQgZXJlY3RlZCBpbiAxOTU1LoIBAA=="}],"submit_version":3,"longitude":"-85.586450","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.259965","trainerlvl":27,"timestamp":1548821618.3672929}
testFortSearchResponse = {"protos":[{"FortSearchResponse":"CAESBAgBEAESBAgBEAESBAgBEAESBAgBEAEoMjCg2e\/niS04AUoGCgQIASgEaiM0M2QzOGMzYjg3YTM0ZTliYTkwM2IwZjU4ZmJkMWY2ZS4xNnL\/AQq0AQgEIgCiBi5DSEFMTEVOR0VfQ0FUQ0hfRUFTWV9QS01OOi03MjAwNjk3MDU3NzY0NDM0NTk5qAbZuoDG1IX\/iJwBsAYCugYZQ0hBTExFTkdFX0NBVENIX0VBU1lfUEtNTsoGAhAK0AYB2gYHCAdCAwiBAeAGxLHd54kt6AbEsd3niS36BiM0M2QzOGMzYjg3YTM0ZTliYTkwM2IwZjU4ZmJkMWY2ZS4xNpgHgICAgICg54uIARJGEgoKAS4QARoBLiABGhpxdWVzdF9jYXRjaF9wb2tlbW9uX3BsdXJhbCIacXVlc3RfY2F0Y2hfcG9rZW1vbl9wbHVyYWwoAQ=="}],"submit_version":3,"longitude":"-85.586430","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.260006","trainerlvl":27,"timestamp":1548821682.6647511}
testGymGetInfoResponse = {"protos":[{"GymGetInfoResponse":"CrkMCm4KIzEwMTEzNTBhYWZiZTQ2NTRhMWM4MGU1YmE5NTgxZDg5LjE2EL2+oOaJLRnovpzZriJFQCGd9L7xtWVVwCgBMMwDQAGSAQIQApgBAaoBExCqFRkAAADg047uPyADKOfimwO4AeGq8OSJLfgBARL1AwrFAQpUCXguyI1tSWmLEJQBGK8FIKgBKKgBMMwBOA1KCU1hc3RyaW9sYX3dsVtAhQEmUydBkAEGmAEEpQEBnAc\/qAED0AGx8fPLnCzoAQH4AQGiAgQQARgBELvK0uSJLRi7BSEAAABg\/VTvPyivBTWamRk+QgoNoAKrPBAMGMAFQgoNoAKrPBAMGMIFQgoNoAKrPBAMGL0FQgoNoAKrPBAMGMQFQgoNoAKrPBAMGMEFQgoNoAKrPBAMGL8FQgoNoAKrPBAMGL4FEgcIAyDn4psDGqECCglNYXN0cmlvbGEQKBqEAloXQVZBVEFSX21faGFpcl9kZWZhdWx0XzFiF0FWQVRBUl9tX3NoaXJ0X2dlbmdhcl8wahtBVkFUQVJfbV9wYW50c190ZWFtcm9ja2V0XzByHEFWQVRBUl9tX2hhdF90ZWFtbGVhZGVyY2FwXzJ6GEFWQVRBUl9tX3Nob2VzX2RlZmF1bHRfM4IBD0FWQVRBUl9tX2V5ZXNfNIoBGkFWQVRBUl9tX2JhY2twYWNrX2dlbmdhcl8wkgEYQVZBVEFSX21fZ2xvdmVzX2pvZ2dlcl8wmgEUQVZBVEFSX21fc29ja3NfZW1wdHmqARlBVkFUQVJfbV9nbGFzc2VzX2pvZ2dlcl8wIAEowrUBQARQxtKTKhKXBArFAQpUCV1GMlf+A\/2zEJMBGKwEIJYBKJYBMMwBOA1KCTQyMExhYlJhdH1DogZAhQFWAJNAiAEPkAEKmAEEpQEekRs\/qAED0AHsuaTOnCzoAQGiAgQQARgBEK\/L0+SJLRi0BCEAAAAgYWrvPyisBDWamRk+QgoN4J6VPBAIGMAFQgoN4J6VPBAIGMIFQgoN4J6VPBAIGL0FQgoN4J6VPBAIGMQFQgoN4J6VPBAIGMEFQgoN4J6VPBAIGL8FQgoN4J6VPBAIGL4FEgcIAiDz4ZoDGsMCCgk0MjBMYWJSYXQQKBqmAkABWhdBVkFUQVJfZl9oYWlyX2RlZmF1bHRfMGIXQVZBVEFSX2Zfc2hpcnRfZ2VuZ2FyXzBqG0FWQVRBUl9mX3BhbnRzX3RlYW1yb2NrZXRfMHIVQVZBVEFSX2ZfaGF0X2dlbmdhcl8wehtBVkFUQVJfZl9zaG9lc190ZWFtcm9ja2V0XzCCAQ9BVkFUQVJfZl9leWVzXzCKARpBVkFUQVJfZl9iYWNrcGFja19nZW5nYXJfMJIBHEFWQVRBUl9mX2dsb3Zlc190ZWFtcm9ja2V0XzCaARhBVkFUQVJfZl9zb2Nrc19kZWZhdWx0XzGiARpBVkFUQVJfZl9iZWx0X3RlYW1yb2NrZXRfMLIBGEFWQVRBUl9mX25lY2tsYWNlX3N0YXJfMCABKMGDAUAEUJCSiSEStAMKwgEKUQkDNEquP8S5yRDMAxjPCyCgAiigAjDXATgoSgt4WHhVck0wTXhYeH0bbgtAhQHv2O5CiAEGkAECmAEOpQFh0yc\/qAEC0AGnoNPiiS2iAgIQAhD2haDmiS0YhwwhAAAA4NOO7j8ozws1mpkZPkIKDRCWOD0QOBjABUIKDRCWOD0QOBjCBUIKDRCWOD0QOBi9BUIKDRCWOD0QOBjEBUIKDRCWOD0QOBjBBUIKDRCWOD0QOBi\/BUIKDRCWOD0QOBi+BRIHCAIgrKfOARrjAQoLeFh4VXJNME14WHgQGRrGASADMAQ4A0gCUANiGEFWQVRBUl9tX3NoaXJ0X2RlZmF1bHRfM2oYQVZBVEFSX21fcGFudHNfZGVmYXVsdF8wchZBVkFUQVJfbV9oYXRfbWltaWt5dV8wigEbQVZBVEFSX21fYmFja3BhY2tfZGVmYXVsdF8zkgEZQVZBVEFSX21fZ2xvdmVzX2RlZmF1bHRfM5oBGEFWQVRBUl9tX3NvY2tzX2RlZmF1bHRfM6oBGEFWQVRBUl9tX2dsYXNzZXNfdGhpY2tfMyABKLMBQAFQ0PM2EgpDcmFuZSBQYXJrGmtodHRwOi8vbGg2LmdncGh0LmNvbS9NTU94WHVCVkZlZHlUb3VYaFAwbTRnX2R0Qi1WRTYtcjlFWXpIc29hV3gtOUpucElNOHVQSlVYcVpGMVNDWVJVaVc3U1RkZm9SdmhyNTE2Uk1DMkRzdyABSgBSCQgDGAEgAzCGAg=="}],"submit_version":3,"longitude":"-85.587938","uuid":"244EC1CA-C317-4292-BC1E-9BC8A5B0B981","validation1":"Ú9£î^kK\r2U¿ï`\u0018¯Ø\u0007\t","latitude":"42.266441","trainerlvl":27,"timestamp":1548821961.6068799}
