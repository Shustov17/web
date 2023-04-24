from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
import datetime

from data import db_session
from data.catalog import Catalog
from data.basket import Basket
from data.basket_form import BasketForm
from data.login_form import LoginForm
from data.users import User
from data.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            print(form.remember_me.data)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неверный логин и пароль", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    catalog = db_sess.query(Catalog).all()
    form = BasketForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        basket = Basket(
            id=1,
            catalog_id=1,
            user_id=1,
            basket_kol=1,
            datetime=datetime.datetime.now
        )
        db_sess.add(basket)
        db_sess.commit()
    return render_template("index.html", catalog=catalog, title='Каталог', form=form)


@app.route("/basket")
def basket():
    db_sess = db_session.create_session()
    basket = db_sess.query(Basket).all()
    catalog = db_sess.query(Catalog).all()
    return render_template("basket.html", basket=basket, title='Корзина')
    return render_template("index.html", catalog=catalog, title='Каталог')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/newfootball.db")
    app.run()


if __name__ == '__main__':
    main()
