from flask import Blueprint, render_template

home_ = Blueprint('home', __name__, template_folder='templates')

@home_.route('/home')
def home_page():


    return render_template('home.html')