from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
import os

webpage = Blueprint('webpage', __name__)

@webpage.route('/', methods=['GET'])
def home():
    return render_template('home.html', message='testo1234')