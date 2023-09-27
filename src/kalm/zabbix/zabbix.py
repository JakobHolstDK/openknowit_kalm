import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import yaml
from ..common import prettyllog
import pprint


ZABBIX_API_URL = os.environ.get('ZABBIX_URL') + "/api_jsonrpc.php"
AUTHTOKEN = os.environ.get('ZABBIX_TOKEN')

#ZABBIX_API_URL = "https://zabbix.openknowit.com/api_jsonrpc.php"
#AUTHTOKEN = "9e39c4605ff25083f230b22ccaf1c18128fb8123a502abddeaad73e0b6cff0b8"
#  --data '{"jsonrpc":"2.0","method":"item.create","params":{"name":"Free disk space on /home/joe/","key_":"vfs.fs.size[/home/joe/,free]","hostid":"10084","type":0,"value_type":3,"interfaceid":"1","delay":30},"id":3}'

def list_host_group():
    HOSTGROUP= os.environ.get('ZABBIX_HOSTGROUP')
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
                "filter": {
                "name": [
                    HOSTGROUP
                        ]         
                }

          },         
        "auth": AUTHTOKEN
    })
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def list_host_groups():
    prettyllog("List host groups","info",   "zabbix", "list_host_groups", "zabbix.py", "kalm")
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
                 "filter": {
                 "name": [
            ] 
            }
        },
        "id": 1,
        "auth": AUTHTOKEN
    })
    pprint.pprint(r.content)
    
    print(json.dumps(r.json(), indent=4, sort_keys=True))


def get_host_group_id(hostgroup):
    r = requests.post(ZABBIX_API_URL,
    json= {

            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [
                        hostgroup
                    ]
                }
            },
            "auth": AUTHTOKEN,
            "id": 1
        })
    return r.json()['result'][0]['groupid']

def create_host_group():
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.create",     
          "params": {         
          "name": "Linux servers"
          },     
        "auth": AUTHTOKEN
    })
    print(json.dumps(r.json(), indent=4, sort_keys=True))
    
def status():
    print("status")
    return 0


def register():
    print("register")
    try:
        hostgroup = os.environ.get('KALM_ZABBIX_HOSTGROUP')
    except:
        print("no hostgroup defined in env KALM_ZABBIX_HOSTGROUP")
        return 1
    print("hostgroup: " + hostgroup)

#    create_host_group()
#    create_host()
#    return 0

def create_host():
  print("\nCreate host")
  hostname = os.environ.get('KALM_ZABBIX_HOSTNAME')
  hostgroup = os.environ.get('KALM_ZABBIX_HOSTGROUP')
  hostip = os.environ.get('KALM_ZABBIX_HOSTIP')   
  grpid = get_host_group_id(hostgroup)
  

  r = requests.post(ZABBIX_API_URL,
                  json={
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "Linux server",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "192.168.3.1",
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": "4"
            }
        ],
        "tags": [
            {
                "tag": "Host name",
                "value": "Linux server"
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
    },
    "id": 2,
    "auth": AUTHTOKEN
  })
  print(json.dumps(r.json(), indent=4, sort_keys=True))
