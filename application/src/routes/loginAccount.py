from application.src.__main__ import cache
from flask import Blueprint, render_template, url_for, request, redirect, session
from flask_login import login_user, current_user
from application.src.database.users.configure_users import Login, check_user_login, User



login_ = Blueprint('login', __name__, template_folder='templates')
@cache.cached(timeout=5)
@login_.route('/devorbit/login/', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar o login
        try_login = Login(email, password)
        is_valid, user_id, pwd, username = check_user_login(try_login)

        

        if try_login and  is_valid:
            # Cria a instância do usuário com o ID e o nome
            user = User(user_id, username)
            # Faz login do usuário usando Flask-Login
            login_user(user)
            
            # Adiciona informações do usuário na sessão
            session['user'] = {'name': current_user.username, 'id': current_user.id}
            
            # Redireciona para a página desejada ou para a home
            next_page = session.get('next', url_for('username_page.register_username'))
            return redirect(next_page)
        else:
           
            return redirect(url_for('login.login_page'))

    return render_template('login.html')
