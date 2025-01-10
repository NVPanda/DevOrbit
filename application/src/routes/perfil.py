from flask import Blueprint, render_template,   send_from_directory, request, redirect, url_for
from flask_login import current_user, login_required
from application.src.__main__ import cache
from application.src.services.api_service import dataRequests
from application.src.services.user_service import get_user_info, UserData


from dotenv import load_dotenv

load_dotenv()

profile = Blueprint('perfil', __name__, template_folder='templates')
viws_img = Blueprint('img', __name__, template_folder='templates')

# Função para gerar uma chave de cache específica para cada usuário
def make_cache_key():
    """
    Gera uma chave única de cache para cada usuário logado.
    Combina o ID do usuário e o caminho da requisição.
    """
    return f"{current_user.id}:{request.path}"

@profile.route('/devorbit/perfil/<usuario>/')
@login_required
@cache.cached(timeout=100, key_prefix=make_cache_key)
def profile_page(usuario):
   
    
    result = measure_performance(usuario)
    return result
   

def measure_performance(usuario):
    
    get_user = get_user_info(current_user.username)
    if not get_user:
        return redirect(url_for('errorHttp.page_erro'))

    user_info = get_user[0]  # Usar o primeiro (e único) dicionário retornado
    photo_user_profile = user_info.get('user_photo', None)
        
    user_photo = get_user[0]['user_photo']

    searching_account_data = UserData(current_user.id)
    username = searching_account_data[0]['username']
    

    if get_user[0]['bio'] is None:
            get_user[0]['bio'] = '''Olá! A comunidade DevOrbit está pronta para te receber.
                Compartilhe seus pensamentos e conecte-se com desenvolvedores apaixonados por inovação.'''
    

    seguir = None

    if usuario != current_user.username:
        seguir = 'Networking'
    else:
         seguir = None 
    

    data = dataRequests()
    if not isinstance(data, dict):
        return data
    
    
    posts_account_user = [
        post for post in data['todos_os_posts'] if post['nome'] == usuario
    ]
    


   # Make sure to pass all necessary variables to the template (Authenticated users)
    if current_user.is_authenticated:
         return render_template('profile.html', 
             username=username, 
             usuario=current_user.username,
            id=current_user.id, posts=posts_account_user, user_photo=user_photo,
            photo_user_profile=photo_user_profile, bio=get_user[0]['bio'], github=get_user[0]['github'], site=get_user[0]['site'], likedin=get_user[0]['linkedin'],
            seguir=seguir, followers=get_user[0]['followers'], following=get_user[0]['following'], banner=get_user[0]['banner'],
             )
    
   # Make sure to pass all necessary variables to the template (Non-authenticated user)
    else:
        return render_template('profile.html',   
                           posts=posts_account_user, 
                           user_photo=get_user[0]['user_photo'], bio=get_user[0]['bio'], banner=get_user[0]['banner'],
                            username=username)


    
@viws_img.route('/files/<path:filename>')
def serve_files(filename):
    return send_from_directory('application/src/static/fotos', filename)