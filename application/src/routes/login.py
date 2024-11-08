from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from application.src.database.users.configure_users import Login, check_user_login, User
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

login_ = Blueprint('login', __name__, template_folder='templates')
logout_ = Blueprint('logout', __name__, template_folder='templates')
home_ = Blueprint('home', __name__, template_folder='templates')
erro_http_ = Blueprint('errorHttp', __name__, template_folder='templates')



API_REDE = "http://localhost:5000/allpost"




class User(UserMixin):
    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

   # Função que busca usuario pelo id 
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
    
    try:

        response = requests.get(API_REDE, timeout=10)
        status_requests = f'{response.status_code} requisição feita com sucesso: ' if response.ok else f'{response.status_code}  Não foi porsivel completa a requisição :('
        print(status_requests)
        view_posts = response.json() 
        if view_posts:
            view_posts.sort(key=lambda x: x["data"], reverse=True)

        melhor_post = response.json()
        
        lista_do_melhor_post = []
        for postlike in melhor_post:
            lista_do_melhor_post.append({
                        'nome': postlike['nome'],
                        'data': postlike['data'],
                        'post': postlike['post'],
                        'likes': postlike['likes']
                    }
                    )
        for post_do_momento in lista_do_melhor_post:
            if post_do_momento['likes'] > 100 or  post_do_momento['likes'] > 300:
                post_titulo = post_do_momento['post'][0:30]
                post = post_do_momento['post']
                post_nome = post_do_momento['nome']
            
            elif not post_do_momento['likes']:
                post_titulo = post_do_momento['post'] = os.getenv('MENSAGEN')
                post = post_do_momento['post'] = os.getenv('MENSAGEN_POST')
                post_nome = post_do_momento['nome'] = os.getenv('CODECHAMBER')
                

             
           
       
                    
    except requests.exceptions.InvalidSchema as ErrorHttp:

        flash(f"Erro HTTP ou HTTPS: Você precisa incluir métodos válidos. {ErrorHttp.args[0]} Você está sendo redirecionado.")
        return redirect(url_for('errorHttp.page_erro'))  # Redirecionamento após erro

    except requests.exceptions.ReadTimeout as ErroTimeaut:
        flash(f'Erro de Timeout, verifique sua conexão à internet. {ErroTimeaut.args[0]}')
        return redirect(url_for('perfil.profile_page'))  # Redirecionamento para erro de timeout

    except requests.exceptions.JSONDecodeError as ErroJson:
        flash("Erro no servidor, estamos passando por problemas internos. Por favor, tente acessar outras rotas em breve.")
        return redirect(url_for('errorHttp.page_erro'))  # Redirecionamento para erro de JSON

    
    # Use current_user.username para exibir o nome do usuário logado
    return render_template('home.html', username=current_user.username, posts=view_posts, postig=post, post_titulo=post_titulo, post_nome=post_nome)


@logout_.route('/logout')
@login_required
def logout():
    logout_user()  # Desloga o usuário
    flash('Você foi desconectado')
    return redirect(url_for('login.login_page'))


@erro_http_.route('/erro_http')
def page_erro():

    try:
        response = requests.get(API_REDE, timeout=1)
        status = response.status_code
        if status == 200:
            time.sleep(3)
            return redirect(url_for('home.home_page'))
        
    
    except requests.exceptions as e:
        return redirect(url_for('errorHttp.page_erro'))



    return 'Erro HTTP ou HTTPS: Você precisa incluir métodos válidos. Você está sendo redirecionado', redirect(url_for('/Codechamber/feed/'))