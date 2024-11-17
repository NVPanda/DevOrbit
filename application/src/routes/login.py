from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from application.src.database.users.configure_users import Login, check_user_login, User
from dotenv import load_dotenv
import requests
from time import sleep
import os

load_dotenv()

login_ = Blueprint('login', __name__, template_folder='templates')
logout_ = Blueprint('logout', __name__, template_folder='templates')
home_ = Blueprint('home', __name__, template_folder='templates')
erro_http_ = Blueprint('errorHttp', __name__, template_folder='templates')



class User(UserMixin):
    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

   # Função que busca usuario pelo id 
    def get_id(self):
        return str(self.id)


@login_.route('/devorbit/login/', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try_login = Login(email, password)
        is_valid, user_id, username = check_user_login(try_login)
        
        if is_valid:
            # Cria a instância do usuário com o ID e o nome
            user = User(user_id, username)
            # Faz login do usuário usando Flask-Login
            login_user(user)
            flash('Login bem-sucedido!')

            next_page = session.get('next', url_for('home.home_page'))
            return redirect(next_page)
        
        else:
            flash('Email ou senha inválidos. Tente novamente.')
            return redirect(url_for('login.login_page'))

    return render_template('login.html')


@home_.route('/devorbit/feed/')
@login_required
def home_page():

    """
    (pt-br)
    A função home mostra todos os posts dos usuários,
    como quem postou, data, quantidade de likes em geral e nossa rota principal.

    (en)
    The home function shows all user posts, such as who posted, date, number of likes in general and our main route.
    """

    try:

        response = requests.get(os.getenv('API_REDE'), timeout=10)
        requesting_all_posts = response.json()
        

        if requesting_all_posts:
            requesting_all_posts.sort(key=lambda post: (post["likes"], post["data"]), reverse=True)

        
        lista_do_melhor_post = [{

            'nome': column['nome'],
            'titulo': column['titulo'],
            'data': column['data'][10:16],
            'post': column['post'],
            'likes': column['likes']
            }
                for column in requesting_all_posts
        ]
  
        
        print(lista_do_melhor_post[0]['data'][10:16], '<------ data reve')

        
        posts_filter = []
        for post_do_momento in lista_do_melhor_post:
            likes = int(post_do_momento['likes'])
                
            if likes >= 30:
                posts_filter.append({
                'post_titulo': post_do_momento['titulo'],
                'post': post_do_momento['post'],
                'post_nome': post_do_momento['nome'],
                'data_post': post_do_momento['data']
                })
                
                
            elif likes <= 10 and len(posts_filter) == 0:
                """
                (pt-br)
                Caso não tenha post em alta, esse elif retorna a mensagem padrão no campo de melhores posts.
                (en)
                If there is no trending post, this elfie returns the default message.
                """ 
                posts_filter.append({
                'post_titulo': os.getenv('MENSAGEN'),
                'post': os.getenv('MENSAGEN_POST'),
                'post_nome': os.getenv('CODECHAMBER'),
                'data_post': 'N/A'
        })
                break


    except requests.exceptions.InvalidSchema as ErrorHttp:

        flash(f"Erro HTTP ou HTTPS: Você precisa incluir métodos válidos. {ErrorHttp.args[0]} Você está sendo redirecionado.")
        return redirect(url_for('errorHttp.page_erro'))  # Redirecionamento após erro

    except requests.exceptions.ReadTimeout as ErroTimeaut:
        flash(f'Erro de Timeout, verifique sua conexão à internet. {ErroTimeaut.args[0]}')
        return redirect(url_for('perfil.profile_page'))  # Redirecionamento para erro de timeout

    except requests.exceptions.JSONDecodeError as ErroJson:
        flash("Erro no servidor, estamos passando por problemas internos. Por favor, tente acessar outras rotas em breve.")
        return redirect(url_for('errorHttp.page_erro'))  # Redirecionamento para erro de JSON

    
    # Use current_user.username para exibir o nome do usuário logado
    return render_template('home.html', username=current_user.username, posts=requesting_all_posts, post_banner=posts_filter)


@logout_.route('/devorbit/logout')
@login_required
def logout():

    logout_user()  # Desloga o usuário
    flash('Você foi desconectado')
    return redirect(url_for('login.login_page'))


@erro_http_.route('/devorbit/erro_http/')
@login_required
def page_erro():

    try:
        response = requests.get(os.getenv('API_REDE'), timeout=1)
        status = response.status_code
        if status == 200:
            yield sleep(3)
            return redirect(url_for('home.home_page'))
        
    
    except requests.exceptions as e:
        return redirect(url_for('errorHttp.page_erro'))



    return 'Erro HTTP ou HTTPS: Você precisa incluir métodos válidos. Você está sendo redirecionado', redirect(url_for('/Codechamber/feed/'))