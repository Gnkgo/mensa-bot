import requests
from datetime import datetime

def fetch_mensa_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Mensa data: {e}")
     
        return None

def parse_mensa_data(mensa_data):
    today = datetime.now().date()
    today_number = today.weekday() + 1
    try: 
        result = ""
        for weekly_rota in mensa_data["weekly-rota-array"]:
            for day in weekly_rota["day-of-week-array"]:
                if day["day-of-week-code"] != today_number:
                    continue
                for opening_hour in day["opening-hour-array"]:
                    for meal_time in opening_hour["meal-time-array"]:
                        for line in meal_time["line-array"]:
                            line_name = line["name"]
                            if (line_name.lower() not in ["street", "garden", "home", "vegan"]):
                                continue
                            meal = line["meal"]
                            meal_name = meal["name"]
                            meal_description = meal["description"]
                            result += f"*{line_name}*:\n{meal_name}:\n{meal_description}\n"

                            for price_info in meal["meal-price-array"]:
                                customer_group_desc = price_info["customer-group-desc-short"]
                                price_value = price_info["price"]
                                result += f"- Price for {customer_group_desc}: {price_value}\n"

                            contains_gluten = False
                            for allergy in meal["allergy-array"]:
                                if (allergy["code"] == 10):
                                    contains_gluten = True
                                    result += "Sorry, it has Gluten :( \n"
                            if (not contains_gluten):
                                result += "Whueee, no Gluten"

        
        return result
    except Exception as e:
        print(f"Error parsing Mensa data: {e}")
        return None



    