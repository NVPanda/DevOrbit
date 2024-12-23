from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from application.src.database.users.configure_users import add_user, my_db
from application.src.models.modelsUser import Cadastro
from application.src.database.users.configure_users import User  
from flask_login import login_user


register_ = Blueprint('register', __name__, template_folder='templates')

@register_.route('/devorbit/register/', methods=['POST', 'GET'])
def page_register():
    if request.method == 'POST':
        name = request.form['name'].capitalize()
        last_name = request.form['lastname'].capitalize()
        email = request.form['email']
        age = request.form['age']
        password = request.form['password']
        confirm_password = request.form['comfirm_password']  

        if password != confirm_password:
            flash("As senhas não coincidem.", "error")
            return redirect(url_for('register.page_register'))
        
        # Cria um objeto de cadastro
        register_in_db = Cadastro(name=name, last_name=last_name, email=email, age=int(age), password=password)
        
        
        # Adiciona o usuário ao banco de dados
        add_user(register_in_db)  # Aqui, chamamos a função add_user para add user

           # Recupera o ID do usuário após o registro
        banco, cursor = my_db()
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        user_id = cursor.fetchone()[0]
        banco.close()

        if register_in_db and add_user and Cadastro:
            session['user'] = {
                'id': user_id,  # Obtenha o ID do banco de dados após o registro
                'name': name,
                'email': email
            }
            info = session['user']
            # autenticando usuarios antes de envia-lo para registra um nome de usuario
            user = User(user_id, name, email)  # Cria o objeto User para autenticação
            login_user(user)

            

            return redirect(url_for('username_page.register_username'))

    return render_template('register.html')
