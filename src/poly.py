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
    if mensa_data is None:
        return "Keine Daten vorhanden."

    result = ""
    current_date_str = str(datetime.now().date())
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d").date()
    current_day_of_week = current_date.weekday() + 1  # Get current day of the week (1 = Monday, 2 = Tuesday, ..., 7 = Sunday)

    weekly_rota_array = mensa_data.get("weekly-rota-array", [])

    for weekly_rota in weekly_rota_array:
        valid_from_str = weekly_rota.get("valid-from")
        valid_to_str = weekly_rota.get("valid-to")

        # Skip entries without valid date range
        if valid_from_str is None or valid_to_str is None:
            continue

        valid_from = datetime.strptime(valid_from_str, "%Y-%m-%d").date()
        valid_to = datetime.strptime(valid_to_str, "%Y-%m-%d").date()

        # Skip entries not within the desired date range
        if current_date < valid_from or current_date > valid_to:
            continue

        day_of_week_array = weekly_rota.get("day-of-week-array", [])

        for day_of_week in day_of_week_array:
            day_of_week_code = day_of_week.get("day-of-week-code")

            # Skip entries for other days
            if day_of_week_code != current_day_of_week:
                continue

            opening_hour_array = day_of_week.get("opening-hour-array", [])

            for opening_hour in opening_hour_array:
                meal_time_array = opening_hour.get("meal-time-array", [])

                for meal_time in meal_time_array:
                    meal_name = meal_time.get("name")

                    if meal_name.lower() == "dinner":
                        continue

                    line_array = meal_time.get("line-array", [])

                    for line in line_array:
                        line_name = line.get("name")

                        if line_name.lower() not in {"home", "garden", "street", "vegan"}:
                            continue

                        line_description = line.get("meal", {}).get("description")
                        price_info = line.get("meal", {}).get("meal-price-array", [])

                        result += (f"*{line_name}*\n")
                        result += (f"{line_description}\n")

                        for price in price_info:
                            customer_group_desc = price.get("customer-group-desc-short")
                            price_value = price.get("price")
                            result += (f"- *Price for {customer_group_desc}: * {price_value}\n")

    return result if result != "" else "Keine Daten vorhanden."
