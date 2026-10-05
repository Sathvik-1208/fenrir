# Fenrir
Fenrir is a software that automates a sales quotation workflow in Odoo,
and handles login, database selection, form filling and data validation, 
confirmation and verification, graceful exception handling and logging of the procedure.

## What's Fenrir really made of?
- Python
- Playwright

## Requirements?
- A Python IDE (PyCharm or equivalent)
- Playwright API
- logging, sys, os, datetime and JSON modules in Python
- An Odoo account
- Playwright's own Chromium browser

## Folder structure?
```text
Fenrir\
    actions.py
    automation.log
    main.py
    services.py
    utils.py
    config.json
    Fenrir_README.md
```

## How to run the program?
- Complete the requirements first
- Clone this repository
- Run the main.py Python file
- Log in to Odoo by manual entry of credentials, if prompted
- Follow the terminal prompts

## Features?
- Persistent browser profile
- Configuration of target link through the `config.json` file for the tech-savvy
- Persistent login session handling
- Database selection
- Customer Name selection
- Automatic filling of quotation form fields, product line addition
and population of product line grid
- Interactive input handling and validation of entered data
- Confirmation of quotation and verification of its presence
- Logs of each step in the workflow displayed in the terminal and saved to the 
`automation.log` file for future reference as well as testing and debugging

## Notes
- Nothing must be changed in the browser window while Fenrir works on the quotation,
this includes clicking, scrolling, typing and any actions that could affect the workflow
- As of this version, addition of only a single product line is supported
- Existing Odoo defaults (like Expiry Date for the quotation) are left unchanged
- By default, the product price will considered Tax Exclusive, since Fenrir selects this
mode in Odoo by default

## Demo link
- Video: https://youtu.be/FQK-FNhZ4DQ
