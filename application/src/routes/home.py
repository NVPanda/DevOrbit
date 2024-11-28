from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from application.src.database.users.configure_users import Login, check_user_login, User
from application.src.database.users.configure_users import my_db
from application.src.services.api_service  import dataRequests

import sqlite3
import requests
from PIL import Image
import urllib.request
from time import sleep
from dotenv import load_dotenv
import os
import time

load_dotenv()


login_ = Blueprint('login', __name__, template_folder='templates')
logout_ = Blueprint('logout', __name__, template_folder='templates')
home_ = Blueprint('home', __name__, template_folder='templates')
erro_http_ = Blueprint('errorHttp', __name__, template_folder='templates')



class User(UserMixin):
    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

   # Função que busca usuario pelo id 
    def get_id(self):
        return str(self.id)


@login_.route('/devorbit/login/', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        

        try_login = Login(email, password)
        is_valid, user_id, username = check_user_login(try_login)
        
        if is_valid:
            # Cria a instância do usuário com o ID e o nome
            user = User(user_id, username)
            # Faz login do usuário usando Flask-Login
            login_user(user)
            flash('Login bem-sucedido!')
            session['user'] = {'name': current_user.username, 'id': current_user.id}
           

            next_page = session.get('next', url_for('home.home_page'))
            return redirect(next_page)
        
        else:
            flash('Email ou senha inválidos. Tente novamente.')
            return redirect(url_for('login.login_page'))
   

    
    return render_template('login.html')

@home_.route('/devorbit/feed/', methods=['POST', 'GET'])
@login_required
def home_page():
    """
    Mostra todos os posts dos usuários, como quem postou, data, quantidade de likes, e a rota principal.
    """

    try:
        
        usuario = current_user.username

        
       
       
       
       
       

    except requests.RequestException as e:
       
        return redirect(url_for('errorHttp.page_erro'))

    except sqlite3.Error as e:
       # Envia os erros para um arquilo de logs
        return redirect(url_for('home.home_page'))

    # Retorna a página principal com os posts
    data = dataRequests()
    data = dataRequests()
    return render_template(
        'home.html',
        username=current_user.username,
        id=current_user.id,
        posts=data['todos_os_posts'], 
        post_banner=data['post_banner'], 
        usuario=usuario
    )
@logout_.route('/devorbit/logout')
@login_required
def logout():

    logout_user()  # Desloga o usuário
    flash('Você foi desconectado')
    return redirect(url_for('login.login_page'))


@erro_http_.route('/devorbit/erro_http/')
@login_required
def page_erro():

    try:
        response = requests.get(os.getenv('API_REDE'), timeout=10)
        if response.status_code == 200:
        
        
            return redirect(url_for('home.home_page'))
        
    
    except requests.exceptions as e:
        print(e)
        print(e)
        print(e)
        print(e)
        print(e)

        return redirect(url_for('errorHttp.page_erro'))



    return 'Erro HTTP ou HTTPS: Você precisa incluir métodos válidos. Você está sendo redirecionado', redirect(url_for('errorHttp.page_erro'))




from flask import send_from_directory
files_ = Blueprint('files', __name__)
@files_.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

