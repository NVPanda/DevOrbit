from flask import Blueprint, render_template, url_for, request, redirect, session
from flask_login import login_user, current_user
from application.src.database.users.configure_users import Login, check_user_login, User


login_ = Blueprint('login', __name__, template_folder='templates')

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
           
            session['user'] = {'name': current_user.username, 'id': current_user.id}
           

            next_page = session.get('next', url_for('home.home_page'))
            return redirect(next_page)
        
        else:
            return redirect(url_for('login.login_page'))
   

    
    return render_template('login.html')