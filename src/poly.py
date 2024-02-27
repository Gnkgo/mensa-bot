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
    try: 
        today_number = datetime.now().date().weekday() + 1
        result = ""
        
        for weekly_rota in mensa_data.get("weekly-rota-array", []):
            for day in weekly_rota.get("day-of-week-array", []):
                if day.get("day-of-week-code") != today_number:
                    continue
                
                for opening_hour in day.get("opening-hour-array", []):
                    for meal_time in opening_hour.get("meal-time-array", []):
                        last_line = len(meal_time.get("line-array", [])) - 1
                        for idx, line in enumerate(meal_time.get("line-array", [])):
                            line_name = line.get("name", "").lower()
                            if line_name not in ["street", "garden", "home", "vegan"]:
                                continue
                            
                            meal = line.get("meal", {})
                            meal_name = meal.get("name", "")
                            meal_description = meal.get("description", "")
                            result += f"*{line_name.upper()}*:\n{meal_name.capitalize()}:\n{meal_description}\n"
                            
                            for price_info in meal.get("meal-price-array", []):
                                customer_group_desc = price_info.get("customer-group-desc-short", "")
                                price_value = price_info.get("price", "")
                                result += f"- Price for {customer_group_desc}: {price_value}\n"
                            
                            contains_gluten = any(allergy.get("code") == 10 for allergy in meal.get("allergen-array", []))
                            result += "Sorry, it has Gluten :( \n" if contains_gluten else "Whueee, no Gluten\n"
                            
                            # Check if it's the last item
                            if idx == last_line:
                                result = result.rstrip("\n")
        
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

