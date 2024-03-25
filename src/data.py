from datetime import datetime
import requests
import os
import configparser
import json
from poly import fetch_mensa_data, parse_mensa_data
from uni import get_uni_msg
from utils import time_range

last_monday, next_sunday = time_range()

# Define facility ID for polymensa
facility_id_polymensa = 9

# Fetch mensa data
mensa_data = fetch_mensa_data(f"https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas/?client-id=ethz-wcms&lang=de&rs-first=0&rs-size=50&valid-after={last_monday}&valid-before={next_sunday}&facility={facility_id_polymensa}")

# Parse mensa data for polymensa
poly_msg = parse_mensa_data(mensa_data)

# Get messages for university mensas
uni_msg = get_uni_msg("obere-mensa", "mittagsverpflegung-farm", "mittagsverpflegung-butcher")
uni_msg_lower = get_uni_msg("untere-mensa", "mittag-garden", "mittag-pure-asia")


# Read credentials from config file
current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, "..", "externalData", "config.ini")
config = configparser.ConfigParser()
config.read(config_file_path)
credentialFilePath = config['Paths']['credentialFilePath']

with open(credentialFilePath) as credential_file:
    credential_data = json.load(credential_file)

phone_number_id = credential_data["phone_number_id"]
access_token = credential_data["access_token"]
recipient_phone_number = credential_data["recipient_phone_number"]


def send_msg(data: dict) -> requests.Response:
    """
    Send a message using Facebook Graph API.

    Parameters:
    - data (dict): The message data to be sent.

    Returns:
    - requests.Response: The response object.
    """
    url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    return requests.post(url, headers=headers, data=json.dumps(data))

def get_templates_data() -> dict:
    
    """
    Get template data for different messages.

    Returns:
    - dict: A dictionary containing template data for various messages.
    """
    return {
        'welcome': {
            'messaging_product': 'whatsapp',
            'to': recipient_phone_number,
            'type': 'template',
            'template': {
                'name': 'welcome',
                'language': {'code': 'de'},
                'components': [{'type': 'body', 'parameters': [{"type": "text", "text": datetime.now().strftime("%#d. %b")}]}]
            }
        },
        'polymensa': {
            'messaging_product': 'whatsapp',
            'to': recipient_phone_number,
            'type': 'template',
            'template': {
                'name': 'polymensa',
                'language': {'code': 'de'},
                'components': [{'type': 'body', 'parameters': [{"type": "text", "text": poly_msg.replace("\n", "\\n")}]}]
            }
        },
        'upperunimensa': {
            'messaging_product': 'whatsapp',
            'to': recipient_phone_number,
            'type': 'template',
            'template': {
                'name': 'upperunimensa',
                'language': {'code': 'de'},
                'components': [{'type': 'body', 'parameters': [{"type": "text", "text": uni_msg.replace("\n", "\\n")}]}]
            }
        },
        'lowerunimensa': {
            'messaging_product': 'whatsapp',
            'to': recipient_phone_number,
            'type': 'template',
            'template': {
                'name': 'lowerunimensa',
                'language': {'code': 'de'},
                'components': [{'type': 'body', 'parameters': [{"type": "text", "text": uni_msg_lower.replace("\n", "\\n")}]}]
            }
        }
    }

def empty_message() -> dict:
    """
    Check if any of the messages is empty.

    Returns:
    - dict: A dictionary containing flags for empty messages.
    """
    return {
        'upperunimensa': not uni_msg,
        'lowerunimensa': not uni_msg_lower,
        'polymensa': not poly_msg
    }



