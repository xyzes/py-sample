"""
The py-sample Flask application package.
"""

from flask import Flask
app = Flask(__name__)

import getpass
import py_sample.views
import py_sample.utils

# Create connection Object which will contain SQL Server Connection
print("Please type your username:")
CONN ='DRIVER={SQL Server Native Client 11.0};' + 'SERVER=(localdb)\MSSQLLocalDB;' + 'DATABASE=sampleorganizer;' + 'UID=' + input() + ';' + 'PWD=' + getpass.getpass('Enter your password:\n') + ';'

views.update(utils.controller({}, CONN))
