from flask import Blueprint,  url_for, redirect
from flask_login import logout_user, login_required

logout_ = Blueprint('logout', __name__, template_folder='templates')


@logout_.route('/devorbit/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('login.login_page'))