from application.src.__main__ import cache
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from application.src.database.configure_post import criando_post
from dotenv import load_dotenv
import requests
import os

load_dotenv()

posts = Blueprint('page_posts', __name__, template_folder='templates')
@cache.cached(timeout=5)
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
               

            # Salvar dados diretamente no banco
            criando_post(username, post_img_path)

            # Preparar dados para a API externa (com JSON)
            data = {
                'nome': username,
                'titulo': titulo,
                'post': post_content,
            }
            print(data)
            # Adicionar arquivo, se existir
            files = None
            if post_image:
                files = {
                    'file': (img_filename, open(post_img_path, 'rb'), post_image.content_type)
                }

            headers = {'Authorization': f'Bearer {current_user.token}'}
            print(headers)

            # Enviar requisição para a API externa com o tipo de conteúdo 'multipart/form-data'
            response = requests.post("https://api-devorbirt.onrender.com/post/", data=data, files=files, headers=headers)

            # Verificar resposta da API
            if response.status_code == 200:
                flash('Post criado com suceso')

                next_page = session.get('next', url_for('home.home_page'))
                return redirect(next_page)


            else:
                error_msg = response.json().get('detail', 'Erro desconhecido')
                flash(f"Erro ao enviar para a API: {error_msg}", 'error')
                return redirect(request.url)

        except Exception as e:
            flash(f"Erro ao criar o post: {str(e)}", 'error')
            with open(os.getenv('LOGS'), 'w') as f:
                f.write('{}\n'.format(e.__class__.__name__))
            return redirect(request.url)

    return render_template('post.html', username=current_user.username, id=current_user.id)
