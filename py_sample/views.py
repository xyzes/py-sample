"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import Markup
from flask import request
from py_sample import app
from py_sample import utils
import pypyodbc as pyodbc

DATA = ""
def update(new):
    DATA = new


@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    utils.controller(request.args)
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        data=Markup(DATA)
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
