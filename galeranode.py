#!/usr/bin/python
import subprocess
import sys
import argparse
from tabulate import tabulate
import logging
from threading import Thread
import mysql.connector
from mysql.connector import Error

class GaleraNode:
    host = "" 
    port = ""
    username = ""
    password = ""
    
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        
    def get_status(self):
        result = self.query_node("SHOW STATUS LIKE 'wsrep_local_state_comment';")
        return result[1]

    def get_hostname(self):
        return self.host
    
    def query_node(self, query):
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.host, port=self.port, user=self.username, password=self.password)
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchone()
            cur.close()
            return result

        except mysql.connector.Error as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

