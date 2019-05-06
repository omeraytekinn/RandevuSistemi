from flask import Flask, render_template, url_for, flash, redirect
from form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']  = "123456"

usernav = [
    {
        'value':'Profil',
        'link':'profile'
    },
    {
        'value':'Randevu İşlemleri',
        'link':'#',
        'alt':True
    },
    {
        'value':'Randevu Talep Et',
        'link':'randvutalep',
        'top':True
    },
    {
        'value':'Randevularım',
        'link':'randvular',
        'top':True,
        'end':True
    }
]

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('ogrenci'))
    return render_template('login.html', title='Login', form=form, body='text-center')

@app.route('/profile', methods=['GET', 'POST'])
def ogrenci():
    return render_template('ogrenci.html', title='Öğrenci Profili', navbar=usernav, auth='Öğrenci', type='Profil')


if __name__ == '__main__':
    app.run(debug=True)
