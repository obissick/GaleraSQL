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
    state = []
    s_queue = []
    s_queue_avg = []
    r_queue = []
    r_queue_avg = []
    sent = []
    received = []
    paused = []
    committed = []

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def set_state(self):
        self.state = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_state_comment';")

    def set_squeue(self):
        self.s_queue = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_send_queue';")

    def set_squeue_avg(self):
        self.s_queue_avg = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_send_queue_avg';")

    def set_rqueue(self):
        self.r_queue = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_recv_queue';")

    def set_rqueue_avg(self):
        self.r_queue_avg = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_recv_queue_avg';")
    
    def set_fsent(self):
        self.sent = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_flow_control_sent';")

    def set_freceived(self):
        self.received = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_flow_control_recv';")
    
    def set_fpaused(self):
        self.paused = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_flow_control_paused';")

    def set_committed(self):
        self.committed = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_last_committed';")

    def get_status(self): 
        t1 = Thread(target=self.set_state)
        t2 = Thread(target=self.set_squeue)
        t3 = Thread(target=self.set_squeue_avg)
        t4 = Thread(target=self.set_rqueue)
        t5 = Thread(target=self.set_rqueue_avg)
        t6 = Thread(target=self.set_fsent)
        t7 = Thread(target=self.set_freceived)
        t8 = Thread(target=self.set_fpaused)
        t9 = Thread(target=self.set_committed)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        result = [self.state[1], self.s_queue[1] + "/" + self.s_queue_avg[1],
            self.r_queue[1] + "/" + self.r_queue_avg[1], self.sent[1], self.received[1], self.paused[1], self.committed[1]]
        return result
    
    def get_version(self):
        result = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_provider_version';")
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

