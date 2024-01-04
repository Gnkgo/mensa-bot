import requests
from datetime import date
from bs4 import BeautifulSoup
from utils import is_float

def generate_menu_msg(menu_type, menu_data):
    msg = f"*{menu_type}* ({menu_data['preis']}):\n"
    msg += f"{menu_data['menu']}\nF: {mnrtg(menu_data['gesamtgewicht'], menu_data['fat'])}, K: {mnrtg(menu_data['gesamtgewicht'], menu_data['carbohydrates'])}, P: {mnrtg(menu_data['gesamtgewicht'], menu_data['protein'])}\n"
    return msg

def mnrtg(gesamtgewicht, naehrwert):
    naehrwert_number = float(naehrwert.split(" ")[0]) if is_float(naehrwert.split(" ")[0]) else None
    gesamtgewicht_number = float(gesamtgewicht.split(" ")[0]) if is_float(gesamtgewicht.split(" ")[0]) else None

    if naehrwert_number is not None and gesamtgewicht_number is not None:
        return str(round(naehrwert_number * (gesamtgewicht_number / 100))) + " g"
    else:
        return "N/A"

def parse_uni_html(menu_type, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        menu = soup.find('h1', class_='sc-dd6b703-3 jAgsDf').text.strip()
        preis = soup.find('p', class_='sc-f9bc0ed9-2 ktmykt').text.strip()
        fat = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[0].text.strip()
        carbohydrates = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[1].text.strip()
        protein = soup.find_all('p', class_='sc-4cf605e8-2 BFqus')[2].text.strip()
        gesamtgewicht = soup.find('h3', class_='sc-4cf605e8-1 cDQYwP').find_next('p', class_='sc-4cf605e8-2 sc-4cf605e8-3 BFqus geMwVZ').text.strip()

        return {
            'menu_type': menu_type,
            'menu': menu,
            'preis': preis,
            'fat': fat,
            'carbohydrates': carbohydrates,
            'protein': protein,
            'gesamtgewicht': gesamtgewicht
        }

    except Exception as e:
        # Handle the exception as per your requirement
        print(f"An error occurred: {e}")
        return None  # or raise an exception, log, etc.

def get_uni_msg():
    current_date = str(date.today())
    uni_msg = ""

    urls = [
        f"https://app.food2050.ch/uzh-zentrum/obere-mensa/food-profile/{current_date}-mittagsverpflegung-farm",
        f"https://app.food2050.ch/uzh-zentrum/obere-mensa/food-profile/{current_date}-mittagsverpflegung-butcher"
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
        else:
            uni_msg += "Diese Daten sind leider nicht vorhanden.\n"

    return uni_msg
