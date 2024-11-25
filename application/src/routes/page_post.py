import asyncio
from flask import Blueprint, render_template, url_for, request, redirect, flash, jsonify
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename  # Importando secure_filename
from application.src.database.configure_post import create_post
from dotenv import load_dotenv
import requests

load_dotenv()

posts = Blueprint('page_posts', __name__, template_folder='templates')
@posts.route('/devorbit/feed/posts/', methods=['POST', 'GET'])
@login_required
def create_post_route():
    if request.method == 'POST':
        # Coletar dados do formulário
        titulo = request.form.get('titulo')  # name="titulo"
        post_content = request.form.get('post')  # name="post"
        post_image = request.files.get('file')  # name="file"
        username = current_user.username  # Nome do usuário logado

        if not titulo or not post_content:
            flash('Todos os campos são obrigatórios.', 'error')
            return redirect(request.url)

        try:
            # Definir caminho para salvar a imagem
            post_img_path = None
            if post_image:
                upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'application/src/static/uploads')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Garante que o nome do arquivo seja seguro
                img_filename = secure_filename(post_image.filename)
                post_img_path = os.path.join(upload_folder, img_filename)
                
                # Salvar imagem no diretório de uploads
                post_image.save(post_img_path)
                print(f"Imagem salva no diretório: {post_img_path}")

            # Salvar dados diretamente no banco
            create_post(username, post_img_path)

            # Se necessário, também podemos salvar dados em uma API externa aqui
            # Preparar dados para a API externa
            data = {
                'user_id': current_user.id,
                'nome': username,
                'titulo': titulo,
                'post': post_content,
            }

            # Adicionar arquivo, se existir
            files = None
            if post_image:
                files = {
                    'file': (post_image.filename, post_image.read(), post_image.mimetype)
                }

            headers = {'Authorization': f'Bearer {current_user.token}'}

            # Enviar requisição para a API externa
            response = requests.post("http://127.0.0.1:8000/post/", data=data, files=files, headers=headers)

            # Verificar resposta da API
            if response.status_code == 200:
                return redirect('/devorbit/feed/')  # Sucesso
            else:
                error_msg = response.json().get('detail', 'Erro desconhecido')
                flash(f"Erro ao enviar para a API: {error_msg}", 'error')
                return redirect(request.url)

        except Exception as e:
            flash(f"Erro ao criar o post: {str(e)}", 'error')
            return redirect(request.url)

    return render_template('post.html')