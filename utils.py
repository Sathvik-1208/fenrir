from datetime import datetime
import logging
import sys


def get_valid_datetime(value):
    """ Takes the value of delivery date and time as input and if the format is correct, and the date and time are not from the past,
    returns the value, else returns None.
    """
    try:
        if (not value) or (value.isspace()):
            log('Please use format: DD/MM/YYYY<ONE SPACE>HH:MM<ONE SPACE>AM/PM and do not leave the field blank.',
                'WARNING')
            return None
        parsed = datetime.strptime(value, '%d/%m/%Y %I:%M %p')
        if parsed < datetime.now():
            log('Please do not enter a past time and/or time.', 'WARNING')
            return None
        return parsed.strftime('%d/%m/%Y %I:%M %p')
    except ValueError:
        log('Please use format: DD/MM/YYYY<ONE SPACE>HH:MM<ONE SPACE>AM/PM', 'ERROR')
        return None


def validate_database_name(database_name):
    """Takes the database name as input and validates it, ensuring that blank inputs are not accepted."""
    if (not database_name) or (database_name.isspace()):
        log('Database name cannot be blank or just a space.', 'WARNING')
        return None
    else:
        return database_name


def validate_customer_name(customer_name):
    """Takes the customer name as input and validates it, ensuring that blank inputs are not accepted."""
    if (not customer_name) or (customer_name.isspace()):
        log('Customer name cannot be blank or just a space.', 'WARNING')
        return None
    else:
        return customer_name


def validate_description(description):
    """Takes the product description as input and validates it, ensuring that blank inputs are not accepted."""
    if (not description) or (description.isspace()):
        log('Description cannot be blank or just spaces. No worries, try another time.', 'WARNING')
        return None
    else:
        return description


def validate_quantity(quantity):
    """Takes the product quantity as input and validates the same, ensuring that blank and invalid  inputs, such as: numbers less than zero,
    letters, and special symbols, etc. are not accepted."""
    if (not quantity) or (quantity.isspace()):
        log('Quantity cannot be blank or just spaces. No worries, try another time.', 'WARNING')
        return None
    try:
        quantity = float(quantity)
        if quantity <= 0:
            log('Quantity must be greater than zero. No worries, try another time.', 'WARNING')
            return None
        else:
            return quantity
    except (ValueError, TypeError):
        log('Quantity must be a number. No worries, try another time.', 'WARNING')
        return None


def validate_price(price):
    """Takes the product price as input and validates the same, ensuring that blank and invalid  inputs, such as: numbers less than zero,
    letters, and special symbols, etc. are not accepted."""
    if (not price) or (price.isspace()):
        log('Price cannot be blank or just a space. No worries, try another time.', 'WARNING')
        return None
    try:
        price = float(price)
        if price <= 0:
            log('Price must be greater than zero. No worries, try another time.', 'WARNING')
            return None
        else:
            return price
    except (ValueError, TypeError):
        log('Price must be a number. No worries, try another time.', 'WARNING')
        return None


def divider(length=60):
    """Prints a clean divider line in the terminal."""
    print('-' * length)


def input_block(prompt):
    """Displays one clean input block and returns stripped user input."""
    print()
    divider()
    value = input(prompt).strip()
    divider()
    print()
    return value


def browser_control_notice():
    """Tells the user not to touch the browser while Fenrir is filling the quotation."""
    print()
    divider()
    print('Fenrir is now working on the quotation.')
    print('Please do not click, type, scroll, or change anything in the browser window until Fenrir finishes.')
    divider()
    print()


def keep_calm_no_rush(page):
    """Makes the page wait for 0.5s and flushes the contents in the output buffer and directs it to the terminal."""
    page.wait_for_timeout(500)
    sys.stdout.flush()


def is_browser_closed(page):
    """Checks if the page is closed or not and returns True or False."""
    return page.is_closed()


def log(message, level='INFO'):
    """The logging function for Fenrir, creates the log object and writes the logs to the terminal
     and the 'automation.log' file in the Fenrir folder."""
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
            logging.FileHandler('automation.log'), logging.StreamHandler()])

    if level == 'ERROR':
        logging.error(message)
    elif level == 'WARNING':
        logging.warning(message)
    else:
        logging.info(message)