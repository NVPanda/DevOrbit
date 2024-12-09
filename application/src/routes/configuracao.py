import sqlite3
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash
from flask import render_template, Blueprint, redirect, flash, url_for, request, session
import requests
from datetime import datetime
from flask_login import current_user, login_required
from application.src.database.users.configure_users import my_db, Links, linki_of_user

import os
from dotenv import load_dotenv

configuracao_ = Blueprint('config', __name__, template_folder='templates')

load_dotenv()

# Definir a rota e a função associada
@configuracao_.route('/devorbit/configuracao/<usuario>', methods=['POST', 'GET'])
def config_account(usuario):
    if request.method == 'POST':
        github = request.form.get('github')
        likedin = request.form.get('likedin')
        site = request.form.get('site')

        # Obtém o ID do usuário logado a partir da sessão
        user_id = session.get('user', {}).get('id')
        if not user_id:
            return redirect(url_for('login.login_page'))  # Redireciona se não estiver logado
        
        # Cria o objeto Links e salva no banco de dados
        link_data = Links(github=github, likedin=likedin, site=site)
        linki_of_user(link_data, user_id)

        return redirect(url_for('config.config_account', usuario=usuario))
    
    


    try:
        response = requests.get(os.getenv('API'), timeout=10)
        requesting_all_posts = response.json()

        """esse bloco de codigo busca a foto de perfil do usuario"""
        conn = sqlite3.connect(os.getenv("BANCO_DB"))
        cursor = conn.cursor()

        """Pegando os dados nescesarios"""
        cursor.execute("SELECT name, photo FROM usuarios")
        user_photos = cursor.fetchall()

        """Transforme em um dicionário para facilitar o acesso"""
        photo_dict = {user[0]: user[1] for user in user_photos}
        conn.close()

        lista_do_melhor_post = [{
            'id': column['id'],
            'nome': column['nome'],
            'titulo': column['titulo'],
            'data': column['data'][10:16],
            'post': column['post'],
            'likes': column['likes'],
            'img_url': column.get('img_url', None),

            'user_photo': photo_dict.get(column['nome'], 'application/src/static/icon/padrão-do-usuário-64.png')  
        } for column in requesting_all_posts]

        banco, cursor = my_db()

        cursor.execute('SELECT id, photo, email, bio, date_create FROM usuarios WHERE name = ?', (usuario,))
        user = cursor.fetchone()

        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('home.home_page'))  # Redireciona caso o usuário não seja encontrado

        user_photo = user[1]
        email_usuario = user[2]
        bio = user[3]
        date_create = user[4][0:10]

        if bio is None:
            bio = '''Olá! A comunidade DevOrbit está pronta para te receber.
                Compartilhe seus pensamentos e conecte-se com desenvolvedores apaixonados por inovação.'''

        usuario = current_user.username
        id_usuario = current_user.id

        # O status da conta é determinado pelo comportamento do usuário na comunidade. 
        # Seguir as regras e interagir de forma positiva ajuda a manter um bom status.
        status = "Conta Saudável"
        if usuario:
            status = "Conta Saudável"
        else:
            status = "Sua conta está sendo verificada. Por favor, aguarde até que o processo seja concluído."

        # Faz a requisição para obter os posts da API
        response = requests.get(os.getenv('API'), timeout=5)

    except requests.exceptions.RequestException as e:
        log_file = os.getenv('LOGS', 'logs.txt')  # Define um padrão caso a variável de ambiente não esteja configurada
        with open(log_file, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'[{timestamp}] {e.__class__.__name__}: {str(e)}\n')

    return render_template('configuracao.html', posts=lista_do_melhor_post, user_photo=user_photo, usuario=usuario,
                           email_usuario=email_usuario, status=status, id_usuario=id_usuario, bio=bio, date_create=date_create)
