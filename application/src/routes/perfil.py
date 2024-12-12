from flask import Blueprint, render_template, flash, redirect, send_from_directory, url_for, request
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.database.users.configure_users import my_db
from application.src.services.api_service import dataRequests
import os
import requests

from dotenv import load_dotenv

load_dotenv()

profile = Blueprint('perfil', __name__, template_folder='templates')
viws_img = Blueprint('img', __name__, template_folder='templates')

# Função para gerar uma chave de cache específica para cada usuário
def make_cache_key():
    """
    Gera uma chave única de cache para cada usuário logado.
    Combina o ID do usuário e o caminho da requisição.
    """
    return f"{current_user.id}:{request.path}"

@profile.route('/devorbit/perfil/<usuario>/')
@login_required
@cache.cached(timeout=20, key_prefix=make_cache_key)
def profile_page(usuario):
   
    
    result = measure_performance(usuario)
    return result
   

def measure_performance(usuario):
    # Conectar ao banco de dados
    banco, cursor = my_db()
    
    # Buscar o ID e o caminho da foto do usuário
    cursor.execute('SELECT id, photo, bio, github, likedin, site, followers, following, banner FROM usuarios WHERE name = ?', (usuario,))
    user = cursor.fetchone()

    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('home.home_page'))  # Redireciona caso o usuário não seja encontrado

    user_photo = user[1]   
    print(user_photo)
    print(user_photo)
    print(user_photo)

    bio = user[2]
    github = user[3]
    likedin = user[4]
    site = user[5]
    followers = user[6]
    following = user[7]
    banner = user[8]
    print(banner)
    print(banner)
    print(banner)



    if bio is None:
            bio = '''Olá! A comunidade DevOrbit está pronta para te receber.
                Compartilhe seus pensamentos e conecte-se com desenvolvedores apaixonados por inovação.'''

    seguir = None

    if usuario != current_user.username:
        seguir = 'Networking'
    else:
         seguir = None 
    

    data = dataRequests()
    if not isinstance(data, dict):
        return data
    
    
    posts_account_user = [
        post for post in data['todos_os_posts'] if post['nome'] == usuario
    ]
    banco.close()

    # Certifique-se de passar todas as variáveis necessárias para o template (Usuario autenticados)
    if current_user.is_authenticated:
         return render_template('profile.html', usuario=usuario, username=current_user.username, 
                           id=current_user.id, posts=posts_account_user, 
                           user_photo=user_photo, bio=bio, github=github, site=site, likedin=likedin,
                           seguir=seguir, followers=followers, following=following, banner=banner )
    
    # Certifique-se de passar todas as variáveis necessárias para o template (Usuario não autenticados)
    else:
        return render_template('profile.html',   
                           posts=posts_account_user, 
                           user_photo=user_photo, bio=bio, banner=banner)


    
@viws_img.route('/files/<path:filename>')
def serve_files(filename):
    return send_from_directory('application/src/static/fotos', filename)