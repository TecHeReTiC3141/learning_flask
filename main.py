from app import *
from flask import render_template, url_for, \
    request, flash, session, redirect, abort, g, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from scripts.DataBase import *
from scripts.UserLogin import *

player_classes = ['choose your class', 'medic',
                  'scout', 'soldier']

class_info = {
    'Heavy': 'Сильный, мощный и медленный',
    'Melee': 'Быстрый, но хлипкий пехотинец',
    'Medic': 'Лечит союзников',
    'Pyro': "It's madness"
}

pages_list = [
    {'url': '/classes', 'descr': 'Посмотри список всех классов TecHeres'},
    {'url': '/feedback', 'descr': 'Пожалуйста, оставь отзыв'},
    {'url': '/login', 'descr': 'Логин/Вход в профиль'},
    {'url': '/news', 'descr': 'Посмотри последние новости'},
]

dbase: DataBase = None


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


@app.before_first_request
def get_db() -> sqlite3.Connection:
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def get_dbase():
    global dbase
    dbase = DataBase(get_db())


@app.route('/')
@app.route('/mainpage')
def homepage():
    return render_template('home_page.html')


@app.route('/classes')
def classes():
    return render_template('classes.html', class_list=dbase.getClasses())


@app.route('/classes/<class_name>')
def class_descr(class_name):
    if class_name in class_info:
        return f'Meet the {class_name}! {class_info[class_name]}'
    return render_template('404error.html')


@app.route('/feedback', methods=['POST', 'GET'])
@login_required
def feedback():
    if request.method == 'POST':
        if len(request.form['username']) > 3:
            flash('Successfully sent', category='success')
        else:
            flash('Error while sending', category='error')
        print(request.form)

    return render_template('feedback.html')


@app.route('/avatar')
@login_required
def get_avatar():
    img = current_user.avatar
    if not img:
        img = ''
    resp = make_response(img)
    resp.headers['Content-type'] = 'image/png'
    return resp


@app.route('/profile/<name>', methods=['POST', 'GET'])
@login_required
def profile(name):
    if current_user.name == name:
        if request.method == 'POST':
            logout_user()
            flash('Successfully logout', category='success')
            return redirect(url_for('login'))
        return render_template('player_greeting.html',
                               user_name=name, user=current_user, classes=player_classes,
                               pages_list=pages_list)
    abort(401)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img and current_user.checkExt(img.filename):
            res = dbase.updateUserAvatar(img.read(), current_user.get_id())
            flash(res, category='success' if res == 'Successfully modified' else 'error')
        else:
            flash('Wrong image extension. Please, use PNG', category='error')
    return redirect(url_for('profile', name=current_user.name))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', name=current_user.name,
                                pages_list=pages_list))
    elif request.method == 'POST':
        user = dbase.getUser(request.form['username'])

        if not user:
            flash('Wrong username or password', category='error')
        else:
            user_password = user['password']
            if check_password_hash(user_password, request.form['psw']):
                user_login = UserLogin().create(user)
                remember = True if request.form.get('remember') else False
                login_user(user_login, remember=remember)
                flash('Successfully logged', category='success')
                return redirect(request.args.get('next') or url_for('profile', name=current_user.name,
                                                                    pages_list=pages_list))
            else:
                flash('Wrong username or password', category='error')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile', name=current_user.name,
                                pages_list=pages_list))
    if request.method == 'POST':
        name, email, psw, rep_psw = request.form['username'], \
                                    request.form['email'], request.form['psw'], request.form['repeat psw']
        res = dbase.addUser(name, email, generate_password_hash(psw)) if psw == rep_psw else "Passwords don't match"

        flash(res, 'success' if res == 'Successfully added' else 'error')
        if res == 'Successfully added':
            user = UserLogin().create(dbase.getUser(name))
            login_user(user)
            return redirect(url_for('profile', name=current_user.name,
                                    pages_list=pages_list))
    return render_template('register.html')


@app.route('/news')
def news_list():
    news = dbase.getNews()
    top_users = dbase.getTopKUsers()
    return render_template('news.html', news_list=news, top_users=top_users)


@app.route('/news/<title>')
@login_required
def show_article(title):
    dbase = DataBase(get_db())
    article = dbase.getNews(title=title)
    if not article:
        abort(404)
    if 'articles_visits' not in session:
        session['articles_visits'] = {}
    if current_user.is_authenticated:
        if title not in session['articles_visits']:
            session['articles_visits'][title] = [current_user.name]
            session.modified = True
            dbase.viewNews(title)
        elif current_user.name not in session['articles_visits'][title]:
            session['articles_visits'][title].append(current_user.name)
            session.modified = True
            dbase.viewNews(title)
    print(session['articles_visits'])

    return render_template('article_text.html', article=article)


@app.route('/add_article', methods=['POST', 'GET'])
@login_required
def add_article():
    if request.method == 'POST':
        title, content = request.form['title'], request.form['text']
        res = dbase.addNews(title, content, current_user.name)
        flash(res, 'success' if res == 'Successfully added' else 'error')
        if res == 'Successfully added':
            return redirect(url_for('show_article', title=title))

    return render_template('add_article.html')


@app.errorhandler(404)
def PageNotFound(error):
    return render_template('404error.html')


@app.errorhandler(401)
def Unauthorized(error):
    return render_template('401error.html')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)
