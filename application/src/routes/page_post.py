from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
import requests, json
from application.src.database.users.configure_users import my_db


posts = Blueprint('page_posts', __name__, template_folder='templates')



# Exibir a página de criação de posts
@posts.route('/Codechamber/feed/posts', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        post_content = request.form.get('post-content')  # Obtendo conteúdo do post
        titulo = request.form.get('post-titulo')
        post_image = request.files.get('post-image')  # Se precisar enviar uma imagem
        username = current_user.username  # Obtendo o nome do usuário logado

        # Verificar se o conteúdo do post foi preenchido
        if not post_content:
            flash('O conteúdo do post não pode estar vazio.', 'error')
            return redirect(request.url)

        # Preparando os dados para enviar para a API
        post_data = {
            'nome': username,
            'titulo': titulo,
            'post': post_content
        }

        try:
            # Enviar o post para a API
            response = requests.post("http://localhost:5000/posts", json=post_data, timeout=30)

            if response.status_code == 201:
                flash('Post criado com sucesso!')
                return redirect(url_for('home.home_page'))  # Redirecionar para a página inicial
            else:
                flash('Erro ao criar o post. Tente novamente.', 'error')
        except requests.exceptions.RequestException as e:
            flash(f"Erro de requisição: {e}", 'error')
            
        except requests.exceptions.ReadTimeout as ErroTimeaut:
            flash(f'Erro de Timeout, verifique sua conexão à internet. {ErroTimeaut.args[0]}')
            return redirect(url_for('perfil.profile_page'))  # Redirecionamento para erro de timeout

        except requests.exceptions.JSONDecodeError as ErroJson:
            flash("Erro no servidor, estamos passando por problemas internos. Por favor, tente acessar outras rotas em breve.")
            return redirect(url_for('errorHttp.page_erro'))  # Redirecionamento para erro de JSON


    return render_template('post.html', usuario_nome=current_user.username)
