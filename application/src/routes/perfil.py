from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.database.users.configure_users import my_db
from application.src.services.api_service import dataRequests
import os
import requests

from dotenv import load_dotenv

load_dotenv()

profile = Blueprint('perfil', __name__, template_folder='templates')

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
    cursor.execute('SELECT id, photo, bio FROM usuarios WHERE name = ?', (usuario,))
    user = cursor.fetchone()

    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('home.home_page'))  # Redireciona caso o usuário não seja encontrado

    user_photo = user[1]
   
    bio = user[2]
    

    data = dataRequests()
    if not isinstance(data, dict):
        return data
    
    
    posts_account_user = [
        post for post in data['todos_os_posts'] if post['nome'] == usuario
    ]
    banco.close()

    if current_user.is_authenticated:
         return render_template('profile.html', usuario=usuario, username=current_user.username, 
                           id=current_user.id, posts=posts_account_user, 
                           user_photo=user_photo, bio=bio)
    else:
        return render_template('profile.html',   
                           posts=posts_account_user, 
                           user_photo=user_photo, bio=bio)


    
