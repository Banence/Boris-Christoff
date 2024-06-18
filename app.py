from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, HiddenField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, Length, ValidationError, URL
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/files/uploaded_logos'
app.config['SECRET_KEY'] = 'admin1234'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    website = db.Column(db.String(40), nullable=False, unique=True)
    logo = db.Column(db.String(120), nullable=False)

class UploadPartnerForm(FlaskForm):
    partner_id = HiddenField()
    logo = FileField("Logo", validators=[InputRequired()], render_kw={"class": "file-input"})
    name = StringField("Name", validators=[InputRequired(), Length(max=40)], render_kw={"class": "input-primary", "placeholder": "Partner Name"})
    website = StringField("Website", validators=[InputRequired(), URL(), Length(max=40)], render_kw={"class": "input-primary", "placeholder": "Partner Website"})
    submit = SubmitField("Add Partner", render_kw={"class": "btn"})

    def validate_name(self, name):
        existing_partner = Partners.query.filter_by(name=name.data).first()
        if existing_partner and existing_partner.id != int(self.partner_id.data):
            raise ValidationError("That partner name already exists. Please choose a different one.")
        
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username", "class": "input-primary"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "input-primary"})
    submit = SubmitField("Register", render_kw={"class": "btn"})

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username", "class": "input-primary"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "input-primary"})
    submit = SubmitField("Login", render_kw={"class": "btn"})

@app.route('/', methods=["GET"])
def getIndex():
    return render_template('index.html', Title="Home")

@app.route('/who-we-are', methods=["GET"])
def getManagementAndTeam():
    return render_template('whoWeAre.html', Title="Who We Are")

@app.route('/admin/login', methods=["GET", "POST"])
def getLogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html', form=form, Title="Admin Login")

@app.route('/admin/admin_dashboard', methods=["GET", "POST"])
def admin_dashboard():
    try:
        if current_user.admin == 1:
            return render_template('admin/admin.html', user=current_user, Title="Admin Dashboard")
        else:
            return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404

@app.route('/admin/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('getLogin'))

@app.route('/admin/register', methods=["GET", "POST"])
def getRegister():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, admin=0) 
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('getLogin'))
    return render_template('admin/register.html', form=form, Title="Admin Register")

@app.route('/admin/upload-partner', methods=["GET", "POST"])
def get_admin_partner_upload():
    form = UploadPartnerForm()
    partners = Partners.query.all()
    try:
        if current_user.admin == 1:
            if form.validate_on_submit():
                logo = form.logo.data
                logo_filename = secure_filename(logo.filename)
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                logo.save(logo_path)

                new_partner = Partners(
                    name=form.name.data,
                    website=form.website.data,
                    logo=logo_filename
                )
                db.session.add(new_partner)
                db.session.commit()
                flash('Partner added successfully!', 'success')
                return redirect('admin_dashboard')
            return render_template('admin/upload-partner.html', form=form, Title="Upload Partner", partners=partners), 200
        else:
            return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404
    
@app.route('/partners', methods=["GET"])
def getPartners():
    partners = Partners.query.all()
    return render_template('partners.html', Title="Partners", partners=partners)

@app.route('/admin/upload-partners/del/<int:id>', methods=["DELETE"])
def deletePartner(id):
    partner_id = id
    try:
        if current_user.admin == 1:
            partner = Partners.query.get(partner_id)
            db.session.delete(partner)
            db.session.commit()
            return '', 204 
        else:
            return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404

    
@app.route('/admin/update-partner/<int:partner_id>', methods=["GET", "PUT", "PATCH"])
def update_partner(partner_id):
    partner = Partners.query.get_or_404(partner_id)
    form = UploadPartnerForm(partner_id=partner.id)
    try:
        if current_user.admin == 1:
            if request.method in ["PUT", "PATCH"]:
                if form.validate_on_submit():
                    partner.name = form.name.data
                    partner.website = form.website.data

                    if form.logo.data:
                        logo = form.logo.data
                        logo_filename = secure_filename(logo.filename)
                        logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                        logo.save(logo_path)
                        partner.logo = logo_filename

                    db.session.commit()
                    return '', 204  

            elif request.method == 'GET':
                form.name.data = partner.name
                form.website.data = partner.website

            return render_template('admin/update-partner.html', form=form, Title="Update Partner", partner=partner)
        else:
            return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
