#!/usr/bin/python
import subprocess
import sys
import argparse
import logging
import base64
import paramiko
from threading import Thread
from tabulate import tabulate
from galeranode import GaleraNode

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',)
logger = logging.getLogger(__name__)

def run():

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", dest='hname', help="The hostname of DB server.")
    parser.add_argument("-P", dest='port', help="The port of DB server.")
    parser.add_argument("-u", dest='user', help="DB username.")
    parser.add_argument("-p", dest='passwd', help="DB password.")
    parser.add_argument("-ussh", dest='sshu', help="User to connect to node via ssh.")
    parser.add_argument("-pssh", dest='sshp', help="User to connect to node via ssh.")
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

    commands = args.query.split(" ")

    if args.query.lower() == "false":
        print("No query was entered.")
    else:
        if commands[0].lower() == "set":
            logger.info('Checking if query is compatible.')
            for node in gnodes:
                logger.info('Running query on node %s', node.host)
                node.query_node(args.query)            
        elif commands[0].lower() == "show" and commands[1].lower() == "galera" and commands[2].lower() == "status":
            for i in range(len(gnodes)):
                statuses.append([])
                node_status = gnodes[i].get_status()
                statuses[i].append(gnodes[i].get_hostname())
                for ii in range(len(node_status)):
                    statuses[i].append(node_status[ii])   
            statuses.sort()
            print_out(statuses, ["Host", "Status", "Send Q [Now/Avg]",
                                 "Receive Q [Now/Avg]", "Flow Ctrl Sent", 
                                 "Flow Ctrl Recieved", "Flow Ctrl Paused", "Last Committed"])
        
        elif commands[0].lower() == "show" and commands[1].lower() == "galera" and commands[2].lower() == "version":
            for i in range(len(gnodes)):
                statuses.append([])
                statuses[i].append(gnodes[i].get_hostname())
                statuses[i].append(gnodes[i].get_version())
            statuses.sort()
            print_out(statuses, ["Host", "Galera Version"])
        
        elif commands[0].lower() == "restart" and commands[1].lower() == "galera" and commands[2].lower() == "nodes":
            for i in range(len(gnodes)):
                ssh(gnodes[i].get_hostname(), args.sshu, args.sshp, "service mysql restart")
        
        elif commands[0].lower() == "update" and commands[1].lower() == "galera" and commands[2].lower() == "nodes":
            for i in range(len(gnodes)):
                logger.info("Updating: " + gnodes[i].get_hostname())
                ssh(gnodes[i].get_hostname(), args.sshu, args.sshp, "yum update -y")
        else:
            logger.error(
                'Invalid commmand.')

def print_out(out, headers):
    print(tabulate(out, headers, tablefmt="grid"))

def ssh(node, user, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(node, username=user, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    for line in stdout:
        logger.info(line.strip('\n'))
    client.close()

if __name__ == '__main__':
    run()

