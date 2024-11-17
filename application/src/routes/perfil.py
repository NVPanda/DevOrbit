import cProfile
import requests
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.database.users.configure_users import my_db
import pstats
from io import StringIO

API_REDE = "http://localhost:5000/allpost"
profile = Blueprint('perfil', __name__, template_folder='templates')

@profile.route('/devorbit/perfil/<usuario>/')
@login_required
@cache.cached(timeout=100)
def profile_page(usuario):
    # Cria o cProfile
    profiler = cProfile.Profile()
    profiler.enable()  # Começa a medir o desempenho

    # Função que será monitorada
    result = measure_performance(usuario)

    profiler.disable()  # Para a medição de desempenho
    
    # Aqui geramos um relatório legível
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')  # 'cumulative' organiza os resultados pela quantidade de tempo acumulado
    ps.print_stats()  # Imprime o relatório no StringIO
    

    # Futuramente envia o resultado 1 por mes para um arquivo separado do app

    # Retorna o resultado da função
    return result

def measure_performance(usuario):
    # Verifica se o usuário existe no banco de dados
    banco, cursor = my_db()
    cursor.execute('SELECT id FROM usuarios WHERE name = ?', (usuario,))
    user = cursor

    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('home.home_page'))  # Redireciona caso o usuário não seja encontrado

    # Faz a requisição para obter os posts da API
    response = requests.get(API_REDE, timeout=5)

    posts_conta_usuario = []

    meus_posts = response.json()
    if response.status_code == 200:
        # Filtra os posts para o usuário atual
        for meu_post in meus_posts:
            if meu_post['nome'] == usuario:
                posts_conta_usuario.append({
                    'nome': meu_post['nome'],
                    'data': meu_post['data'],
                    'posts': meu_post['post'],
                    'likes': meu_post['likes']
                })

    # Retorna os posts e outras informações
    return render_template('profile.html', usuario=usuario, username=current_user.username, posts=posts_conta_usuario)
