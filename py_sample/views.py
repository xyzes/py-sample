"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import Markup
from flask import request
from py_sample import app
from py_sample import utils

data = "" # <-- Initialized to an empty string

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    """Renders the home page. Sends user input to the controller."""
    global data
    data = utils.controller(request.args)
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        data=Markup(data) # <-- This function renders the output of the controller to the user.
    )

@app.route('/contact')
def contact():
    """Renders the contact page (Not used)."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page (Not used)."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
