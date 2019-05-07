from flask import Flask, render_template, redirect, url_for
from form import LoginForm

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


@app.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('profile'), code=302)
    return render_template('login.html', form=form)

@app.route('/profile')
def profile():
    return render_template('ogrenci.html', navbar=stdnav)

@app.route('/randevutalep')
def randevutalep():
        return render_template('randevutalep.html', navbar=stdnav)



if __name__ == '__main__':
    app.run(debug=True)
