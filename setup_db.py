#!/usr/bin/env python3
"""Sync db with latest source."""

import csv, json
from requests import get


apple = "https://raw.githubusercontent.com/clo4/apple_device_identifiers/main/ids.json"
android = "https://storage.googleapis.com/play_public/supported_devices.csv"


def remove_bom(file):
    first_char = file.read(1)
    if first_char != '\ufeff':
        file.seek(0)  # Reset file pointer if BOM is not present
    return file

def sync_apple():
    """Download apple ids json."""
    j = get(url=apple).json()
    # patch iphones to remove uncessary (GSM)
    for x in j:
        if "iPhone" in x:
            j[x][0] = j[x][0].split(" (")[0]
    f = open("pple_ids.json", "w")
    json.dump(j, f, indent=4)
    f.close()


def sync_android():
    """Get android csv from play store database."""
    j = get(url=android)
    if j.status_code != 200:
        print("Network error 404 lol")
        exit(1)
    f = open("andr_ids.csv", "wb")
    f.write(j.content)
    f.close()
    # Convert to json
    json_data = {}
    csvfile = open('andr_ids.csv', 'r', encoding='UTF-16 lE')
    csvfile = remove_bom(csvfile)
    andr = csv.DictReader(csvfile)
    for row in andr:
        # Extract the fields from the current row
        model = row['Model']
        retail_branding = row['Retail Branding']
        device = row['Device']
        marketing_name = row['Marketing Name']
        
        # Create a dictionary for the current model
        json_data[model] = {
            "Retail Branding": retail_branding,
            "Device": device,
            "Marketing Name": marketing_name
        }
    f = open("andr_ids.json", "w")
    json.dump(json_data, f, indent=4)
    f.close()
    



sync_apple()
sync_android()
