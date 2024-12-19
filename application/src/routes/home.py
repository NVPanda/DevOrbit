from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from application.src.services.api_service import dataRequests
from application.src.services.user_service import get_user_info
from application.src.models.recommendations import recommendationsUser
from application.src.__main__ import cache

# Configuração do Blueprint
home_ = Blueprint('home', __name__, template_folder='templates')

@login_required
def make_cache_key():
    """
    Gera uma chave única de cache para cada usuário logado.
    Combina o ID do usuário e o caminho da requisição.
    """
    return f"{current_user.id}:{request.path}"

@home_.route('/devorbit/feed/', methods=['POST', 'GET'])
@cache.cached(timeout=20, key_prefix=make_cache_key)
def home_page():
    """
    Mostra todos os posts dos usuários, incluindo informações de quem postou,
    data, contagem de likes, e serve como rota principal do feed.
    """
    try:
        # Solicita os dados de postagens
        data = dataRequests()
        # recommendationsUser | Account
        recommendations = recommendationsUser()
        get_user = get_user_info(current_user.username)

        # var sendo usada para verificação
        likes = [post['likes'] for post in data['todos_os_posts'] if post['likes'] >= 0]
       


        # Verifica se os dados esperados estão presentes
        if not data or 'todos_os_posts' not in data or 'post_banner' not in data:
            # Caso os dados estejam ausentes, redireciona para uma página de erro
            return redirect(url_for('errorHttp.page_erro'))

        if current_user.is_authenticated:
            # Renderiza a página com informações do usuário logado
            return render_template(
                'home.html',
                username=current_user.username,
                photo_user_profile=get_user[0]['user_photo'],
                id=current_user.id,
                posts=data['todos_os_posts'],
                post_banner=data['post_banner'],
                recommendations=recommendations,
                likes=likes
            )
        else:
            # Renderiza a página com postagens públicas (sem informações do usuário)
            return render_template(
                'home.html',
                posts=data['todos_os_posts'],
                post_banner=data['post_banner'],
                likes=likes
            )
    except Exception as e:
        # Loga o erro e redireciona para uma página de erro
        print(f"Erro ao carregar a página inicial: {e}")
        return redirect(url_for('errorHttp.page_erro'))
