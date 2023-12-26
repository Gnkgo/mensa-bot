# uni.py
import requests
from datetime import date
from utils import is_float

def generate_menu_msg(menus):
    msg = ''
    for menu in menus:
        msg += menu + ":\n"
        msg += menus[menu] + "\n"
    return msg


def mnrtg(gesamtgewicht, naehrwert):
    naehrwert_number = float(naehrwert.split(" ")[0]) if is_float(naehrwert.split(" ")[0]) else None
    gesamtgewicht_number = float(gesamtgewicht.split(" ")[0]) if is_float(gesamtgewicht.split(" ")[0]) else None

    if naehrwert_number is not None and gesamtgewicht_number is not None:
        return str(round(naehrwert_number * (gesamtgewicht_number/100))) + " g"
    else:
        return "N/A"

def parse_uni_html(menu_type: str, html: str):
    menu = html.split("<h1 class=\"sc-dd6b703-3 jAgsDf\">")[1].split("<!-- --> <!-- --></h1>")[0]
    preis = html.split("<p class=\"sc-f9bc0ed9-2 ktmykt\">")[1].split("</p>")[0]
    fat = html.split("<p class=\"sc-4cf605e8-2 BFqus\">fat</p><p class=\"sc-4cf605e8-2 BFqus\">")[1].split("</p>")[0]
    carbohydrates = html.split("<p class=\"sc-4cf605e8-2 BFqus\">carbohydrates</p><p class=\"sc-4cf605e8-2 BFqus\">")[1].split("</p>")[0]
    protein = html.split("<p class=\"sc-4cf605e8-2 BFqus\">Protein</p><p class=\"sc-4cf605e8-2 BFqus\">")[1].split("</p>")[0]
    gesamtgewicht = html.split("<h3 class=\"sc-4cf605e8-1 cDQYwP\">Gesamtgewicht</h3><p class=\"sc-4cf605e8-2 sc-4cf605e8-3 BFqus geMwVZ\">")[1].split("</p>")[0]

    return {"*" + menu_type + "* (" + preis + ")": menu + "\nF: " + mnrtg(gesamtgewicht, fat) + ", K: " + mnrtg(gesamtgewicht, carbohydrates) + ", P: " + mnrtg(gesamtgewicht, protein)}

def get_uni_msg():
    current_date = str(date.today())
    uni_msg = ""

    response_obere_mensa_farm = requests.get(f"https://app.food2050.ch/uzh-zentrum/obere-mensa/food-profile/{current_date}-mittagsverpflegung-farm")
    
    if response_obere_mensa_farm.status_code == 200:
        menu_farm_obere_mensa = parse_uni_html("Farm", response_obere_mensa_farm.text)
        uni_msg += generate_menu_msg(menu_farm_obere_mensa)
    else:
        uni_msg += "Diese Daten sind leider nicht vorhanden.\n"

    response_obere_mensa_butcher = requests.get(f"https://app.food2050.ch/uzh-zentrum/obere-mensa/food-profile/{current_date}-mittagsverpflegung-butcher")
    
    if response_obere_mensa_butcher.status_code == 200:
        menu_butcher_obere_mensa = parse_uni_html("Butcher", response_obere_mensa_butcher.text)
        uni_msg += generate_menu_msg(menu_butcher_obere_mensa)
    else:
        uni_msg += "Diese Daten sind leider nicht vorhanden."

    return uni_msg
