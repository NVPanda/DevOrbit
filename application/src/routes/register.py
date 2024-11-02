from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from application.src.database.users.configure_users import Cadastro, add_user


register_ = Blueprint('register', __name__, template_folder='templates')

@register_.route('/register', methods=['POST', 'GET'])
def page_register():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['lastname']
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
        append_user = add_user(register_in_db)  # Aqui, chamamos a função add_user

    return render_template('register.html')
