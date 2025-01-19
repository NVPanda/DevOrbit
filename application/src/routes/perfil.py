from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.services.api_service import dataRequests
from application.src.services.user_service import get_user_info, UserData

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

profile = Blueprint('perfil', __name__, template_folder='templates')
viws_img = Blueprint('img', __name__, template_folder='templates')

# Função para gerar uma chave de cache específica para cada usuário

@profile.route('/devorbit/perfil/<usuario>/')
@login_required
def profile_page(usuario):
   
    

    try:
        # Obtendo informações do usuário
        usuario_id = int(usuario)
       

        user_metadata = get_user_info(usuario_id)
        if not user_metadata:
            return redirect(url_for('home.home_page'))
        

        user_metadata = user_metadata[0]
 

        # Preenchendo campos opcionais com valores padrão
        bio = user_metadata.get('bio', 'Bem-vindo à DevOrbit! Conecte-se e compartilhe.')
        photo_user_profile = user_metadata.get('user_photo', None)

        # Verificar se é o perfil do próprio usuário logado
        seguir = 'Networking' if usuario != current_user.username else None

        # Filtrar os posts do usuário
        data = dataRequests()
        if not isinstance(data, dict) or 'todos_os_posts' not in data:
            return redirect(url_for('errorHttp.page_erro'))
        filtered_user_posts = [post for post in data['todos_os_posts'] if post['nome'] == usuario]

        # Renderizar template
        return render_template(
            'profile.html',
            username=usuario,
            usuario=current_user.username,
            id=current_user.id,
            posts=filtered_user_posts,
            photo_user_profile=photo_user_profile,
            bio=bio,
            github=user_metadata.get('github', ''),
            site=user_metadata.get('site', ''),
            linkedin=user_metadata.get('linkedin', ''),
            seguir=seguir,
            followers=user_metadata.get('followers', 0),
            following=user_metadata.get('following', 0),
            banner=user_metadata.get('banner', '')
        )
    except Exception as e:
        print('Erro:', e.__class__.__name__)
        return redirect(url_for('errorHttp.page_erro'))

@viws_img.route('/files/<path:filename>')
def serve_files(filename):
    return send_from_directory('application/src/static/fotos', filename)
