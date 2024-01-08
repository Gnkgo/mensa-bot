#!/usr/bin/python3
import requests
import json
import configparser
from datetime import datetime, date
import locale
from poly import fetch_mensa_data, parse_mensa_data
from uni import get_uni_msg
import os
import time


# Set the language for later use of the weekday
#locale.setlocale(locale.LC_TIME, 'de_DE')

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the config file
config_file_path = os.path.join(current_directory, "..", "externalData", "config.ini")

# Read the configuration file
config = configparser.ConfigParser()
config.read(config_file_path)

# Access the values
credentialFilePath = config['Paths']['credentialFilePath']

def send_msg_welcome():
    return requests.post(url, headers=headers, data=json.dumps(data_welcome))

def send_msg_polymensa():
    return requests.post(url, headers=headers, data=json.dumps(data_poly))

def send_msg_upperunimensa():
    return requests.post(url, headers=headers, data=json.dumps(data_upper_uni))

def send_msg_lowerunimensa():
    return requests.post(url, headers=headers, data=json.dumps(data_lower_uni))


if __name__ == "__main__":
    api_url = "https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas?client-id=ethz-wcms&lang=en&rs-first=0&rs-size=50&valid-after=2024-01-01"
    mensa_data = fetch_mensa_data(api_url)

    # create BODY of MSG
    uni_msg = get_uni_msg("obere-mensa", "mittagsverpflegung-farm", "mittagsverpflegung-butcher")
    uni_msg_lower = get_uni_msg("untere-mensa", "mittag-garden", "mittag-pure-asia")
    poly_msg = parse_mensa_data(mensa_data)

    # create MSG for Whatsapp API
    credential_file = open(credentialFilePath)
    credential_data = json.load(credential_file)

    phone_number_id = credential_data["phone_number_id"]
    access_token = credential_data["access_token"]
    recipient_phone_number = credential_data["recipient_phone_number"]

    credential_file.close()

    url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }


    data_welcome = {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'welcome',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': [
                    {"type": "text", "text": datetime.now().strftime("%#d. %b")},
                ]}
            ]
        }
    }

    data_poly = {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'polymensa',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': [
                    {"type": "text", "text": poly_msg.replace("\n", "\\n")},
                ]}
            ]
        }
    }

    data_upper_uni = {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'upperunimensa',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': [
                    {"type": "text", "text": uni_msg.replace("\n", "\\n")},
                ]}            ]
        }
    }

    data_lower_uni = {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'lowerunimensa',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': [
                    {"type": "text", "text": uni_msg_lower.replace("\n", "\\n")},
                ]}            ]
        }
    }


    response1 = send_msg_welcome()
    time.sleep(3)
    response2 = send_msg_polymensa()
    time.sleep(3)
    response3 = send_msg_upperunimensa()
    time.sleep(3)
    response4 = send_msg_lowerunimensa()

    print(f"Whatsapp API status: {response1.status_code}" + ("" if response1.status_code == 200 else f" - {response1.content}"))
    print(f"Whatsapp API status: {response2.status_code}" + ("" if response2.status_code == 200 else f" - {response2.content}"))
    print(f"Whatsapp API status: {response3.status_code}" + ("" if response3.status_code == 200 else f" - {response3.content}"))
    print(f"Whatsapp API status: {response4.status_code}" + ("" if response4.status_code == 200 else f" - {response4.content}"))
