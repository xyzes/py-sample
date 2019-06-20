"""
The py-sample Flask application package.
"""

from flask import Flask
app = Flask(__name__)

import getpass
import py_sample.utils
import urllib

# The __init__ file is the main entry point for the program.
# It prompts the user for their credentials and constructs the connection string to be given to the controller.
DRIVER = "{SQL Server Native Client 11.0};"
SERVER = "(localdb)\MSSQLLocalDB"
DATABASE = "sampleorganizer"
print("Please type your username:")
UID = input() # <-- Prompt user for username in console.
PWD = getpass.getpass() # <-- Prompt user for password in console.
PARAMS ='DRIVER={}SERVER={};DATABASE={};UID={};PWD={};'.format(DRIVER, SERVER, DATABASE, UID, PWD)
CONN = urllib.parse.quote_plus(PARAMS)

# Initialize the controller in its initial state:
utils.controller({}, CONN)

# NOTE: views.py is not required in this file; the controller will initialize the view.