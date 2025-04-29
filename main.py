import csv
import os
import time

# my stuff
from core.dns_updater import *

__version__ = 1.0

default_interval = 600
default_ttl = 86400
recordsfile = 'records.csv'

def main():
    my_ip='1234'

    # read env variables
    get_env_vars(default_interval, default_ttl)

    # ----- update loop start

    while(True):
        display_message(["INFO", 12*"-" + " New Cycle " + 12*"-"])

        # track IP
        status_code, obtained_ip = get_public_ip()

        match(status_code):
            case 200:
                display_message(["INFO", "Retrieving Public IP."])

                if obtained_ip == my_ip:
                    display_message(["INFO", "My IP is still fresh."], 200)

                if obtained_ip != my_ip:
                    display_message(["INFO", "New Public IP detected", obtained_ip])
                    my_ip = obtained_ip

                    display_message(["INFO", "Building Record Data."])
                    my_records = build_records(recordsfile, my_ip)

                    update_dns(my_records, my_ip)


            case _:
                display_message(["INFO", "Retrieving Public IP.", False])

        display_message(["INFO", "Cycle complete.", "Waiting for next Cycle."])

        wait_interval()

    # ----- update loop end

main()