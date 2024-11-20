from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
import requests, json
from application.src.database.users.configure_users import my_db
import base64

posts = Blueprint('page_posts', __name__, template_folder='templates')
@posts.route('/devorbit/feed/posts/', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        titulo = request.form.get('post-titulo')
        post_content = request.form.get('post-content')
        post_image = request.files.get('post-image')  # Imagem enviada pelo formulário
        username = current_user.username  # Nome do usuário logado

        if not post_content:
            flash('O conteúdo do post não pode estar vazio.', 'error')
            return redirect(request.url)

        try:
            # Preparar dados e arquivo para enviar à API
            data = {
                'nome': username,
                'titulo': titulo,
                'post': post_content,
            }
            files = {'file': (post_image.filename, post_image.stream, post_image.mimetype)} if post_image else None

            # Enviar para a API
            response = requests.post("http://127.0.0.1:8000/post/", data=data, files=files)

            if response.status_code == 200:
                flash('Post criado com sucesso!', 'success')
            else:
                flash('Erro ao criar o post.', 'error')

        except Exception as e:
            flash(f"Erro: {e}", 'error')

        return redirect(url_for('home.home_page'))
    return render_template('post.html')
