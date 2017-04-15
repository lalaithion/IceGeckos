from flask import render_template, request, redirect, url_for
from website import website

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

db = {}



class User:
    def __init__(self, uname, pword, mac):
        self.username = uname
        self.password = pword
        self.macaddrs = mac
    
    def __repr__(self):
        return 'User({username}, {password}, {macaddrs})'.format(**vars(self))
    
    def try_login(self, password):
        return self.password == password


class RegisterForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = StringField('Password', validators=[DataRequired()])
    macad = StringField('MAC Address', validators=[DataRequired()])
    
    def add_user(self):
        user = User(self.uname.data, self.pword.data, self.macad.data)
        db[self.uname.data] = user
        return True



class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = StringField('Password', validators=[DataRequired()])

    def check_login(self):
        try:
            return db[self.uname.data].try_login(self.pword.data)
        except KeyError:
            return False



@website.route('/', methods=['GET', 'POST'])
@website.route('/index', methods=['GET', 'POST'])
@website.route('/login', methods=['GET', 'POST'])
def index():
    print(db)
    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        if form.check_login():
            return render_template('account.html', username=form.uname.data)
        else:
            return render_template('login.html', form=form, error='Error logging in')
            
    return render_template('login.html', form=form, error='')



@website.route('/register', methods=['GET', 'POST'])
def register():
    print(db)
    form = RegisterForm(request.form)
    
    if form.validate_on_submit():
        if form.uname.data in db:
            return render_template('register.html', form=form, error='Username already taken')
        form.add_user()
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form, error='')
