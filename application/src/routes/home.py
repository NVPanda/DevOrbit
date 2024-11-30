import os
from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from application.src.services.api_service import dataRequests
from application.src.__main__ import cache
from dotenv import load_dotenv
import requests

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Blueprint
home_ = Blueprint('home', __name__, template_folder='templates')

# Função para gerar uma chave de cache específica para cada usuário
@login_required
def make_cache_key():
    """
    Gera uma chave única de cache para cada usuário logado.
    Combina o ID do usuário e o caminho da requisição.
    """
    return f"{current_user.id}:{request.path}"

@home_.route('/devorbit/feed/', methods=['POST', 'GET'])
@login_required
@cache.cached(timeout=20, key_prefix=make_cache_key)
def home_page():
    """
    Mostra todos os posts dos usuários, incluindo quem postou, data, quantidade de likes, 
    e serve como a rota principal do feed.
    """
    # Dados do usuário atual
    usuario = current_user.username

    # Requisição de dados dos posts
    data = dataRequests()
    
    # Renderizar a página inicial com os dados necessários
    return render_template(
        'home.html',
        username=current_user.username,
        id=current_user.id,
        posts=data['todos_os_posts'], 
        post_banner=data['post_banner'], 
        usuario=usuario
    )
