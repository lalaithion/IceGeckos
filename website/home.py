from flask import render_template, request
from website import website

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

users = {'firefly': '1000hugs', 'rabbit':'wascilly'}

class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = StringField('Password', validators=[DataRequired()])
    
    def check_login(self):
        print("Checked")
        return users.get(self.uname.data, None) == self.pword.data
            

@website.route('/', methods=['GET', 'POST'])
@website.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("validated")
        if form.check_login():
            return render_template('account.html', username=form.uname.data)
        else:
            return render_template('login.html', form=form, error='<p class="error">Error logging in</p>')
    return render_template('login.html', form=form, error='')
