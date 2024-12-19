from flask import Blueprint, render_template
# from dotenv import load_dotenv

username_unic = Blueprint('username_page',__name__, template_folder='templates')
termosEcondicao = Blueprint('temos', __name__, template_folder='templates')

@username_unic.route('/devorbit/username/')
def register_username():
    return render_template('create_username.html')

@termosEcondicao.route('/devorbit/termos/')
def termos():
    return render_template('termos.html')