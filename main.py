from flask import Flask, render_template, url_for, flash, redirect
from form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']  = "123456"


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
