#!/usr/bin/python
import subprocess
import sys
import argparse
from tabulate import tabulate
import logging
from galeranode import GaleraNode
from threading import Thread
import mysql.connector
from mysql.connector import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", dest='hname', help="The hostname of DB server.")
    parser.add_argument("-P", dest='port', help="The port of DB server.")
    parser.add_argument("-u", dest='user', help="DB username.")
    parser.add_argument("-p", dest='passwd', help="DB password.")
    parser.add_argument("-q", dest='query', help="Query to run on all nodes.", default="false")

    args = parser.parse_args()

    logger.info('Getting cluster nodes.')
    init_node = GaleraNode(args.hname, args.port, args.user, args.passwd)
    nodes = init_node.query_node("show status like 'wsrep_incoming_addresses';")
    nodes = nodes[1].split(",")
    nodes = [i.split(':')[0] for i in nodes]
    gnodes = []
    statuses = []

    for i in range(len(nodes)):    
        gnodes.append(GaleraNode(nodes[i], args.port, args.user, args.passwd))

    if args.query.lower() == "false":
        print("No query was entered.")
    else:
        if args.query.lower().startswith('set'):
            logger.info('Checking if query is compatible.')
            for node in gnodes:
                logger.info('Running query on node %s', node.host)
                node.query(args.query)            
        elif args.query.lower() == "show galera status":
            for i in range(len(gnodes)):
                statuses.append([])
                statuses[i].append(gnodes[i].get_hostname())
                statuses[i].append(gnodes[i].get_status())
            statuses.sort()
            print(tabulate(statuses, headers=[
                  "Host", "Status"], tablefmt="grid"))
        else:
            logger.error(
                'This Query should not be ran on all nodes at the same time.')



if __name__ == '__main__':
    run()
