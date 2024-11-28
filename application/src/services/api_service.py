from typing import Dict, Any
from flask import redirect, url_for
import sqlite3
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def dataRequests() -> Dict[str, Any]:
    response = requests.get(os.getenv('API'))

    # Redireciona caso a API não esteja disponível
    if response.status_code != 200:
        return redirect(url_for('perfil.profile_page'))
    
    requesting_all_posts = response.json()

    # Ordena os posts por likes e data
    if requesting_all_posts:
        requesting_all_posts.sort(key=lambda post: (post["likes"], post["data"]), reverse=True)

    # Conecta ao banco de dados para buscar fotos de usuários
    conn = sqlite3.connect(os.getenv("BANCO_DB"))
    cursor = conn.cursor()

    cursor.execute("SELECT name, photo FROM usuarios")
    user_photos = cursor.fetchall()

    photo_dict = {user[0]: user[1] for user in user_photos}
    conn.close()

    # Lista de posts formatados
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

    # Filtra os posts com 30 ou mais likes
    posts_em_destaque = [
        post for post in lista_do_melhor_post if int(post['likes']) >= 30
    ]

    # Define o banner padrão (caso não haja destaque)
    banner = {
        'post_titulo': os.getenv('MENSAGEN'),
        'post': os.getenv('MENSAGEN_POST'),
        'post_nome': os.getenv('CODECHAMBER'),
        
    }

    # Troca o banner pelo primeiro post destacado, se houver
    if posts_em_destaque:
        banner = posts_em_destaque[0]

    # Retorna todos os posts e o banner
    return {
        "todos_os_posts": lista_do_melhor_post,
        "post_banner": banner,
    }
