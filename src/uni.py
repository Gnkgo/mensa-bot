import requests
from datetime import date
from bs4 import BeautifulSoup

def generate_menu_msg(menu_type, menu_data):
    msg = f"*{menu_type.upper()}*\n"
    msg += f"{menu_data.get('menu', '')}\nF: {get_nutrition(menu_data.get('weight', ''), menu_data.get('fat', ''), True)}, K: {get_nutrition(menu_data.get('weight', ''), menu_data.get('carbohydrates', ''), True)}, P: {get_nutrition(menu_data.get('weight', ''), menu_data.get('protein', ''), True)}\nCalories: {get_nutrition(menu_data.get('weight', ''), menu_data.get('calories', ''), False)}\n"
    msg += f"- Price for Stud: {menu_data.get('price_student', '')}\n"
    msg += f"- Price for Int: {menu_data.get('price_internal', '')}\n"
    msg += f"- Price for Ext: {menu_data.get('price_external', '')}\n"
    msg += "Whueee, no Gluten\n" if (not menu_data.get('contains_gluten', False)) else "Sorry, it has Gluten :( \n"
    return msg

def get_nutrition(weight, nutrition, gram):
    try:
        nutrition_str, weight_str = nutrition.split(" ")[0], weight.split(" ")[0]
        nutrition = float(nutrition_str)
        weight_number = float(weight_str)
        calculated_value = round(nutrition * (weight_number / 100))
        return f"{calculated_value}g" if gram else str(calculated_value)
    except ValueError:
        return "There was an error calculating the nutrition value."

def parse_uni_html(menu_type, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        menu = soup.find('h1', class_='sc-150998b9-4 bUDPpG').text.strip()
        price = [p.text.strip() for p in soup.find_all('p', class_= 'sc-cecedeae-2 jTrBQq')]
        calories = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[1].text.strip()
        fat = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[3].text.strip()
        carbohydrates = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[5].text.strip()
        protein = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[9].text.strip()
        contains_gluten = any("Glutenhaltiges Getreide" in p.text for p in soup.find('div', class_="sc-4879eb88-1 iPrkwi").find_all('p', class_="sc-4879eb88-2 jKiJga"))
        weight = soup.find_all('h3', class_='sc-4cf605e8-1 cDQYwP')[-1].find_next('p', class_='sc-4cf605e8-2 sc-4cf605e8-3 BFqus geMwVZ').text.strip()

        return {
            'menu_type': menu_type,
            'menu': menu,
            'price_student': price[0],
            'price_internal': price[1],
            'price_external': price[2],
            'calories': calories,
            'fat': fat,
            'carbohydrates': carbohydrates,
            'protein': protein,
            'weight': weight,
            'contains_gluten' : contains_gluten
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
            try:
                menu_data = parse_uni_html(url.split('-')[-1], response.text)
                if menu_data:
                    uni_msg += generate_menu_msg(menu_data['menu_type'], menu_data)
            except Exception as e:
                print(f"An error occurred: {e}")
    return uni_msg
