import requests
import json
import os
from ..common import prettyllog




def getenv():
    env = {}
    env['KALM_DNS_TYPE'] = os.getenv('KALM_DNS_TYPE')
    env['KALM_DNS_URL'] = os.getenv('KALM_DNS_URL')
    env['KALM_DNS_TOKEN'] = os.getenv('KALM_DNS_TOKEN')
    env['KALM_DNS_DOMAIN'] = os.getenv('KALM_DNS_DOMAIN')
    env['KALM_DNS_PROVIDER'] = os.getenv('KALM_DNS_PROVIDER')
    if env['KALM_DNS_TYPE'] != "cloudflare":
        print("DNS type not supported")
        exit(1)
    if env['KALM_DNS_URL'] == None:
        print("DNS URL not set")
        exit(1)
    # if url ends with /, remove it
    if env['KALM_DNS_URL'][-1] == "/":
        env['KALM_DNS_URL'] = env['KALM_DNS_URL'][:-1]

    if env['KALM_DNS_TOKEN'] == None:
        print("DNS TOKEN not set")
        exit(1)
    if env['KALM_DNS_DOMAIN'] == None:
        print("DNS DOMAIN not set")
        exit(1)
    if env['KALM_DNS_PROVIDER'] == None:
        print("DNS PROVIDER not set")
        exit(1)
    return env




def check_access():
    env = getenv()
    url = env["KALM_DNS_URL"] + "/client/v4/user/tokens/verify"
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if response.json()["result"]["status"] == "active":
            print("Access verified")
            return True
    else:
        return False

def list_dns():
    myenv = getenv()
    #  --url https://api.cloudflare.com/client/v4/zones/zone_identifier/dns_records \
    url = os.environ.get("KALM_DNS_URL") + "/client/v4/zones/" + os.environ.get("KALM_DNS_ZONEID") + "/dns_records"
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    records = []
    if response.status_code == 200:
        for record in response.json()["result"]:
            records.append(record)
    else:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit(1)
    return records

def add_record(record):
    myenv = getenv()
    records = list_dns()
    url = os.environ.get("KALM_DNS_URL") + "/client/v4/zones/" + os.environ.get("KALM_DNS_ZONEID") + "/dns_records"
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    data = {
    "content": "198.51.100.4",
    "name": "demo",
    "proxied": False,
    "type": "A",
    "comment": "Domain verification record",
    "ttl": 3600
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Record added")
        return True
    else:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit(1)
        return False









