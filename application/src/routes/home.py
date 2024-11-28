from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from application.src.database.users.configure_users import Login, check_user_login, User
from application.src.database.users.configure_users import my_db

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
        response = requests.get('https://api-devorbirt.onrender.com/posts/')
        response.raise_for_status()
        
        

        # Certifique-se de que a resposta é válida e um JSON é retornado
        if response.status_code != 200:
            flash("Erro ao carregar posts. Tente novamente mais tarde.")
            return redirect(url_for('perfil.profile_page'))

        requesting_all_posts = response.json()
        print(requesting_all_posts)

        # Conectar ao banco de dados para buscar fotos de usuários
        conn = sqlite3.connect(os.getenv("BANCO_DB"))
        cursor = conn.cursor()

        cursor.execute("SELECT name, photo FROM usuarios")
        user_photos = cursor.fetchall()
        photo_dict = {user[0]: user[1] for user in user_photos}
        conn.close()


        # # Buscando usurio e foto que foi enviado ao fazer um post
        # banco = sqlite3.connect(os.getenv("BANCO_POST"))
        # cur = banco.cursor()

        # cursor.execute("SELECT nome, img_path FROM post_do_usuario")
        # all_post = cur.fetchall()
        # data_post = {user[0]: user[1] for user in user_photos}
        # banco.close()

        # Ordenar os posts por likes e data
        if requesting_all_posts:
            requesting_all_posts.sort(key=lambda post: (post["likes"], post["data"]), reverse=True)

        # Construir lista de posts com fotos de perfil
        lista_do_melhor_post = []
        for column in requesting_all_posts:
            lista_do_melhor_post.append({
                'id': column['id'],
                'nome': column['nome'],
                'titulo': column['titulo'],
                'data': column['data'][10:16],
                'post': column['post'],
                'likes': column['likes'],
                'img_url': column.get('img_url', None),
                'user_photo': photo_dict.get(column['nome'], '/caminho/para/imagem/padrao.jpg')
            })

        # Filtro de posts populares
        posts_filter = []
        for post_do_momento in lista_do_melhor_post:
            likes = int(post_do_momento['likes'])
            if likes >= 30:
                posts_filter.append({
                    'post_titulo': post_do_momento['titulo'],
                    'post': post_do_momento['post'],
                    'post_nome': post_do_momento['nome'],
                    'likes': post_do_momento['likes'],
                    'data_post': post_do_momento['data'],
                    'img_url': post_do_momento['img_url'],
                    'user_photo': post_do_momento['user_photo']
                })

        # Se nenhum post popular foi encontrado'img_url':
        if not posts_filter:
            posts_filter.append({
                'post_titulo': os.getenv('MENSAGEN'),
                'post': os.getenv('MENSAGEN_POST'),
                'post_nome': os.getenv('CODECHAMBER'),
                'data_post': 'N/A',
                
            })

    except requests.RequestException as e:
       
        return redirect(url_for('errorHttp.page_erro'))

    except sqlite3.Error as e:
       # Envia os erros para um arquilo de logs
        return redirect(url_for('home.home_page'))

    # Retorna a página principal com os posts
    return render_template('home.html', 
                           username=current_user.username, 
                           id=current_user.id, 
                           posts=lista_do_melhor_post, 
                           post_banner=posts_filter, 
                           usuario=usuario)
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

