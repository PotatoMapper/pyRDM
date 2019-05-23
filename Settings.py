###############################################
### ProjectTitle: BetaPotatoController      ###
### File: Setting.py                        ###
### Created By: Kyle W. Nicol on 03/21/2019 ###
###############################################

import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    
    load_dotenv()
	
    ######################### Required Environment Variables ###############################
    # DB_HOST: Host IP for database connection
    DB_HOST = os.environ.get('DB_HOST') or '127.0.0.1'
    # DB_PORT: Host Port for database connection
    DB_PORT = os.environ.get('DB_PORT') or 3306
    # DB_NAME: Database name
    DB_NAME = os.environ.get('DB_NAME') or 'rdmdb'
    # DB_USER: Database username
    DB_USER = os.environ.get('DB_USER') or 'rdmuser'
    # DB_PASS: Database user password
    DB_PASS = os.environ.get('DB_PASS') or 'IHeartPotatoes!'
    #DB_CHAR: Default Character set for DB RDM='utf8mb4'
    DB_CHAR = os.environ.get('DB_CHAR') or 'utf8mb4'
    # Max_Log_Files: Max Number of Logs for Rotating File Handler to write to
    MAX_LOG_FILES = os.environ.get('MAX_LOG_FILES') or 4
    # Max_Log_Size: Max Size in Bytes for a single log file
    MAX_LOG_SIZE = os.environ.get('MAX_LOG_SIZE') or 5000000
    # Log_Level: [ERROR/WARNING/INFO/DEBUG]
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'WARNING'
    # RDM_USER = RDM Username with root user group
    RDM_USER = os.environ.get('RDM_USER') or None
    # RDM_PASS = os.environ.get('RDM_PASS') or None
    #########################################################################################