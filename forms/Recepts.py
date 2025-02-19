from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    products = StringField('Добавить к поиску')
    photo = FileField('Изображение ваших продуктов')
    submit = SubmitField("Отправить")

class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    name = StringField("Имя")
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    status = StringField("Статус")
    submit = SubmitField('Войти')
    reg_submit = SubmitField('Зарегистрироваться')