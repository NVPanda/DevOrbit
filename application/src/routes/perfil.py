from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.database.users.configure_users import my_db
from urllib.parse import urljoin  # Import para construir URLs completas
import os
import requests
from dotenv import load_dotenv

load_dotenv()

profile = Blueprint('perfil', __name__, template_folder='templates')

@profile.route('/devorbit/perfil/<usuario>/')
@login_required
@cache.cached(timeout=100)
def profile_page(usuario):
    # Função para obter os posts e a foto do usuário
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

    # Faz a requisição para obter os posts da API
    response = requests.get(os.getenv('API_REDE','https://api-devorbirt.onrender.com/posts/'))
    posts_conta_usuario = []

    if response.status_code == 200:
        meus_posts = response.json()

        # Filtra os posts para o usuário atual
        for meu_post in meus_posts:
            if meu_post['nome'] == usuario:
                posts_conta_usuario.append({
                    'id': meu_post['id'],
                    'nome': meu_post['nome'],
                    'data': meu_post['data'][10:16],
                    'posts': meu_post['post'],
                    'likes': meu_post['likes'],
                    'img_url': meu_post['img_url']
                })


        # Verifica a URL da primeira imagem para debug
        
    banco.close()
    # Retorna o template com a foto do usuário e os posts
    return render_template('profile.html', usuario=usuario, username=current_user.username, 
                           id=current_user.id, posts=posts_conta_usuario, 
                           user_photo=user_photo, bio=bio)
