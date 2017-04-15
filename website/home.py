import json
import hashlib
import base64

from flask import render_template, request, redirect, url_for
from website import website

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

from meraki import mac_exists

error = ''

def phash(s):
    sha = hashlib.sha256()
    sha.update(s.encode())
    return str(base64.b64encode(sha.digest()))

class User:
    def __init__(self, uname, pword, mac):
        self.username = uname
        self.password = phash(pword)
        self.macaddr = mac
    
    def __repr__(self):
        return 'User({username}, {password}, {macaddr})'.format(**vars(self))
    
    def try_login(self, password):
        if mac_exists(self.macaddr):
            return self.password == phash(password)
        else:
            global error
            error = "mac"
            return False



db = json.load(open('users.json'))
db = {k: User(v['uname'], v['pword'], v['mac']) for k, v in db.items()}

def save():
    data = {k: {'uname': v.username, 'pword': v.password, 'mac': v.macaddr} for k, v in db.items()}
    json.dump(data, open('users.json', 'w'), indent=2)



class RegisterForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
    macad = StringField('MAC Address', validators=[DataRequired()])
    
    def add_user(self):
        user = User(self.uname.data, self.pword.data, self.macad.data)
        db[self.uname.data] = user
        save()
        return True



class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])

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
            global error
            if error == 'mac':
                error = ''
                return render_template('login.html', form=form, error='You must log in from within the network')
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
