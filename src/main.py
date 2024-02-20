#!/usr/bin/python3
from utils import send_msg
from data import get_template_messages, empty_message
import time

if __name__ == "__main__":

    template_messages = get_template_messages()

    response1 = send_msg(template_messages['welcome'])
    time.sleep(3)
    response2 = None
    response3 = None
    response4 = None

    empty_message = empty_message()

    if (not empty_message['polymensa']):
        response2 = send_msg(template_messages['polymensa'])
    time.sleep(3)
    if (not empty_message['upperunimensa']):
        response3 = send_msg(template_messages['upperunimensa'])
    time.sleep(3)
    if (not empty_message['lowerunimensa']):
        response4 = send_msg(template_messages['lowerunimensa'])

    print(f"Whatsapp API status: {response1.status_code}" + ("" if response1.status_code == 200 else f" - {response1.content}"))
    print(f"Whatsapp API status: {response2.status_code}" + ("" if response2.status_code == 200 else f" - {response2.content}"))
    print(f"Whatsapp API status: {response3.status_code}" + ("" if response3.status_code == 200 else f" - {response3.content}"))
    print(f"Whatsapp API status: {response4.status_code}" + ("" if response4.status_code == 200 else f" - {response4.content}"))
