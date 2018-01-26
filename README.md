# GaleraSQL
Run server variable changes simultaneously on all nodes in cluster.

## Requirements ##
* python 2.7+
* python-pip
* argparse (install with pip)
* tabulate (install with pip)
* mysql-connector=2.1.6 (install with pip)

__Usage:__ GaleraSQL Example

	python gsql.py -H 10.1.30.54 -P 3306 -u root -p password -q "show galera status"
   ![Alt text](/images/status_out.PNG?raw=true "Show status output.")
