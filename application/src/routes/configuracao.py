from flask import render_template, Blueprint, redirect, flash,url_for
import requests
import sqlite3
from flask_login import current_user
from flask_login import current_user, login_required
from application.src.database.users.configure_users import my_db

import os
from dotenv import load_dotenv

configuracao_ = Blueprint('config', __name__, template_folder='templates')

load_dotenv()

# Definir a rota e a função associada
@configuracao_.route('/devorbit/configuracao/<usuario>')
@login_required
def config_account(usuario):

    try:
        
        
        response = requests.get(os.getenv('API_REDE'), timeout=10)
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

        cursor.execute('SELECT id, photo, email, bio FROM usuarios WHERE name = ?', (usuario,))
        user = cursor.fetchone()

        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('home.home_page'))  # Redireciona caso o usuário não seja encontrado

   
        user_photo = user[1]
        email_usuario = user[2]
        bio = user[3]
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
        response = requests.get(os.getenv('API_REDE'), timeout=5)

    except requests.exceptions as e:
        print(e)


    return render_template('configuracao.html', posts=lista_do_melhor_post, user_photo=user_photo, usuario=usuario,email_usuario=email_usuario, status=status, id_usuario=id_usuario, bio=bio)
