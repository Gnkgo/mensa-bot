from datetime import date, timedelta

def generate_menu_msg(menus):
    msg = ''
    for menu in menus:
        msg += menu + ":\n"
        msg += menus[menu] + "\n"
    return msg


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def time_range():
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    next_sunday = (last_monday + timedelta(days=6)).strftime("%Y-%m-%d")
    last_monday = last_monday.strftime("%Y-%m-%d")
    return last_monday, next_sunday

