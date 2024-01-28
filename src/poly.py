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

#print(str(extract_todays_menu(fetch_mensa_data("https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas?client-id=ethz-wcms&lang=en&rs-first=0&rs-size=50&valid-after=2024-01-01"))))
def parse_mensa_data(mensa_data):
    #get the todays date as a number from 1-7 where 1 is monday and 7 is sunday
    today = datetime.now().date()
    #today = datetime.strptime("2024-01-25", "%Y-%m-%d").date()
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
                            #print(line_name.lower())
                            if (line_name.lower() not in ["street", "garden", "home", "vegan"]):
                                continue
                            meal = line["meal"]
                            meal_name = meal["name"]
                            meal_description = meal["description"]
                            result += f"*{line_name}*:\n{meal_name}:\n{meal_description}\n"

                            # Iterate over meal-price-array
                            for price_info in meal["meal-price-array"]:
                                customer_group_desc = price_info["customer-group-desc-short"]
                                price_value = price_info["price"]
                                result += f"- Price for {customer_group_desc}: {price_value}\n"
        
        return result
    except Exception as e:
        print(f"Error parsing Mensa data: {e}")
        return None



    