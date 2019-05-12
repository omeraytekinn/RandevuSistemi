from flask import Flask, render_template, redirect, url_for ,session, flash
from functools import wraps
from form import LoginForm, OgrenciProfilForm
import Classes

app = Flask(__name__)

app.config['SECRET_KEY']  = "123456"


stdnavOfStudent = [
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

stdnavOfTeacher = [
    {
        'value':'Profil',
        'link':'profile'
    },
    {
        'value':'Randevularım',
        'link':'randevular',
        'alt':True #dropdown link
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
    if "logged_in" in session:#login islemi yapildi ise profil sayfasına yönlendir
            return redirect(url_for("profile"))
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        real_password=Classes.GetPassword(username)
        if real_password == password:
            session["logged_in"]=True
            session["username"]=username
            session["id"]=Classes.GetId(username)
            flash('Giriş Başarılı!', 'success')
            return redirect(url_for('profile'), code=302)
        else:
            flash('Hatalı Bilgi Girişi!', 'error')
    return render_template('login.html', form=form)

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = OgrenciProfilForm()
    user=Classes.GetUser(session['id'])

    if user.user_type == 'Student':
        navbar=stdnavOfStudent
    if user.user_type == 'Teacher':
        navbar=stdnavOfTeacher

    if form.validate_on_submit():
        ad=form.ad.data
        soyad=form.soyad.data
        email=form.email.data
        telefon=form.telefon.data
        adres=form.adres.data
        user=Classes.User(name=ad,surname=soyad,email=email,adres=adres,number=telefon)
        Classes.UpdateUser(session['id'],user)
        return redirect(url_for('profile'))
    ### Burada auth ile kullanıcı tipi gönderiliyor
    ### Burada auth, loginde yapılan giriş türüne göre
    ### ogrenci, ogretmen, yonetici değerlerini alabilir
    ### ona göre yaparsınız artık bunu
    return render_template('profil_layout.html', navbar=navbar, form=form, auth=user.user_type,user=user)

@app.route('/randevutalep')
@login_required
def randevutalep():
        teacher=Classes.GetTeachers()
        return render_template('randevu_talep.html', navbar=stdnavOfStudent,teachers=teacher)


@app.route('/randevular')
@login_required
def randevular():
    return render_template('randevular.html', navbar=stdnavOfStudent)

@app.route('/logout')
def logout():
        session.clear()
        flash('Çıkış Başarılı', 'success')
        return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
