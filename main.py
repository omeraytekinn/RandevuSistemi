from flask import Flask, render_template, redirect, url_for ,session
from functools import wraps
from form import LoginForm
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
        'link':'randvular',
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
            return redirect(url_for('profile'), code=302)
    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('ogrenci.html', navbar=stdnav)

@app.route('/randevutalep')
@login_required
def randevutalep():
        return render_template('randevutalep.html', navbar=stdnav)

@app.route('/logout')
def logout():
        session.clear()
        return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
    
