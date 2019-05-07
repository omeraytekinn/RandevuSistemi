from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı')
    password = PasswordField('Şifre')
    auth = SelectField('Giriş Türü',
                        choices=[('ogr','Öğrenci'),('ogu','Öğretim Üyesi'),('yon','Yönetici')])
    submit = SubmitField("Giriş Yap");
