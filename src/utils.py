from datetime import date, timedelta  # for date manipulation

def generate_menu_msg(menus: dict) -> str:
    """
    Generate a formatted message for the menus.

    Parameters:
    - menus (dict): A dictionary containing menu names as keys and their descriptions as values.

    Returns:
    - str: The formatted message containing all menus.
    """
    msg = ''
    for menu in menus:
        msg += menu + ":\n"
        msg += menus[menu] + "\n"
    return msg

def is_float(string: str) -> bool:
    """
    Check if a string can be converted to a float.

    Parameters:
    - string (str): The string to check.

    Returns:
    - bool: True if the string can be converted to a float, False otherwise.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def time_range() -> tuple:
    """
    Calculate the time range for the current week (Monday to Sunday).

    Returns:
    - tuple: A tuple containing the start and end dates of the current week in the format (start_date, end_date).
    """
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    next_sunday = (last_monday + timedelta(days=6)).strftime("%Y-%m-%d")
    last_monday = last_monday.strftime("%Y-%m-%d")
    return last_monday, next_sunday