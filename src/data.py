import datetime
from utils import time_range
from poly import fetch_mensa_data, parse_mensa_data
from uni import get_uni_msg
from utils import time_range
from data import get_mensa_url
import os
import configparser
import json

# facility id of the different mensas at ETH
id_index = {
    "polymensa": 9
}

last_monday, next_sunday = time_range()

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, "..", "externalData", "config.ini")
config = configparser.ConfigParser()
config.read(config_file_path)
credentialFilePath = config['Paths']['credentialFilePath']

credential_file = open(credentialFilePath)
credential_data = json.load(credential_file)

phone_number_id = credential_data["phone_number_id"]
access_token = credential_data["access_token"]
recipient_phone_number = credential_data["recipient_phone_number"]

credential_file.close()

mensa_data = fetch_mensa_data(get_mensa_url())

uni_msg = get_uni_msg("obere-mensa", "mittagsverpflegung-farm", "mittagsverpflegung-butcher")
uni_msg_lower = get_uni_msg("untere-mensa", "mittag-garden", "mittag-pure-asia")
poly_msg = parse_mensa_data(mensa_data)

url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"
headers = {
    "Authorization": f"Bearer {access_token}",
    'Content-Type': 'application/json'
}

templates_data = {
    'welcome': {
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
    },
    'polymensa': {
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
    },
    'upperunimensa': {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'upperunimensa',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': [
                    {"type": "text", "text": uni_msg.replace("\n", "\\n")},
                ]}            
            ]
        }
    },
    'lowerunimensa': {
        'messaging_product': 'whatsapp',
        'to': recipient_phone_number,
        'type': 'template',
        'template': {
            'name': 'lowerunimensa',
            'language': {'code': 'de'},
            'components': [
                {'type': 'body', 'parameters': [
                    {"type": "text", "text": uni_msg_lower.replace("\n", "\\n")},
                ]}            
            ]
        }
    }
}

def empty_message():
    return {
        'upperunimensa': True if uni_msg == "" else False,
        'lowerunimensa': True if uni_msg_lower == "" else False,
        'polymensa': True if poly_msg == "" else False
    }

def get_template_messages():
    return templates_data

def get_mensa_url():
    return f"https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas/?client-id=ethz-wcms&lang=de&rs-first=0&rs-size=50&valid-after={last_monday}&valid-before={next_sunday}&facility={id_index['polymensa']}"


