import requests
from datetime import date
from bs4 import BeautifulSoup
from utils import is_float

def generate_menu_msg(menu_type, menu_data):
    customer_group_desc = ["stud", "int", "ext"]
    msg = f"*{menu_type.upper()}*\n"
    msg += "Whueee, no Gluten" if (not menu_data['contains_gluten']) else "Sorry, it has Gluten :( \n"
    msg +=  ({menu_data['preis']})
    msg += f"{menu_data['menu'].replace(",", " |")}\nF: {get_nutrition(menu_data['weight'], menu_data['fat'])}, K: {get_nutrition(menu_data['weight'], menu_data['carbohydrates'])}, P: {get_nutrition(menu_data['weight'], menu_data['protein'])}, Calories: {get_nutrition(menu_data['weight'], menu_data['calories'])}\n"

    for i, price_value in enumerate(menu_data["price"]):
        msg += f"- Price for {customer_group_desc[i]}: {price_value}\n"

    return msg

def get_nutrition(weight, nutrition, gram):
    def is_convertible_to_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    nutrition_str, weight_str = nutrition.split(" ")[0], weight.split(" ")[0]
    if is_convertible_to_float(nutrition_str) and is_convertible_to_float(weight_str):
        nutrition = float(nutrition_str)
        weight_number = float(weight_str)
        calculated_value = round(nutrition * (weight_number / 100))
        return f"{calculated_value}g" if gram else str(calculated_value)
    else:
        return ""



def parse_uni_html(menu_type, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        menu = soup.find('h1', class_='sc-7777f2ac-4 exYHeE').text.strip()
        price = soup.find_all('p', class_='sc-4af05c12-2 efEXNF').text.strip()
        calories = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[1].text.strip()
        fat = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[3].text.strip()
        carbohydrates = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[5].text.strip()
        protein = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[9].text.strip()

        allergies = soup.find('div', class_="sc-4879eb88-1 iPrkwi")

        contains_gluten = False

        # Iterate through each <p> tag within the div and check for the gluten-containing text
        for p in allergies.find_all('p', class_="sc-4879eb88-2 jKiJga"):
            if "Glutenhaltiges Getreide" in p.text:
                contains_gluten = True
                break
        
        weight = soup.find_all('h3', class_='sc-4cf605e8-1 cDQYwP')[3].find_next('p', class_='sc-4cf605e8-2 sc-4cf605e8-3 BFqus geMwVZ').text.strip()
        
        print (contains_gluten)

        return {
            'menu_type': menu_type,
            'menu': menu,
            'price': price,
            'calories': calories,
            'fat': fat,
            'carbohydrates': carbohydrates,
            'protein': protein,
            'weight': weight,
            'contains_gluten' : contains_gluten
        }
    

    except Exception as e:
        # Handle the exception as per your requirement
        print(f"An error occurred: {e}")
        return None  # or raise an exception, log, etc.

def get_uni_msg(upperLower, menu_vegi, menu_meet):
    current_date = str(date.today())
    uni_msg = ""

    urls = [
        f"https://app.food2050.ch/uzh-zentrum/{upperLower}/food-profile/{current_date}-{menu_vegi}",
        f"https://app.food2050.ch/uzh-zentrum/{upperLower}/food-profile/{current_date}-{menu_meet}"
    ]

    for url in urls:
        response = requests.get(url)


        if response.status_code == 200:
            try :
                menu_data = parse_uni_html(url.split('-')[-1], response.text)
                uni_msg += generate_menu_msg(menu_data['menu_type'], menu_data)

            except Exception as e:
                print(f"An error occurred: {e}")
                uni_msg += "Diese Daten sind leider nicht vorhanden.\n"

    return uni_msg
