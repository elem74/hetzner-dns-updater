import requests
import json

def get_zones(token):
    # Getting Zones
    # GET https://dns.hetzner.com/api/v1/zones

    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/zones",
            headers={
                "Auth-API-Token": token,
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))

        temp = json.loads(response.content)
        return response.status_code, temp["zones"]

    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_records(token, zone_id):
    # Getting Records
    # GET https://dns.hetzner.com/api/v1/records

    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/records",
            params={
                "zone_id": zone_id,
            },
            headers={
                "Auth-API-Token": token,
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))

        temp = json.loads(response.content)
        return response.status_code, temp["records"]

    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_record(token, record_id):
    # Get Record
    # GET https://dns.hetzner.com/api/v1/records/{RecordID}

    try:
        response = requests.get(
            url=f"https://dns.hetzner.com/api/v1/records/{record_id}",
            headers={
                "Auth-API-Token": token,
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))

        temp = json.loads(response.content)
        return response.status_code, temp["record"]

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def create_record(token, record_data):
    # Create Record
    # POST https://dns.hetzner.com/api/v1/records

    try:
        response = requests.post(
            url="https://dns.hetzner.com/api/v1/records",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": token,
            },
            data=json.dumps({
                "value": record_data["value"],
                "ttl": int(record_data["ttl"]),
                "type": record_data["type"],
                "name": record_data["name"],
                "zone_id": record_data["zone_id"]
            })
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))

        return response.status_code
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def update_record(token, record_id, record_data):
    # Update Record
    # PUT https://dns.hetzner.com/api/v1/records/{RecordID}

    try:
        response = requests.put(
            url=f"https://dns.hetzner.com/api/v1/records/{record_id}",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": token,
            },
            data=json.dumps({
                "value": record_data["value"],
                "ttl": int(record_data["ttl"]),
                "type": record_data["type"],
                "name": record_data["name"],
                "zone_id": record_data["zone_id"]
            })
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))

        return response.status_code
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_public_ip():
    return requests.get('https://api.ipify.org')