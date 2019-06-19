"""
The py-sample Flask application package.
"""

from flask import Flask
app = Flask(__name__)

import pypyodbc as pyodbc
import getpass
import py_sample.views
import py_sample.utils

# Create connection Object which will contain SQL Server Connection
print("Please type your username:")
CONNECTION ='DRIVER={SQL Server Native Client 11.0};' + 'SERVER=(localdb)\MSSQLLocalDB;' + 'DATABASE=sampleorganizer;' + 'UID=' + input() + ';' + 'PWD=' + getpass.getpass('Enter your password:\n') + ';'
CONN = (pyodbc.connect(CONNECTION))
print('Connected to database.\n')

views.update(utils.controller({}, CONN))
