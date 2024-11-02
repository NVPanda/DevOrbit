from flask import Blueprint, render_template
from flask_login import current_user, login_required

profile = Blueprint('perfil', __name__, template_folder='templates')

@profile.route('/perfil/usuario/')
@login_required
def profile_page():


    return render_template('profile.html', username=current_user.username)


    