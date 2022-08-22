import sqlite3
from flask import Blueprint, g, \
    session, redirect, url_for, flash, request, render_template
from scripts.WTForms import *
from scripts.DataBase import *
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

pages_list = [
    {'url': '.list_users', 'descr': 'List of users'},
    {'url': '.panel', 'descr': 'Admin panel'},

]

@admin.before_request
def before_request():
    global db
    db = DataBase(g.get('link_db'))


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not session.get('AdminLogged'):
        return redirect(url_for('.login'))
    return render_template('admin/admin_base.html', pages_list=pages_list)


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('AdminLogged'):
        return redirect(url_for('.index', pages_list=pages_list))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.getUser(form.user.data)
        if not user:
            flash('Wrong username or password', category='error')
        elif not user['is_admin']:
            flash('This user has no admin permissions', category='error')
        else:
            user_password = user['password']
            if check_password_hash(user_password, form.password.data):
                session['AdminLogged'] = user['name']
                flash('Successfully logged', category='success')
                return redirect(request.args.get('next') or url_for('.index',
                                                                    pages_list=pages_list))
            flash('Wrong username or password', category='error')

    return render_template('admin/login.html', form=form)


@admin.route('/list_users')
def list_users():
    users = db.getUsers()
    return render_template('admin/list_users.html', users=users)


@admin.route('/list_users')
def panel():
    return 'panel'
