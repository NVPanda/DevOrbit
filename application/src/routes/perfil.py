from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from application.src.__main__ import cache
from markupsafe import escape
from application.src.database.users.configure_users import my_db


profile = Blueprint('perfil', __name__, template_folder='templates')

@profile.route('/CodeChamber/perfil/<usuario>/')
@login_required
@cache.cached(timeout=50)
def profile_page(usuario):

    banco, cursor = my_db()
    cursor.execute('SELECT id FROM usuarios WHERE name = ?', (usuario,))
    user = cursor.fetchone()
    
    if user:
        # Se o usuário existir no banco de dados, renderiza o perfil
        return render_template('profile.html', usuario=usuario, username=current_user.username)
    else:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('home.home_page'))  # Ou para a rota que você preferir
    
    return render_template('profile.html', usuario=usuario, username=current_user.username)
