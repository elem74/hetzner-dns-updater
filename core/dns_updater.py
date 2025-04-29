import os
import time
import requests

from datetime import datetime

from rich.table import Table
from rich.console import Console
from rich.text import Text

# my stuff
from core.hetzner_api import *
from core.csvimport import *

log = False
token = 0
interval = 0
ttl = 0
requests_per_second = 3

# rich text console
console = Console()

# ---------------------------------------------------------------------------------------------

class Entry:
    def __init__(self, data, server_zones, my_ip, ttl):
        # csv columns
        # 0 = zone
        # 1 = type
        # 2 = name

        for el in server_zones:
            if el["name"] == data[0]:
                zone_id = el["id"]

        self.record = {
                "value": my_ip,
                "ttl": ttl,
                "type": data[1],
                "name": data[2],
                "zone_id": zone_id,
                "zone_name": data[0]
            }


def delay_after_request():
    time.sleep(1/requests_per_second)

def wait_interval():
    time.sleep(int(interval))


def get_env_vars(default_interval, default_ttl):

    global token
    global interval
    global ttl

    # logging
    # log = os.getenv('log')
    # if token is None:
    #     display_message(['INFO', 'No logging option set, using default.', str(log)])
    # else:
    #     display_message(["INFO", "Logging", str(log)])

    # token

    token = os.getenv('api_token')
    if token is None:
        display_message(['CRITICAL', 'No API Token provided'])
        exit()
    else:
        display_message(["INFO", "API Token", "Received"])

    # update interval
    interval = os.getenv('update_interval')
    if interval is None:
        interval = default_interval
        display_message(["INFO", "No update interval set, using default.", str(interval) + " seconds"])
    else:
        display_message(["INFO", "Update interval =", interval])

    # ttl
    ttl = os.getenv('ttl')
    if ttl is None:
        ttl = default_ttl
        display_message(["INFO", "No TTL set, using default.", str(ttl) + " seconds"])

    else:
        display_message(["INFO", "TTL =", ttl])


def get_public_ip():
    response = requests.get('https://api.ipify.org')

    # text = ip
    return response.status_code, response.text


def build_records(recordsfile, my_ip):
    # api actions
    status_code, server_zones = get_zones(token)

    display_message(["INFO", "Retrieving ZONES IDs"], status_code)
    delay_after_request()

    # reading records.csv
    csv_data = csv_get_records(recordsfile)

    my_records = []

    for linedata in csv_data:
        my_records.append(Entry(linedata, server_zones, my_ip, ttl))

    display_message(["INFO", "Reading File", recordsfile])

    return my_records


def update_dns(my_records, my_ip):
    new_zone = True
    last_zone=''
    current_zone = ''

    for index, entry in enumerate(my_records):

        # set zone vars on first run
        if index == 0:
            current_zone = entry.record["zone_name"]
            last_zone = current_zone

        # determine zone vars on subsequent run
        else:
            if entry.record["zone_name"] != last_zone:
                last_zone = current_zone
                current_zone = entry.record["zone_name"]
                new_zone = True

        full_url = entry.record["name"] + "." + entry.record["zone_name"]

        found_record = False

        if new_zone == True:
            status_code, server_zone_records = get_records(token, entry.record["zone_id"])

            display_message(["INFO", "Retrieving Records for Zone", entry.record["zone_name"]], status_code)
            delay_after_request()
            new_zone = False

            if status_code != 200:
                display_message(["INFO", "No Zone Data", "Skipping Round"])
                break

        # searching for record in server_zone_records
        for server_el in server_zone_records:
            if server_el["name"] == entry.record["name"]:

                # checking if IP is up to date
                if server_el["value"] == my_ip:
                    text_action1 = "Record IP is still fresh."
                    text_action2 = ""
                    status_code = 200
                else:
                    text_action1 = "Updating Record."
                    text_action2 = ''
                    status_code = update_record(token, server_el["id"], entry.record)

                found_record = True
                break

        if found_record == False:
            status_code = create_record(token, entry.record)
            text_action1 = "Creating Record",
            text_action2 = ''

        display_message(["INFO", full_url, text_action1, text_action2], status_code)

    delay_after_request()


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def display_message(texts, status_code = ''):
    output = Text()

    color_critical = "red"
    color_info = "bright_cyan"
    color_text = ["white", "magenta", "yellow", "dark_goldenrod"]

    output.append(f"{get_time()} ", style=f"white")

    for index, item in enumerate(texts):

        if index == 0:
            match(item):
                case 'CRITICAL':
                    current_style = color_critical
                case _:
                    current_style = color_info
        else:
            current_style = color_text[index]

        output.append(f"{item} ", style=f"{current_style}")

    if status_code != '':
        if status_code == 200 or status_code == True:
            output.append("OK", style="green")
        else:
            output.append("FAILED", style="red")

    console.print(output)