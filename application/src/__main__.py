from flask import Flask, url_for
from application.src.database.users.configure_users import create_datebase
from flask_caching import Cache
from flask_login import LoginManager, UserMixin
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv() # Carregando as variaves de ambiente
cache = Cache() # Instacia da class cache



# Função para obter a conexão com o banco de dados
def get_db_connection():
    return sqlite3.connect('usuarios.db')

# Classe User com suporte ao Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM usuarios WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return User(user[0], user[1])
        return None


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['SECRET_KEY'] = os.getenv('KEY')
    app.config['CACHE_TYPE'] = os.getenv('CACHE')

    # Registrar blueprints
    from application.src.routes.login import login_, logout_, home_
    from application.src.routes.register import register_
    from application.src.routes.perfil import profile


    app.register_blueprint(home_)
    app.register_blueprint(login_)
    app.register_blueprint(register_)
    app.register_blueprint(logout_)
    app.register_blueprint(profile)

    


    # Banco de dados
    create_datebase()

    # Configuração do Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Corrige a referência à página de login
    login_manager.login_view = 'login.login_page'

    @login_manager.user_loader
    def load_user(user_id):
        # Usar o método estático `get` para buscar o usuário
        return User.get(user_id)

    '''Registrar rota da API'''
    from application.src.routes.api_docs.route_api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    '''Abaixo temos a função que ira fazer cache das rotas home, perfil'''
    cache.init_app(app)


    CONFIG={
            "DEBUG:": True,
            "CACHE_DEFAULT_TIMEOUT": 300,
            "CACHE_NO_NULL_WARNING":True
        }

    app.config.update(CONFIG)

    return app


