###############################################
### ProjectTitle: BetaPotatoController      ###
### File: DB_Handler.py                     ###
### Created By: Kyle W. Nicol on 03/21/2019 ###
###############################################

import sys, os, json
sys.path.append(os.path.realpath('..'))

import pymysql
from pymysql import ProgrammingError, DataError, OperationalError, IntegrityError, NotSupportedError
from pymysql.cursors import DictCursor

from Misc import get_logger
from Settings import Config

conf = Config()

class DB_Handler(object):

    def __init__(self):
      
        self.db_host = conf.DB_HOST
        self.db_name = conf.DB_NAME
        self.db_port = conf.DB_PORT
        self.db_user = conf.DB_USER
        self.db_pass = conf.DB_PASS
        #self.table_style = config["SqlTableStyle"]

    def Query(self,sql):

        db_conn = pymysql.connect(host = self.db_host, database = self.db_name, port=int(self.db_port), user=self.db_user,cursorclass=DictCursor, passwd=self.db_pass,charset='utf8mb4')
        
        try:    
            db_curs = db_conn.cursor()
            db_curs.execute(sql)
            results = db_curs.fetchall()
        except:
            results = None
            self.log.error('Exception Raised on Query:curs.fetchall().\nQuery Executed: {}'.format(sqlStatement))
            db_conn.rollback()
            db_conn.close()
            raise
        else:
            db_conn.commit()
            db_conn.close()

        return(results)

    def QueryParams(self, sql, params):

        db_conn = pymysql.connect(host = self.db_host, database = self.db_name,port=int(self.db_port), user=self.db_user,passwd=self.db_pass,cursorclass=DictCursor, charset='utf8mb4')
        
        try:
            db_curs = db_conn.cursor()
            db_curs.execute(sql, params)
            results = db_curs.fetchall()
        except:
            results = None
            self.log.error('Exception Raised on QuertyWithParams:curs.fetchall().\nQuery Executed: {}'.format(sql))
            db_conn.rollback()
            db_conn.close()
            raise
        else:
            db_conn.commit()
            db_conn.close()

        return(results)

    def Update(self,sql,params):

        db_conn = pymysql.connect(host = self.db_host, database = self.db_name,port=int(self.db_port), user=self.db_user,passwd=self.db_pass,cursorclass=DictCursor, charset='utf8mb4')

        db_curs = db_conn.cursor()
            
        try:
            db_curs.execute(sql,params)
        except:
            self.log.error("You have fucked up now,Nothing was inserted")
            db_conn.rollback()
            db_conn.close()
            raise
        else:
            self.log.info("WORKED YOU BEAUTIFUL BASTARD")
            db_conn.commit()
            db_conn.close()
