import utils as u
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError


def enter_customer_name(page) -> bool:
    """Receives the database's home page as input, and enters the customer name."""
    try:
        u.keep_calm_no_rush(page)
        customer_name = u.input_block('Please enter the customer name: ')
        validated_customer_name = u.validate_customer_name(customer_name)

        if validated_customer_name is not None:
            try:
                u.log(f'Attempting to select customer: {validated_customer_name}...')
                page.locator('input#partner_id_0').click()
                page.get_by_text(customer_name, exact=True).wait_for(timeout=5000)
                page.get_by_text(customer_name, exact=True).click()
                u.log(f'Successfully selected customer: {customer_name}!')
            except PlaywrightTimeoutError:
                u.log(f'Timeout: Could not find customer: {validated_customer_name}! Create and try again!',
                      'ERROR')
                return False
        return True
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while selecting customer name: {e}', 'ERROR')
        return False

def enter_delivery_date_and_time(page) -> bool:
    """Receives the new quotation page as input, validates date and time using utils validation,
    and enters the value in the 'Delivery Date' form field. The function runs until correct format is entered."""
    try:
        while True:
            u.keep_calm_no_rush(page)
            delivery_datetime = u.input_block(
                'Please enter the delivery date and time (DD/MM/YYYY<ONE SPACE>HH:MM<ONE SPACE>AM/PM) in 12 HOUR format: ')
            validated_datetime = u.get_valid_datetime(delivery_datetime)

            if validated_datetime is not None:
                delivery_date_field = 'input#commitment_date_0.o_input.cursor-pointer.user-select-none'
                page.locator(delivery_date_field).fill(validated_datetime)
                u.log(f'Successfully populated delivery date and time!')
                break
            else:
                continue
        return True
    except (KeyboardInterrupt, SystemExit):
        u.log('User cancelled the date input process.', 'ERROR')
        return False
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while populating delivery date and time: {e}', 'ERROR')
        return False


def add_product_line(page) -> bool:
    """Receives the new quotation page as input, and adds a new product line."""
    try:
        page.get_by_role('button', name='Add Line').click()
        page.wait_for_selector('td[name="name"]', timeout=5000)
        return True
    except PlaywrightTimeoutError:
        u.log('Timeout: The product line did not load in time!', 'ERROR')
        return False
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while adding product line: {e}', 'ERROR')
        return False

def populate_description_field(page) -> bool:
    """Receives the new quotation page as input, and enters the product description."""
    try:
        while True:
            u.keep_calm_no_rush(page)
            description = u.input_block('Enter the description of the goods: ')
            validated_description = u.validate_description(description)

            if validated_description is not None:
                description_cell = page.locator('td[name="name"]').first
                description_cell.click()
                description_box = description_cell.locator('textarea.o_input').first
                description_box.wait_for(timeout=5000)
                description_box.fill(str(validated_description))
                page.keyboard.press('Tab')
                u.log('Successfully populated description field!')
                break
            else:
                continue
        return True
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while populating description field: {e}', 'ERROR')
        return False


def populate_quantity(page) -> bool:
    """Receives the new quotation page as input, and enters product quantity."""
    try:
        while True:
            u.keep_calm_no_rush(page)
            quantity = u.input_block('Enter the quantity of the goods: ')
            validated_quantity = u.validate_quantity(quantity)

            if validated_quantity is not None:
                page.locator('td[name="product_uom_qty"]').click()
                page.locator('td[name="product_uom_qty"] input.o_input').fill(str(validated_quantity))
                page.keyboard.press('Tab')
                u.log('Successfully populated quantity field!')
                break
            else:
                continue
        return True
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while populating quantity: {e}', 'ERROR')
        return False


def populate_price(page) -> bool:
    """Receives the new quotation page as input, and enters the product price for one unit."""
    try:
        while True:
            u.keep_calm_no_rush(page)
            price = u.input_block('Enter the price of one unit of the goods: ')
            validated_price = u.validate_price(price)

            if validated_price is not None:
                page.locator('td[name="price_unit"]').click()
                page.locator('td[name="price_unit"] input.o_input').fill(str(validated_price))
                page.keyboard.press('Tab')
                u.log('Successfully populated price field!')
                break
            else:
                continue
        return True
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while populating price: {e}', 'ERROR')
        return False