from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, HiddenField, TextAreaField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, Length, ValidationError, URL, DataRequired
from flask_bcrypt import Bcrypt
from flask_wtf.file import FileAllowed
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/files/uploaded_pictures'
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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class UploadPartnerForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=40)], render_kw={"class": "input-primary", "placeholder": "Partner Name"})
    website = StringField("Website", validators=[InputRequired(), URL(), Length(max=40)], render_kw={"class": "input-primary", "placeholder": "Partner Website"})
    logo = FileField("Logo", validators=[InputRequired()], render_kw={"class": "file-input"})
    partner_id = HiddenField('Partner ID')
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

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()], render_kw={"class": "input-primary"})
    summary = TextAreaField('Summary', validators=[DataRequired()], render_kw={"class": "textarea-primary"})
    picture = FileField('Picture', render_kw={"class": "file-input"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"class": "textarea-primary"})
    submit = SubmitField('Upload Event', render_kw={"class": "btn", "style": "background-color: #f5494c;"})

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
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form, Title="Admin Login")

@app.route('/admin/admin_dashboard', methods=["GET", "POST"])
def admin_dashboard():
    try:
        if current_user.admin == 1:
            return render_template('admin/admin.html', user=current_user, Title="Admin Dashboard")
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
        flash('User registered successfully!', 'success')
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
                return redirect(url_for('admin_dashboard'))
            return render_template('admin/upload-partner.html', form=form, Title="Upload Partner", partners=partners)
        return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404

@app.route('/partners', methods=["GET"])
def getPartners():
    partners = Partners.query.all()
    return render_template('partners.html', Title="Partners", partners=partners)

@app.route('/admin/update-partner/<int:partner_id>', methods=['GET', 'PUT'])
def update_partner(partner_id):
    partner = Partners.query.get_or_404(partner_id)
    form = UploadPartnerForm()

    try:
        if current_user.admin == 1:
            if request.method == 'PUT':
                form = UploadPartnerForm(meta={'csrf': False})  # Disable CSRF check for PUT
                if form.validate():
                    logo_file = form.logo.data
                    if logo_file:
                        logo_filename = logo_file.filename
                        logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
                        partner.logo = logo_filename
                    
                    partner.name = form.name.data
                    partner.website = form.website.data
                    db.session.commit()
                    return jsonify({'message': 'Partner updated successfully!'})
                return jsonify({'error': 'Invalid form data'}), 400

            form.name.data = partner.name
            form.website.data = partner.website
            form.partner_id.data = str(partner.id)  # Populate hidden field with partner id
            return render_template('admin/update-partner.html', form=form, partner=partner)
        else:
            return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404


@app.route('/admin/upload-partners/del/<int:partner_id>', methods=['DELETE'])
def delete_partner(partner_id):
    partner = Partners.query.get_or_404(partner_id)
    db.session.delete(partner)
    db.session.commit()
    return '', 204

@app.route("/events", methods=["GET"])
def getEvents():
    events = Event.query.all()
    return render_template("events.html", Title="Events", events=events)

@app.route('/admin/upload-event', methods=['GET', 'POST'])
def upload_event():
    form = EventForm()

    try:
        if current_user.admin == 1:
            if form.validate_on_submit():
                picture = form.picture.data
                if picture:
                    picture_filename = secure_filename(picture.filename)
                    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
                    picture.save(picture_path)

                    new_event = Event(
                        name=form.name.data,
                        summary=form.summary.data,
                        picture=picture_filename,
                        description=form.description.data
                    )
                    db.session.add(new_event)
                    db.session.commit()
                    flash('Event uploaded successfully!', 'success')
                    return redirect(url_for('upload_event'))

            events = Event.query.all()
            return render_template('admin/upload-event.html', form=form, events=events), 200
        else:
            return render_template('includes/404.html') , 404
    except:
        return render_template('includes/404.html') , 404

@app.route('/admin/update-event/<int:event_id>', methods=['GET', 'POST', 'PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    try:
        if current_user.admin == 1:
            if request.method in ['POST', 'PUT']:
                try:
                    if form.validate_on_submit():
                        event.name = form.name.data
                        event.summary = form.summary.data
                        event.description = form.description.data

                        if form.picture.data:
                            picture = form.picture.data
                            picture_filename = secure_filename(picture.filename)
                            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
                            picture.save(picture_path)
                            event.picture = picture_filename

                        db.session.commit()
                        return jsonify({'message': 'Event updated successfully!'}), 200
                    else:
                        return jsonify({'message': 'Form validation failed', 'errors': form.errors}), 400
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'message': 'Error updating event', 'error': str(e)}), 500

            return render_template('admin/update-event.html', form=form, event=event), 200
        else:
            return render_template('includes/404.html'), 404
    except:
        return render_template('includes/404.html'), 404

@app.route('/admin/delete-event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting event', 'error': str(e)}), 500

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text}: {error}", 'error')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
