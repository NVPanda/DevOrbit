from flask import Flask, url_for
from application.src.database.users.configure_users import create_database
from flask_caching import Cache
from flask_login import LoginManager, UserMixin
from flask_restx import Api
from application.src.api.upload_file import register_file_routes, caminho_img, send_from_directory
from application.src.database.configure_post import initialize_posts_schema
import asyncio



from fastapi import FastAPI
import os
import sqlite3
from dotenv import load_dotenv



load_dotenv()  # Carregando as variáveis de ambiente
cache = Cache()  # Instância da classe Cache


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
    # Criando a aplicação Flask
    
    app = Flask(__name__,  static_url_path='/static')
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['SECRET_KEY'] = os.getenv('KEY')
    app.config['CACHE_TYPE'] = os.getenv('CACHE')
    app.config['UPLOAD_FOLDER'] = os.path.abspath("application/src/static/uploads")
    app.add_url_rule('/files/<filename>', endpoint='files', view_func=send_from_directory, defaults={'directory': caminho_img})
    
   

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print("Diretório de uploads:", app.config['UPLOAD_FOLDER'])

    # Registrar blueprints
    from application.src.routes.home import login_, logout_, home_, erro_http_
    from application.src.routes.register import register_
    from application.src.routes.perfil import profile
    from application.src.routes.page_post import posts
    from application.src.routes.denucia import denucia
    from application.src.routes.configuracao import configuracao_

    app.register_blueprint(home_)
    app.register_blueprint(login_)
    app.register_blueprint(register_)
    app.register_blueprint(logout_)
    app.register_blueprint(profile)
    app.register_blueprint(erro_http_)
    app.register_blueprint(posts)
    app.register_blueprint(denucia)
    app.register_blueprint(configuracao_)


    # Banco de dados
    create_database()
    
    initialize_posts_schema()
   
   

    # Configuração do Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Corrige a referência à página de login
    login_manager.login_view = 'login.login_page'

    """"""
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    
    api = Api(app, version="1.0", title="API da Aplicação", description="Endpoints REST com Flask-RESTx")
    register_file_routes(api)


    

    # Configuração de cache
    cache.init_app(app)

    CONFIG = {
        "DEBUG:": True,
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_NO_NULL_WARNING": True,
    }

    app.config.update(CONFIG)

    return app

app = create_app()