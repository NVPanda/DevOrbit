from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from application.src.database.users.configure_users import Login, check_user_login, User
import requests
import time

login_ = Blueprint('login', __name__, template_folder='templates')
logout_ = Blueprint('logout', __name__, template_folder='templates')
home_ = Blueprint('home', __name__, template_folder='templates')


API_REDE = "http://localhost:5000/allpost"

class User(UserMixin):
    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

    # Flask-Login needs this method for the current_user object
    def get_id(self):
        return str(self.id)


@login_.route('/login/', methods=['POST', 'GET'])
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

            next_page = session.get('next', url_for('home.home_page'))
            return redirect(next_page)
        
        else:
            flash('Email ou senha inválidos. Tente novamente.')
            return redirect(url_for('login.login_page'))

    return render_template('login.html')


@home_.route('/Codechamber/feed/')
@login_required
def home_page():

    response = requests.get(API_REDE)
    response.raise_for_status()  # Verifica se houve um erro na requisição

   
   # Mandado os posts da api para o front end
    view_posts = response.json() 
    if view_posts:
        time.sleep(1)
    view_posts.sort(key=lambda x: x["data"], reverse=True)



    # Use current_user.username para exibir o nome do usuário logado
    return render_template('home.html', username=current_user.username, posts=view_posts)


@logout_.route('/logout')
@login_required
def logout():
    logout_user()  # Desloga o usuário
    flash('Você foi desconectado')
    return redirect(url_for('login.login_page'))
