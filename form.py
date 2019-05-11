from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms_components import DateTimeField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı')
    password = PasswordField('Şifre')
    auth = SelectField('Giriş Türü',
                        choices=[('ogr','Öğrenci'),('ogu','Öğretim Üyesi'),('yon','Yönetici')])
    submit = SubmitField("Giriş Yap");

class OgrenciProfilForm(FlaskForm):
        ad = StringField('Ad:')
        soyad = StringField('Soyad:')
        email = StringField('Email:', validators=[Email()])
        telefon = TelField('Telefon No:')
        adres = StringField('Adres:', widget=TextArea())

class OgretmenProfilForm(FlaskForm):
        ad = StringField('Ad:')
        soyad = StringField('Soyad:')
        email = StringField('Email:', validators=[Email()])
        telefon = TelField('Telefon No:')
        adres = StringField('Adres:', widget=TextArea())

class YoneticiProfilForm(FlaskForm):
        ad = StringField('Ad:')
        soyad = StringField('Soyad:')
        email = StringField('Email:', validators=[Email()])
        telefon = TelField('Telefon No:')
        adres = StringField('Adres:', widget=TextArea())
