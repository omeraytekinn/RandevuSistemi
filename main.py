from flask import Flask, render_template, redirect, url_for ,session, flash, request, jsonify
from functools import wraps
from form import LoginForm, OgrenciProfilForm, OgretmenProfilForm, YoneticiProfilForm
import Classes
import datetime
from enum import Enum



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
        'link':'randevular'
    }
]

stdnavOfYonetici = [
    {
        'value':'Profil',
        'link':'profile'
    },
    {
        'value':'Randevularım',
        'link':'randevular'
    },
    {
        'value':'Öğrenci Ekle',
        'link':'ogrenciekle'
    },
    {
        'value':'Öğretim Üyesi Ekle',
        'link':'ogretmenekle'
    }
]



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Giriş Yapmanız Gerekiyor!", "error")
            return redirect("/")
    return decorated_function

def login_requiredOfAdmin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "adminmode" in session:
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
        if(username=="admin" and password=="1234"):
            session["adminmode"]=True
            session["navbar"]=stdnavOfYonetici
            return redirect(url_for('ogrenciekle'))
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
    user=Classes.GetUser(session['id'])

    if user.user_type == 'Student':
        session["navbar"]=stdnavOfStudent
        form = OgrenciProfilForm()
    if user.user_type == 'Teacher':
        session["navbar"]=stdnavOfTeacher
        user=Classes.GetTeacher(session['id'])
        form = OgretmenProfilForm()

    if form.validate_on_submit():
        ad=form.ad.data
        soyad=form.soyad.data
        email=form.email.data
        telefon=form.telefon.data
        adres=form.adres.data
        if user.user_type =='Student':
            user=Classes.User(name=ad,surname=soyad,email=email,adres=adres,number=telefon)
            Classes.UpdateUser(session['id'],user)
        else:
            note=form.notes.data
            arastirma=form.research.data
            takvim=form.schedule.data
            teacher=Classes.Teacher(name=ad,surname=soyad,email=email,adres=adres,number=telefon,note=note,arastirma=arastirma,takvim=takvim)
            Classes.UpdateTeacher(session['id'],teacher)
        return redirect(url_for('profile'))
    ### Burada auth ile kullanıcı tipi gönderiliyor
    ### Burada auth, loginde yapılan giriş türüne göre
    ### ogrenci, ogretmen, yonetici değerlerini alabilir
    return render_template('profil_layout.html', navbar=session["navbar"], form=form, auth=user.user_type,user=user)

@app.route('/randevutalep', methods=['POST', 'GET'])
@login_required
def randevutalep():
        form = request.form
        if form:
            hour = form.get('hour')
            minute = form.get('minute')
            date = form.get('date')
            date=date.split("-")
            konu=form.get('topic')
            dateformat=datetime.datetime(int(date[2]),int(date[1]),int(date[0]),int(hour),int(minute))
            teacher_id = form.get('id')
            teacher=Classes.GetTeacher(teacher_id)
            ogrenci=Classes.GetUser(session["id"])
            Classes.TalepOlustur(konu,teacher_id,session["id"],teacher.name,ogrenci.name,dateformat)
            flash('Randevu Başarıyla Kaydedildi!', 'success')
        teacher=Classes.GetTeachers()
        return render_template('randevu_talep.html', navbar=session["navbar"],teachers=teacher)

@app.route('/randevular')
@login_required
def randevular():
    user=Classes.GetUser(session["id"])
    gecmisrandevular=Classes.GetGecmisRandevu(session["id"],user.user_type)
    gelecekrandevular=Classes.GetGelecekRandevu(session["id"],user.user_type)
    taleprandevular=Classes.GetTalepRandevu(session["id"],user.user_type)
    return render_template('randevular_layout.html', navbar=session["navbar"],PastRandevu=gecmisrandevular,GelecekRandevu=gelecekrandevular,TalepRandevu=taleprandevular,user=user)

@app.route('/logout')
def logout():
        session.clear()
        flash('Çıkış Başarılı', 'success')
        return redirect('/')

@app.route('/get/profile/<id>')
def show_profile(id):
    teacher=Classes.GetTeacher(id)
    _teacher = {
        'name': teacher.name,
        'surname': teacher.surname,
        'email': teacher.email,
        'tel' : teacher.number,
        'research': teacher.arastirma,
        'schedule': teacher.takvim,
        'notes': teacher.note
    }
    return jsonify(_teacher)

@app.route('/ogretmenekle', methods=['GET','POST'])
@login_requiredOfAdmin
def ogretmenekle():
    form=request.form
    if form:
        username=form.get('username')
        password=form.get('pass')
        name=form.get('name')
        surname=form.get('surname')
        email=form.get('email')
        tel=form.get('tel')
        adres=form.get('adres')
        Classes.OgretmenEkle(ad=name,soyad=surname,kullanici=username,sifre=password,adres=adres,email=email,number=tel,note="")
    return render_template('ogretmen_ekle.html', navbar=session["navbar"])

@app.route('/ogrenciekle', methods=['GET','POST'])
@login_requiredOfAdmin
def ogrenciekle():
    form=request.form
    if form:
        username=form.get('username')
        password=form.get('pass')
        name=form.get('name')
        surname=form.get('surname')
        email=form.get('email')
        tel=form.get('tel')
        adres=form.get('adres')
        Classes.OgrenciEkle(ad=name,soyad=surname,kullanici=username,sifre=password,adres=adres,email=email,number=tel)
    return render_template('ogrenci_ekle.html', navbar=session["navbar"])

if __name__ == '__main__':
    app.run(debug=True)
