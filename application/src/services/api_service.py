from typing import Dict
from flask import redirect, url_for
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
from flask_login import current_user

from application.src.services.user_service import UserData
load_dotenv()
def dataRequests() -> Dict:

    
    
    try:
        # Faz a requisição à API
        response = requests.get(os.getenv("API","https://api-devorbirt.onrender.com/posts/"))
        print(f"Resposta da API: {response.status_code} ") # Retira antes de ir a prodrução

        if not response.ok:
            print(f"Erro na API: {response.status_code}")
            return {}

        # Tenta converter a resposta para JSON
        try:
            posts = response.json()
            print(f"Posts retornados: {posts[:5]}")  # Mostra os 5 primeiros posts
        except ValueError:
            print("Erro ao converter a resposta para JSON") # Retira antes de ir a prodrução
            return {}
        

        if not isinstance(posts, list):  # Garante que é uma lista
            print("A resposta da API não é uma lista de posts.")
            return {}

        # Conecta ao banco de dados para buscar dados dos usuários
        conn = sqlite3.connect(os.getenv("BANCO_DB"))
        cursor = conn.cursor()

        # Buscar fotos dos usuários
        cursor.execute("SELECT name, photo FROM usuarios")
        user_photos = dict(cursor.fetchall())

        # Buscar nomes de usuário correspondentes
        cursor.execute("SELECT name, username, occupation FROM user_information")
        user_usernames = {name: {'username': username, 'occupation': occupation} 
        for name, username, occupation in cursor.fetchall()}


# Formata a lista de posts
        best_post_list = []
        for post in posts:
            real_name = post['nome']  # Nome real do autor do post
            user_info = user_usernames.get(real_name, {"username": "Desconhecido", "occupation": "Desconhecido"})  # Obter username e occupation
    
            best_post_list.append({
        'id': post['id'],
        'nome': user_info['username'],  # Nome de usuário correto
        'titulo': post['titulo'],
        'data': post['data'][11:16],  # Formato HH:MM
        'post': post['post'].capitalize(),
        'likes': post['likes'],
        'img_url': post.get('img_url', None),
        'user_photo': user_photos.get(real_name, None),  # Foto baseada no nome real
        'occupation': user_info['occupation'],  # Adiciona a ocupação
        
        })

        # Filtra os posts com 30 ou mais likes
        featured_posts = [
            post for post in best_post_list if int(post['likes']) >= 4
        ]

        # Configura o banner padrão
        banner = {
            'post_titulo': os.getenv('MENSAGEN', "Fala Dev!"),
            'post': os.getenv('MENSAGEN_POST', "Os melhores posts vão aparecer aqui! 🌟 Não deixe de comentar e compartilhar suas ideias. Vamos juntos criar uma comunidade incrível!"),
            'nome': os.getenv('CODECHAMBER', "DEV ORBIT")
        }

        # Substitui o banner pelo primeiro post em destaque, se disponível
        if featured_posts:
            banner = featured_posts[0]

        return {
            "todos_os_posts": best_post_list,
            "post_banner": banner
        }

    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        log_file = os.getenv('LOGS', 'logs.txt')
        with open(log_file, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'[{timestamp}] {e.__class__.__name__}: {str(e)}\n')
        return {}

    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}") # Retira antes de ir a prodrução
        return {}
    
