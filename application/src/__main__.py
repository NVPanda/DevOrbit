from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager, UserMixin
from flask_restx import Api
from flask_cors import CORS

from application.src.database.users.configure_users import create_database,add_column
from application.src.api.upload_file import register_file_routes, caminho_img, send_from_directory
from application.src.database.configure_post import banco_post, criar_tabela_post


import os
import sqlite3
from dotenv import load_dotenv
import logging 

cache = Cache()
load_dotenv()


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
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    # Criando a aplicação Flask
    
    app = Flask(__name__,  static_url_path='/static')
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['SECRET_KEY'] = os.getenv('KEY')
    app.config['CACHE_TYPE'] = os.getenv('CACHE')
    app.config['UPLOAD_FOLDER'] = os.path.abspath("application/src/static/banners")
    
    app.add_url_rule('/files/<filename>', endpoint='files', view_func=send_from_directory, defaults={'directory': caminho_img})
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    logging.debug("CORS configurado com sucesso.")
    hashing = Bcrypt(app)
    

    # Registrar blueprints
    from application.src.routes.home import home_
    
    app.register_blueprint(home_)
   

    from application.src.routes.loginAccount import login_
    app.register_blueprint(login_)

    from application.src.routes.logoutAccont import logout_
    app.register_blueprint(logout_)

    from application.src.routes.register import register_
    app.register_blueprint(register_)

    from application.src.routes.perfil import profile, viws_img
    app.register_blueprint(profile)
    app.register_blueprint(viws_img)

    from application.src.routes.page_post import posts
    app.register_blueprint(posts)

    from application.src.routes.denucia import denucia
    app.register_blueprint(denucia)

    from application.src.routes.configuracao import configuracao_
    app.register_blueprint(configuracao_)

    from application.src.routes.page_erro import erro_http_
    app.register_blueprint(erro_http_)

    from application.src.routes.username import username_unic
    app.register_blueprint(username_unic)

    from application.src.routes.username import termosEcondicao
    app.register_blueprint(termosEcondicao)
    

    create_database() # Banco de dados
    add_column() # add coluna no banco
    banco_post() # banco de dados para posts | Null
    criar_tabela_post() # init tabalas
   
   

    # Configuração do Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
   
   # Pagina padrão de login
    login_manager.login_view = 'login.login_page'

    
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

    # Logs iniciais para monitoramento
    logging.info("Inicializando aplicação Flask...")

    return app



