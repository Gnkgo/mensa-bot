#!/usr/bin/python3

from data import get_templates_data, empty_message, send_msg  # importing necessary functions
import time  # for time-related functions

if __name__ == "__main__":
    
    # Get template messages
    template_messages = get_templates_data()
    
    # Send welcome message
    response1 = send_msg(template_messages['welcome'])
    print(f"Whatsapp API status: {response1.status_code}" + ("" if response1.status_code == 200 else f" - {response1.content}"))

    # Pause for 3 seconds
    time.sleep(5)

    # Initialize response variables
    response2 = None
    response3 = None
    response4 = None

    # Check if any message is available for PolyMensa
    empty_message_result = empty_message()
    if not empty_message_result['polymensa']:
        response2 = send_msg(template_messages['polymensa'])
        print(f"Whatsapp API status: {response2.status_code}" + ("" if response2.status_code == 200 else f" - {response2.content}"))

    # Pause for 3 seconds
    time.sleep(5)

    # Check if any message is available for UpperUniMensa
    if not empty_message_result['upperunimensa']:
        response3 = send_msg(template_messages['upperunimensa'])
        print(f"Whatsapp API status: {response3.status_code}" + ("" if response3.status_code == 200 else f" - {response3.content}"))

    # Pause for 3 seconds
    time.sleep(5)

    # Check if any message is available for LowerUniMensa
    if not empty_message_result['lowerunimensa']:
        response4 = send_msg(template_messages['lowerunimensa'])
        print(f"Whatsapp API status: {response4.status_code}" + ("" if response4.status_code == 200 else f" - {response4.content}"))
