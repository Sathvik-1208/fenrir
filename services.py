import utils as u
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError


def check_login(page: Page, target_url: str) -> bool:
    """Navigates to the Odoo database selector page. If the session is invalid or too old, it detects the login screen
    and lets the person authenticate."""
    try:
        u.log('Navigating to the Odoo database selector to check login validity...')
        page.goto(target_url)

        u.log('Searching page for signs of a valid session...')
        page.wait_for_selector('.oe_database_information', timeout=5000)

        u.log('Session verified successfully! Previous login session is valid!')
        u.keep_calm_no_rush(page)
        return True

    except PlaywrightTimeoutError:
        u.log('Login invalid! Redirecting to login screen.', 'WARNING')
        u.keep_calm_no_rush(page)
        print('='*60 + '\n')
        print('ACTION REQUIRED: Please log in with your credentials manually.')
        print('Once you log in, come back to this terminal and press ENTER.')
        print('='*60 + '\n')

        input('Press [ENTER] after you have logged into Odoo.')
        u.keep_calm_no_rush(page)

        try:
            page.wait_for_selector('.oe_database_information', timeout=5000)
            u.log('Manual login verified. Session saved!')
            return True

        except PlaywrightTimeoutError:
            u.log('Verification failed! Person failed to login.', 'ERROR')
            return False

    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while verifying session: {e}.', 'ERROR')
        return False


def database_selection_and_direction(page) -> bool:
    """Receives the database selection page as input, and directs the browser to the database's sales page."""
    try:
        u.keep_calm_no_rush(page)
        database_name = u.input_block('Please enter the database name: ')
        validated_database_name = u.validate_database_name(database_name)

        if validated_database_name is not None:
            try:
                u.log(f'Waiting for database listings page. Looking for database: {database_name}...')
                page.wait_for_selector('.oe_database_information', timeout=5000)
                target_listing = page.locator('.oe_database_row', has=page.get_by_text(database_name, exact=True))
                target_listing.wait_for(state='attached', timeout=5000)

                u.log(f'Database {database_name} found. Clicking connect for the same.')
                target_listing.locator('.oe_connect').click()
                u.log(f'Successfully connected to database {database_name}')

                u.log(f'Clicking on sales option for database {database_name}...')
                page.locator("a[href='/odoo/sales']").click()
                u.log('Successfully navigated to the database sales page.')
                return True
            except PlaywrightTimeoutError:
                u.log(f'Could not locate database selection panel or database name: {database_name}.', 'ERROR')
                return False
        else:
            return False
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected structural error while connecting to database: {e}.', 'ERROR')
        return False


def create_new_quotation_form(page) -> bool:
    """Receives the database's sales page as input, and opens a new quotation form."""
    try:
        u.log('Waiting for Quotations page to appear...')
        page.get_by_text('Quotations', exact=True).wait_for(timeout=5000)

        u.log('Page active. Creating a new quotation form...')
        page.get_by_role('button', name='New').click()

        u.log(f'Successfully created new blank quotation form.')
        return True

    except PlaywrightTimeoutError:
        u.log(f'Timeout: Failed to navigate to or locate the "Quotations" page or the "New" action button.', 'ERROR')
        return False
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while creating new, blank quotation form: {e}.', 'ERROR')
        return False


def confirm_quotation_and_validate(page) -> bool:
    """Receives the quotation form page as input, confirms it and validates the confirmation."""
    try:
        u.log('Submitting quotation document payload (Clicking "Confirm" button)...')
        page.get_by_role('button', name='Confirm').click()
        u.log('Waiting for confirmation verification indicator ("Create Invoice")...')
        page.get_by_role('button', name='Create Invoice').wait_for(timeout=10000)

        u.log('Successfully created and confirmed the quotation.')
        return True

    except PlaywrightTimeoutError:
        u.log('Timeout/Validation warning: The Quotation could not be confirmed.', 'ERROR')
        return False
    except PlaywrightError as net_err:
        u.log(f'Network drop or connection issue detected: {net_err}.', 'ERROR')
        return False
    except Exception as e:
        u.log(f'Unexpected error while confirming and verifying quotation : {e}.', 'ERROR')
        return False