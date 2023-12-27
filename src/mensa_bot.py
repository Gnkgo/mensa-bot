#!/usr/bin/python3
import requests
import json
import configparser
from datetime import datetime, date
import locale
from poly import fetch_mensa_data, parse_mensa_data
from uni import get_uni_msg
import os


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

def send_msg():
    return requests.post(url, headers=headers, data=json.dumps(data))


if __name__ == "__main__":
    api_url = "https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas?client-id=ethz-wcms&lang=en&rs-first=0&rs-size=50&valid-after=2023-12-05"
    mensa_data = fetch_mensa_data(api_url)

    # create BODY of MSG
    uni_msg = get_uni_msg()
    uni_msg_lower = "Wiieterii Mensas sind bald verfüegbar."
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

    msg_body_params = [
    {"type": "text", "text": datetime.now().strftime("%#d. %b")},
        {"type": "text", "text": poly_msg.replace("\n", "\\n")},
        {"type": "text", "text": uni_msg.replace("\n", "\\n")},
        {"type": "text", "text": uni_msg_lower.replace("\n", "\\n")}
    ]

    data = {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'mensa_bot',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': msg_body_params}
            ]
        }
    }

    response = send_msg()
    print(f"Whatsapp API status: {response.status_code}" + ("" if response.status_code == 200 else f" - {response.content}"))
