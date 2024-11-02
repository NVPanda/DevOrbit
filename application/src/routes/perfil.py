from flask import Blueprint, render_template
from flask_login import current_user, login_required
from application.src.__main__ import cache
from markupsafe import escape


profile = Blueprint('perfil', __name__, template_folder='templates')

@profile.route('/CodeChamber/perfil/<usuario>/')
@login_required
@cache.cached(timeout=50)
def profile_page(usuario):
    
    usuario = escape(usuario)
    
    
    return render_template('profile.html', usuario=usuario, username=current_user.username)
