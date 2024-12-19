from typing import Dict
from flask import redirect, url_for
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def dataRequests() -> Dict:
    try:
        # Faz a requisição à API
        response = requests.get(os.getenv("API"))
        print(response)  # Log para depuração
      

        if not response.ok:
            print(f"Erro na API: {response.status_code}")
            return {}

        # Tenta converter a resposta para JSON
        try:
            posts = response.json()
        except ValueError:
            print("Erro ao converter a resposta para JSON")
            return {}

        if not isinstance(posts, list):  # Garante que é uma lista
            print("A resposta da API não é uma lista de posts.")
            return {}

        # Conecta ao banco de dados para buscar fotos dos usuários
        conn = sqlite3.connect(os.getenv("BANCO_DB"))
        cursor = conn.cursor()
        cursor.execute("SELECT name, photo FROM usuarios")
        user_photos = cursor.fetchall()
        photo_dict = {user[0]: user[1] for user in user_photos}
        conn.close()

        # Formata a lista de posts
        best_post_list = []
        for post in posts:
            best_post_list.append({
                'id': post['id'],
                'nome': post['nome'],
                'titulo': post['titulo'],
                'data': post['data'][11:16],  # Formato HH:MM
                'post': post['post'].capitalize(),
                'likes': post['likes'],
                'img_url': post.get('img_url', None),
                'user_photo': photo_dict.get(post['nome'], None)
            })

        # Filtra os posts com 30 ou mais likes
        featured_posts = [
            post for post in best_post_list if int(post['likes']) >= 4
        ]
        
        


        # Configura o banner padrão
        banner = {
            'post_titulo': os.getenv('MENSAGEN', "Fala Dev!"),
            'post': os.getenv('MENSAGEN_POST', "'Os melhores posts vão aparecer aqui! 🌟 Não deixe de comentar e compartilhar suas ideias. Vamos juntos criar uma comunidade incrível!"),
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
        # Log do erro em um arquivo
        log_file = os.getenv('LOGS', 'logs.txt')
        with open(log_file, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'[{timestamp}] {e.__class__.__name__}: {str(e)}\n')
        return {}

    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return {}
