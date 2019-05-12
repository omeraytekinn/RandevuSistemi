from flask import Flask, render_template, redirect, url_for ,session, flash
from functools import wraps
from form import LoginForm, OgrenciProfilForm
import Classes

app = Flask(__name__)

app.config['SECRET_KEY']  = "123456"


stdnav = [
    {
        'value':'Profil',
        'link':'profile'
    },
    {
        'value':'Randevu İşlemleri',
        'link':'#',
        'alt':True #dropdown link
    },
    {
        'value':'Randevu Talep Et',
        'link':'randevutalep',
        'top':True #dropdown element
    },
    {
        'value':'Randevularım',
        'link':'randevular',
        'top':True,
        'end':True #dropdown last element
    }
]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return decorated_function



@app.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        real_password=Classes.GetPassword(username)
        if real_password == password:
            session["logged_in"]=True
            session["username"]=username
            flash('Giriş Başarılı!', 'success')
            return redirect(url_for('profile'), code=302)
        else:
            flash('Hatalı Bilgi Girişi!', 'error')
    return render_template('login.html', form=form)

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = OgrenciProfilForm()
    if form.validate_on_submit():
        ad=form.ad.data
        soyad=form.soyad.data
        email=Classes.GetPassword(username)
        flash('Bİlgileriniz Kaydedildi!', 'success')
        return redirect(url_for('profile'))
    ### Burada auth ile kullanıcı tipi gönderiliyor
    ### Burada auth, loginde yapılan giriş türüne göre
    ### ogrenci, ogretmen, yonetici değerlerini alabilir
    ### ona göre yaparsınız artık bunu
    return render_template('profil_layout.html', navbar=stdnav, form=form, auth='ogrenci')

@app.route('/randevular')
@login_required
def randevular():
        return render_template('randevular.html', navbar=stdnav)


@app.route('/randevutalep')
@login_required
def randevutalep():
        return render_template('randevu_talep.html', navbar=stdnav)

@app.route('/logout')
def logout():
        session.clear()
        flash('Çıkış Başarılı', 'success')
        return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
