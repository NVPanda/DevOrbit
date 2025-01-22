from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.services.api_service import dataRequests
from application.src.services.user_service import get_user_info, UserData, enrich_posts_with_user_info


import logging
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
        unformacao_usuario = UserData(usuario_id)

        
        
        if not unformacao_usuario:
          return redirect(url_for('home.home_page'))

        #user_metadata = user_metadata[0]
        
 

        # Preenchendo campos opcionais com valores padrão
        biography = user_metadata.get('bio', None)
        banner = user_metadata.get('banner', None)
        photo_user_profile = user_metadata.get('user_photo', None)
        
        

        occupation = unformacao_usuario.get('occupation')
        name = user_metadata.get('username', 'sem info')
        followers = user_metadata.get('followers', 0)
        following = user_metadata.get('following', 0)


        
       
       

        # Verificar se é o perfil do próprio usuário logado
        seguir = 'Networking' if usuario != current_user.username else None

        # Filtrar os posts do usuário
        data = dataRequests()
        if not isinstance(data, dict) or 'todos_os_posts' not in data:
            return redirect(url_for('errorHttp.page_erro'))
        
        
          # Vamos pergar os posts do usuario desta função
        
        

        filtered_user_posts = [post for post in data['todos_os_posts'] if post['user_id'] == current_user.id]
       
        # 1. Chama a função `dataRequests()` para obter os dados da API ou banco de dados,
        # que geralmente retorna um dicionário contendo várias informações, incluindo os posts.
        var = dataRequests()
        # 2. Extrai apenas os posts da resposta retornada, acessando a chave "todos_os_posts".
        # Isso garante que a variável `posts` contenha apenas a lista de posts para ser processada.
        posts = var["todos_os_posts"]  # Extrai apenas os posts
        # 3. Envia a lista de posts para a função `enrich_posts_with_user_info()`,
        # que adiciona informações adicionais aos comentários, como nome e foto do autor.
        # O resultado enriquecido é armazenado em `enriched_posts`.
        enriched_posts = enrich_posts_with_user_info(posts)


        print(user_metadata, '<<< user_metadata')
        print(filtered_user_posts, '<<< filtered_user_posts')

        # Renderizar template
        return render_template(
            'profile.html',
            username=name,
            usuario=current_user.username,
            id=current_user.id,
            posts = filtered_user_posts,
            photo_user_profile =photo_user_profile,
            banner=banner,
            occupation=occupation,
            followers=followers,
            following=following,
            biography=biography,
            foto_commet=enriched_posts
           
           
        )
    except Exception as e:
        logging.critical("Error on profile page", exc_info=True)
        print(e.__class__.__name__)

       

@viws_img.route('/files/<path:filename>')
def serve_files(filename):
    return send_from_directory('application/src/static/fotos', filename)

