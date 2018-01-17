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
        """Set galera state from node."""
        self.state = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_state_comment';")

    def set_squeue(self):
        """Set sent queue from node."""
        self.s_queue = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_send_queue';")

    def set_squeue_avg(self):
        """Set sent queue average from node."""
        self.s_queue_avg = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_send_queue_avg';")

    def set_rqueue(self):
        """Set receive queue from node."""
        self.r_queue = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_recv_queue';")

    def set_rqueue_avg(self):
        """Set receive queue average from node."""
        self.r_queue_avg = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_local_recv_queue_avg';")

    def set_fsent(self):
        """Set flow control sent from node."""
        self.sent = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_flow_control_sent';")

    def set_freceived(self):
        """Set flow control receive from node."""
        self.received = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_flow_control_recv';")

    def set_fpaused(self):
        """Set flow control paused from node."""
        self.paused = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_flow_control_paused';")

    def set_committed(self):
        """Set last commit from node."""
        self.committed = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_last_committed';")

    def get_status(self): 
        """Show the status of the server."""
        threads = [
            Thread(target=self.set_state),
            Thread(target=self.set_squeue), 
            Thread(target=self.set_squeue_avg),
            Thread(target=self.set_rqueue),
            Thread(target=self.set_rqueue_avg),
            Thread(target=self.set_fsent),
            Thread(target=self.set_freceived),
            Thread(target=self.set_fpaused),
            Thread(target=self.set_committed)
        ] 

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        result = [self.state[1], self.s_queue[1] + "/" + self.s_queue_avg[1],
                  self.r_queue[1] + "/" + self.r_queue_avg[1], self.sent[1],
                  self.received[1], self.paused[1], self.committed[1]]
        return result

    def get_version(self):
        """Get the version of galera."""
        result = self.query_node(
            "SHOW GLOBAL STATUS LIKE 'wsrep_provider_version';")
        return result[1]

    def get_hostname(self):
        """Get the hostname or IP if the server."""
        return self.host

    def query_node(self, query):
        """Run a query on the node and return result."""
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
