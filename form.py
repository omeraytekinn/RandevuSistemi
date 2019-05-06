from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                            validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Şifre',
                            validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField("Beni Hatırla")
    submit = SubmitField("Giriş Yap");
