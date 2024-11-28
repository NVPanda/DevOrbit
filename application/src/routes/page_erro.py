from flask import Blueprint,  url_for,  redirect, url_for
import requests
from flask_login import login_required
import os
from dotenv import load_dotenv

load_dotenv()
erro_http_ = Blueprint('errorHttp', __name__, template_folder='templates')

@erro_http_.route('/devorbit/erro_http/')
@login_required
def page_erro():

    try:
        response = requests.get(os.getenv('API_REDE'), timeout=10)
        if response.status_code == 200:        
            return redirect(url_for('home.home_page'))
        
    
    except requests.exceptions as e:

        return redirect(url_for('errorHttp.page_erro'))

    return 'Erro HTTP ou HTTPS: Você precisa incluir métodos válidos. Você está sendo redirecionado', redirect(url_for('errorHttp.page_erro'))