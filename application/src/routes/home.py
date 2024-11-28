import os
from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from application.src.services.api_service import dataRequests
from dotenv import load_dotenv
import requests

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Blueprint
home_ = Blueprint('home', __name__, template_folder='templates')

@home_.route('/devorbit/feed/', methods=['POST', 'GET'])
@login_required
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