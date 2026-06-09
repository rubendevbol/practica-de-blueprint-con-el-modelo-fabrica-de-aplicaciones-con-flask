from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import current_user

from blueprintapp.app import db

bp_core = Blueprint('bp_core',__name__,template_folder='templates')

@bp_core.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('core/index.html')