from playwright.sync_api import sync_playwright
import os
import sys
import json

import services as s
import utils as u
import actions as a
import time as t


def configuration():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config


def fenrir():
    print()
    with sync_playwright() as p:
        user_data_dir = os.path.abspath('./odoo_user_profile')
        browser_args = ['--start-maximized', '--disable-blink-features=AutomationControlled', '--disable-extensions']
        u.log('Initialising Fenrir...')
        u.log('Launching a stealth browser with persistent context...')

        context = p.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=False, args=browser_args, no_viewport=True)
        page = context.pages[0] if context.pages else context.new_page()

        if not s.check_login(page, configuration()['target_url']):
            u.log('Script Stopped: Login validation failed.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not s.database_selection_and_direction(page):
            u.log('Script Stopped: Database selection and routing failed.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not s.create_new_quotation_form(page):
            u.log('Script Stopped: Quotation form creation failed.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        u.browser_control_notice()

        if not a.enter_customer_name(page):
            u.log('Script Stopped: Customer name entry did not work as planned.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not a.enter_delivery_date_and_time(page):
            u.log('Script Stopped: Delivery date entry did not work as planned.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not a.add_product_line(page):
            u.log('Script Stopped: Product line addition did not work as planned.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not a.populate_description_field(page):
            u.log('Script Stopped: Description entry did not work as planned.', 'ERROR')
            context.close()
            sys.exit(1)

        if not a.populate_quantity(page):
            u.log('Script Stopped: Quantity entry did not work as planned.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not a.populate_price(page):
            u.log('Script Stopped: Price entry did not work as planned.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        if not s.confirm_quotation_and_validate(page):
            u.log('Script Stopped: Quotation confirmation failed.', 'ERROR')
            u.keep_calm_no_rush(page)
            context.close()
            sys.exit(1)

        u.log('Success! Fenrir has created your quotation successfully!')
        t.sleep(5)
        u.keep_calm_no_rush(page)
        context.close()


if __name__ == '__main__':
    try:
        fenrir()
    except KeyboardInterrupt:
        print()
        u.log('Script safely closed by the client. Shutting down Fenrir...', 'WARNING')
        sys.exit(0)
    except Exception as global_err:
        u.log(f'Fatal exception in the main script: {global_err}', 'ERROR')
        sys.exit(1)