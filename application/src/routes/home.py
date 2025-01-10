from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from application.src.services.api_service import dataRequests
from application.src.services.user_service import get_user_info, UserData
from application.src.models.recommendations import recommendationsUser
from application.src.__main__ import cache
import requests
import logging 

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
@cache.cached(timeout=100, key_prefix=make_cache_key)
def home_page():
    """
    Mostra todos os posts dos usuários, incluindo informações de quem postou,
    data, contagem de likes, e serve como rota principal do feed.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    try:
        
        data = dataRequests() # Request post data
        print()
        print(current_user.id)
        print(current_user.username)

        if not isinstance(data, (dict)):
            try:
                data = dict(data)
            except (ValueError, TypeError):
                print("Erro: os dados recebidos não puderam ser convertidos para um dicionário.")
                return redirect(url_for('errorHttp.page_erro'))
        
        if not data or "todos_os_posts" not in data or "post_banner" not in data:
            print("Erro: dados incompletos ou ausentes.")
            return redirect(url_for('errorHttp.page_erro'))
        
        posts = data["todos_os_posts"] # Get the posts and banner
        post_banner = data["post_banner"] # Get posts and banner

       
        recommendations = recommendationsUser()  # Obtaining user recommendations and information
        get_user = get_user_info(current_user.username)
        if not get_user:
            return redirect(url_for('errorHttp.page_erro'))

        user_info = get_user[0]  # Usar o primeiro (e único) dicionário retornado
        photo_user_profile = user_info.get('user_photo', None)
        

        searching_account_data = UserData(current_user.id)
        if not searching_account_data:
            return redirect(url_for('errorHttp.page_erro'))
        
        username = searching_account_data[0]['username']
        user_id = searching_account_data[0]['id']
       
        likes = [post['likes'] for post in posts if post['likes'] >= 0] # This line creates a list called "likes", containing only the number of likes for the posts. 
        # It filters posts, including only those whose number of likes is greater than or equal to zero, 
        # ensuring that negative values ​​are discarded.        


        if current_user.is_authenticated: # Render the page with logged in or public user information
            return render_template(
                'home.html',
                username=username,
                usuario=current_user.username,
                photo_user_profile=photo_user_profile,
                id=current_user.id,
                posts=posts,
                post_banner=post_banner,
                recommendations=recommendations,
                likes=likes
            )
        else: # visitor users
            return render_template(
                'home.html',
                id=user_id,
                posts=posts,
                post_banner=post_banner,
                likes=likes
            )
       
    except Exception as e:  # Loga o erro e redireciona para uma página de erro
        print(f"Erro ao carregar a página inicial: {e} : {e.__class__.__name__} : {e.__cause__}")
        return redirect(url_for('errorHttp.page_erro'))
       
    except requests.exceptions.InvalidURL as e:
        return redirect(url_for('home_home_page'))