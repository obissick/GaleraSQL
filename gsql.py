#!/usr/bin/python
import subprocess
import sys
import argparse
import logging
from threading import Thread
import mysql.connector
from mysql.connector import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect(host, port, username, passwd, query):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host, port=port, user=username, password=passwd)
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


def run():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest='hname', help="The hostname of DB server.")
    parser.add_argument("-P", dest='port', help="The port of DB server.")
    parser.add_argument("-u", dest='user', help="DB username.")
    parser.add_argument("-p", dest='passwd', help="DB password.")
    parser.add_argument("-q", dest='query', help="Query to run on all nodes.")

    args = parser.parse_args()
    logger.info('Checking if query is compatible.')
    if args.query.lower().startswith('set'):
        logger.info('Getting cluster nodes.')
        nodes = connect(args.hname, args.port, args.user, args.passwd,
                        "show status like 'wsrep_incoming_addresses';")
        nodes = nodes[1].split(",")
        nodes = [i.split(':')[0] for i in nodes]
        for node in nodes:
            t = Thread(target=connect, args=(
                node, args.port, args.user, args.passwd, args.query))
            logger.info('Running query on node %s', node)
            t.start()

    else:
        logger.error(
            'This Query should not be ran on all nodes at the same time.')


if __name__ == '__main__':
    run()
