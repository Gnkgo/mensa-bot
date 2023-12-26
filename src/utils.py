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
