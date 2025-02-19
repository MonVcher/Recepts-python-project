import os
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from forms.Recepts import RegisterForm, SearchForm, LoginForm
from data.Recepts import Search, Recept, Users
from sqlalchemy import create_engine, select 
from data import db_session
from sqlalchemy.orm import Session
from func.export_xlsx import extand_xlsx_file
from func.system import rem, cmd_command
from ultralytics import YOLO
import subprocess

model = YOLO("yolo11n-cls.pt")
# from databases import engine
# # yolo predict model=yolo11x-cls.pt source='test_1.png'
# Session = sessionmaker(engine)
UPLOAD_FOLDER = 'static/images'
sqlite_database = "sqlite:///blogs.db"
engine = create_engine(sqlite_database, echo=True)
session = Session(engine, future=True)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '322'
login_manager.login_view = 'login'
zapros = ''


def main():
    db_session.global_init("db/blogs.db")
    app.run(debug=True)

def search_in_bd(zapros, db_sess):
    li=[]
    zapros = zapros.split(', ')
    recept = db_sess.query(Recept).all()
    recept = filter(lambda x: sum([i in x.products for i in zapros]) >= (len(zapros)*(75/100)), recept)
    for i in recept:
        li.append(f"<a href='{i.recept}'>{i.name}</a>")
    db_sess.commit()
    return li

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(Users, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def search():
    global zapros
    form = SearchForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        # os.remove('static/images/test_1.png')
        item = Search()
        item.text = form.products.data
        search_in_bd(zapros, db_sess)
        img_file = secure_filename(form.photo.data.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], img_file)
        form.photo.data.save(path)
        item.photo = path
        fr_neiro = cmd_command(f'yolo predict model=yolo11x-cls.pt source="static/images/{img_file}"')
        db_sess.add(item)
        if fr_neiro:
            zapros = item.text + ', ' + fr_neiro
        else:
            zapros = item.text
        print(zapros)
        db_sess.commit()
        return redirect('/demonstrarion')
    return render_template("search.html", form=form, title="Из чего будем готовить?")

@app.route("/demonstrarion")
def demonstrarion():
    global zapros
    db_sess = db_session.create_session()
    items = db_sess.query(Recept).filter().all()
    trtp = len(items) != 0
    # db_sess = db_session.create_session()
    # path = "func/exp.xlsx"
    # extand_xlsx_file(db_sess, path)
    # if some:
    #     print(some)
    # rem('static\images')
    return render_template("demonstrarion.html",
                           items=items,
                           trtp=trtp,
                           option=search_in_bd(zapros, db_sess),
                           title="Вот, что мы нашли"
                           )

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   )
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.name == form.name.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message= "Такой пользователь уже есть",
                                   )
        user = Users(name=form.name.data,
                     password=form.password.data,
                     )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               )
    return render_template('login.html',
                           title='Авторизация',
                           form=form,
                           )

if __name__ == '__main__':
    main()