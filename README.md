# GaleraSQL
Run server variable changes simultaneously on all nodes in cluster.

## Requirements ##
* python 2.7+
* python-pip
* argparse (install with pip)
* tabulate (install with pip)
* paramiko (install with pip)
* mysql-connector=2.1.6 (install with pip)

__Commands:__ Avaliable Commands
    show galera (status | version) - Show status of each node in the cluster.
    restart galera nodes - restart mysql process on all nodes in rolling fashion.
    update galera nodes - update database software on all nodes in rolling fashion.

__Usage:__ GaleraSQL Example

	python gsql.py -H 10.1.30.54 -P 3306 -u root -p password -q "show galera status"
   ![Alt text](/images/status_out.PNG?raw=true "Show status output.")
