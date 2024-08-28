from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/') # Main page
def home():
    return render_template('main.html')

# @views.route('/<user>') # Redirct each user's page
# def user_redirect(user_email):
#     return render_template('main.html')

