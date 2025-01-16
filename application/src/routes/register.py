from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from application.src.database.users.configure_users import add_user, my_db
from email_validator import validate_email, EmailNotValidError
from application.src.models.modelsUser import Cadastro
from application.src.database.users.configure_users import User  
from flask_login import login_user


register_ = Blueprint('register', __name__, template_folder='templates')

@register_.route('/devorbit/register/', methods=['POST', 'GET'])
def page_register():
    try:

        if request.method == 'POST':
            name = request.form['name']
            last_name = request.form['lastname']
            email = request.form['email']
            age = request.form['age']
            password = request.form['password']
            confirm_password = request.form['comfirm_password']  

            if password != confirm_password:
                flash("As senhas não coincidem.", "error")
                return 'As senhas não coincidem.'
            
            if not all([name, last_name, email, age, password, confirm_password]):
                flash("Todos os campos são obrigatórios.", "error")
                return 'Todos os campos são obrigatórios.'
            
            validate_email(email)
    

            if not age.isdigit() or int(age) < 18:
                flash("A idade deve ser um número válido e maior ou igual a 18.", "error")
                return 'A idade deve ser um número válido e maior ou igual a 18.'
            if len(password) < 8:
                flash("A senha deve ter pelo menos 8 caracteres.", "error")
                return 'A senha deve ter pelo menos 8 caracteres.'
        
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
        
    except ValueError as error:
        print(f'PAGE_REGISTE: {error.__class__.__name__}')

    except EmailNotValidError:
        flash("O -mail fornecido não é válido.", "error")
        return redirect(url_for('register.page_register'))