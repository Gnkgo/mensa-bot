#!/usr/bin/python3
from data import get_templates_data, empty_message, send_msg
import time

if __name__ == "__main__":

    template_messages = get_templates_data()

    response1 = send_msg(template_messages['welcome'])
    print(f"Whatsapp API status: {response1.status_code}" + ("" if response1.status_code == 200 else f" - {response1.content}"))

    time.sleep(3)
    response2 = None
    response3 = None
    response4 = None

    empty_message_result = empty_message()

    if (not empty_message_result['polymensa']):
        response2 = send_msg(template_messages['polymensa'])
        print(f"Whatsapp API status: {response2.status_code}" + ("" if response2.status_code == 200 else f" - {response2.content}"))

    time.sleep(3)
    if (not empty_message_result['upperunimensa']):
        response3 = send_msg(template_messages['upperunimensa'])
        print(f"Whatsapp API status: {response3.status_code}" + ("" if response3.status_code == 200 else f" - {response3.content}"))

    time.sleep(3)
    if (not empty_message_result['lowerunimensa']):
        response4 = send_msg(template_messages['lowerunimensa'])
        print(f"Whatsapp API status: {response4.status_code}" + ("" if response4.status_code == 200 else f" - {response4.content}"))
