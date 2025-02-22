from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, HiddenField, TextAreaField, BooleanField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, Length, ValidationError, URL, DataRequired, Email
from flask_bcrypt import Bcrypt
from flask_wtf.file import FileAllowed
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
from random import shuffle
from flask_mail import Mail, Message
import pymysql
from flask_migrate import Migrate
from flask import session
from email_validator import validate_email, EmailNotValidError
pymysql.install_as_MySQLdb()

def init_db():
    try:
        # Connect to MySQL server without selecting a database
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'ScionxB2007')
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'borischristoff_db')} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
        connection.close()
        
    except Exception as e:
        print(f"Error initializing database: {e}")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_directories():
    directories = ['news', 'partners', 'events']
    for dir_name in directories:
        dir_path = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ScionxB2007@localhost:3306/borischristoff_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_timeout': 20,
    'pool_size': 10,
    'max_overflow': 5
}
app.config['UPLOAD_FOLDER'] = 'static/files/uploaded_pictures'
app.config['SECRET_KEY'] = 'admin1234'  # You should use a secure secret key
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your actual email
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Replace with your actual app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_MAX_EMAILS'] = 5
app.config['MAIL_ASCII_ATTACHMENTS'] = False
create_upload_directories()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "getLogin"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20, collation='utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100, collation='utf8mb4_unicode_ci'), nullable=False)
    website = db.Column(db.String(200, collation='utf8mb4_unicode_ci'), nullable=False)
    logo = db.Column(db.String(200, collation='utf8mb4_unicode_ci'))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100, collation='utf8mb4_unicode_ci'), nullable=False)
    summary = db.Column(db.String(200, collation='utf8mb4_unicode_ci'))
    description = db.Column(db.Text(collation='utf8mb4_unicode_ci'))
    picture = db.Column(db.String(100, collation='utf8mb4_unicode_ci'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.name}>'

class UploadPartnerForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=100)], 
                      render_kw={"class": "input-primary", "placeholder": "Partner Name"})
    website = StringField("Website", validators=[InputRequired(), URL()], 
                         render_kw={"class": "input-primary", "placeholder": "https://example.com"})
    logo = FileField("Logo", validators=[InputRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'svg'], 'Images and SVG only!')], 
                    render_kw={"class": "file-input"})
    partner_id = HiddenField()
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
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])], render_kw={"class": "file-input"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"class": "textarea-primary"})
    date = StringField('Date', validators=[DataRequired()], render_kw={"class": "input-primary", "type": "datetime-local"})
    submit = SubmitField('Upload Event', render_kw={"class": "btn", "style": "background-color: #f5494c;"})

class ContactForm(FlaskForm):
    first_name = StringField('Първо Име', 
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"class": "input-primary", "placeholder": "Въведете първо име"}
    )
    last_name = StringField('Фамилно Име', 
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"class": "input-primary", "placeholder": "Въведете фамилно име"}
    )
    email = StringField('Email', 
        validators=[
            DataRequired(),
            Email(message='Моля, въведете валиден email адрес')
        ],
        render_kw={"class": "input-primary", "placeholder": "Въведете електронна поща"}
    )
    message = TextAreaField('Съобщение', 
        validators=[DataRequired(), Length(min=10, max=1000)],
        render_kw={"class": "textarea-primary", "placeholder": "Въведете съобщение..."}
    )
    submit = SubmitField('Изпрати съобщение', 
        render_kw={"class": "btn"}
    )

@app.route('/')
def index():
    
    return render_template('index.html', 
                         Title='Начало - Фондация Бори Христов')

@app.route('/who-we-are', methods=["GET"])
def getManagementAndTeam():
    return render_template('whoWeAre.html', Title="Кои сме ние?")

@app.route('/admin/login', methods=['GET', 'POST'])
def getLogin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.admin == 1:
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            else:
                flash('You do not have admin privileges', 'error')
        else:
            flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('getLogin'))

@app.route('/admin/register', methods=['GET', 'POST'])
def getRegister():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        is_first_user = User.query.count() == 0
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            admin=1 if is_first_user else 0
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('getLogin'))
    return render_template('admin/register.html', form=form)

@app.route('/admin/upload-partner', methods=['GET', 'POST'])
@login_required
def upload_partner():
    if not current_user.admin:
        abort(403)

    form = UploadPartnerForm()
    
    if form.validate_on_submit():
        try:
            # Handle logo upload
            logo_path = None
            if form.logo.data:
                file = form.logo.data
                if file and allowed_file(file.filename):
                    logo_filename = secure_filename(file.filename)
                    # Create partners directory if it doesn't exist
                    partners_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'partners')
                    if not os.path.exists(partners_dir):
                        os.makedirs(partners_dir)
                    
                    # Save file
                    file_path = os.path.join(partners_dir, logo_filename)
                    file.save(file_path)
                    logo_path = f'/static/files/uploaded_pictures/partners/{logo_filename}'

            # Create new partner
            new_partner = Partners(
                name=form.name.data,
                website=form.website.data,
                logo=logo_path
            )
            
            db.session.add(new_partner)
            db.session.commit()
            flash('Partner added successfully!', 'success')
            return redirect(url_for('admin_partners'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding partner: {str(e)}', 'error')
    
    partners = Partners.query.all()
    return render_template('admin/upload-partner.html', form=form, partners=partners)

@app.route('/partners', methods=["GET"])
def getPartners():
    partners = Partners.query.all()
    return render_template('partners.html', Title="Партньори", partners=partners)

@app.route('/admin/update-partner/<int:partner_id>', methods=['GET', 'PATCH'])
@login_required
def update_partner(partner_id):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized'}), 403

    partner = Partners.query.get_or_404(partner_id)
    form = UploadPartnerForm()

    if request.method == 'PATCH':
        try:
            data = request.form
            
            # Validate CSRF token
            if not form.validate_csrf_token(form.csrf_token, data.get('csrf_token')):
                return jsonify({'error': 'Invalid CSRF token'}), 400

            partner.name = data.get('name', partner.name)
            partner.website = data.get('website', partner.website)

            if 'logo' in request.files:
                logo_path = save_uploaded_file(request.files['logo'], 'partners')
                if logo_path:
                    partner.logo = logo_path

            db.session.commit()
            return jsonify({'message': 'Partner updated successfully!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # GET request
    form.name.data = partner.name
    form.website.data = partner.website
    form.partner_id.data = partner.id
    return render_template('admin/update-partner.html', form=form, partner=partner)

@app.route('/admin/partners/delete/<int:partner_id>', methods=['DELETE'])
@login_required
def delete_partner(partner_id):
    if not current_user.admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    try:
        partner = Partners.query.get_or_404(partner_id)
        
        # Delete associated logo file if it exists
        if partner.logo and partner.logo.startswith('/static/files/uploaded_pictures/partners/'):
            logo_path = os.path.join(
                app.root_path, 
                'static', 
                'files', 
                'uploaded_pictures',
                'partners',
                os.path.basename(partner.logo)
            )
            if os.path.exists(logo_path):
                os.remove(logo_path)
        
        db.session.delete(partner)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Partner deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/events", methods=["GET"])
def getEvents():
    events = Event.query.all()
    # Clean up the picture paths
    for event in events:
        if event.picture:
            # Remove any leading slashes and ensure correct path
            event.picture = event.picture.lstrip('/')
    return render_template("events.html", Title="Събития", events=events)

@app.route('/admin/upload-event', methods=['GET', 'POST'])
@login_required
def upload_event():
    if not current_user.admin:
        abort(403)

    form = EventForm()
    
    if form.validate_on_submit():
        try:
            # Handle picture upload
            picture_filename = None
            if form.picture.data:
                file = form.picture.data
                if file and allowed_file(file.filename):
                    picture_filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'events', picture_filename)
                    file.save(file_path)

            # Create new event with correct path format
            new_event = Event(
                name=form.name.data,
                summary=form.summary.data,
                description=form.description.data,
                date=datetime.strptime(form.date.data, '%Y-%m-%dT%H:%M'),
                picture=f'static/files/uploaded_pictures/events/{picture_filename}' if picture_filename else None  # Removed leading slash
            )
            
            db.session.add(new_event)
            db.session.commit()
            flash('Event uploaded successfully!', 'success')
            return redirect(url_for('admin_events'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading event: {str(e)}', 'error')
    
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('admin/upload-event.html', form=form, events=events)

@app.route('/admin/update-event/<int:event_id>', methods=['GET', 'POST', 'PATCH'])
@login_required
def update_event(event_id):
    if not current_user.admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('getLogin'))

    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    if request.method in ['POST', 'PATCH'] and form.validate_on_submit():
        try:
            event.name = form.name.data
            event.summary = form.summary.data
            event.description = form.description.data
            event.date = datetime.strptime(form.date.data, '%Y-%m-%dT%H:%M')

            if form.picture.data:
                # Delete old picture if it exists
                if event.picture and event.picture.startswith('/static/files/uploaded_pictures/events/'):
                    old_picture_path = os.path.join(
                        app.root_path,
                        'static',
                        'files',
                        'uploaded_pictures',
                        'events',
                        os.path.basename(event.picture)
                    )
                    if os.path.exists(old_picture_path):
                        os.remove(old_picture_path)

                # Save new picture
                picture_path = save_uploaded_file(form.picture.data, 'events')
                if picture_path:
                    event.picture = picture_path

            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin_events'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'error')

    # Pre-fill form with existing data
    if request.method == 'GET':
        form.name.data = event.name
        form.summary.data = event.summary
        form.description.data = event.description
        if event.date:
            form.date.data = event.date.strftime('%Y-%m-%dT%H:%M')

    return render_template('admin/update-event.html', form=form, event=event)

@app.route('/admin/events/delete/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    if not current_user.admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    try:
        event = Event.query.get_or_404(event_id)
        
        # Delete associated picture if it exists
        if event.picture and event.picture.startswith('/static/files/uploaded_pictures/events/'):
            picture_path = os.path.join(
                app.root_path,
                'static',
                'files',
                'uploaded_pictures',
                'events',
                os.path.basename(event.picture)
            )
            if os.path.exists(picture_path):
                os.remove(picture_path)
        
        db.session.delete(event)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Event deleted successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text}: {error}", 'error')

@app.route('/admin/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_authenticated or current_user.admin != 1:
        abort(403)
    
    events_count = Event.query.count()
    partners_count = Partners.query.count()
    
    return render_template('admin/dashboard.html',
                         events_count=events_count,
                         partners_count=partners_count,
                         user=current_user,
                         Title="Admin Dashboard")

@app.route('/admin/events')
@login_required
def admin_events():
    if not current_user.admin:
        abort(403)
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template('admin/events.html', events=events)

@app.route('/admin/partners')
@login_required
def admin_partners():
    if not current_user.admin:
        abort(403)
    partners = Partners.query.all()
    return render_template('admin/partners.html', partners=partners)

@app.route('/admin/partners/add', methods=['GET', 'POST'])
@login_required
def add_partner():
    if not current_user.admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('getLogin'))

    form = UploadPartnerForm()
    if form.validate_on_submit():
        try:
            logo_path = None
            if form.logo.data:
                logo_path = save_uploaded_file(form.logo.data, 'partners')
            
            partner = Partners(
                name=form.name.data,
                website=form.website.data,
                logo=logo_path
            )
            
            db.session.add(partner)
            db.session.commit()
            flash('Partner added successfully!', 'success')
            return redirect(url_for('admin_partners'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding partner: {str(e)}', 'error')
    
    return render_template('admin/add_partner.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': False, 'message': 'Page not found'}), 404
    return render_template('includes/404.html', Title='Page Not Found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
    return render_template('includes/500.html', Title='Server Error'), 500

@app.errorhandler(403)
def forbidden_error(error):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
    flash('You do not have permission to access this page', 'error')
    return redirect(url_for('getLogin'))

@app.template_filter('shuffle')
def shuffle_filter(seq):
    try:
        result = list(seq)
        shuffle(result)
        return result
    except:
        return seq

def save_uploaded_file(file, subfolder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        subfolder_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        
        # Create directory if it doesn't exist
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            
        file_path = os.path.join(subfolder_path, filename)
        try:
            file.save(file_path)
            return f'/static/files/uploaded_pictures/{subfolder}/{filename}'
        except Exception as e:
            app.logger.error(f"Error saving file: {str(e)}")
            return None
    return None

@app.route('/admin/partners/edit/<int:partner_id>', methods=['GET', 'POST'])
@login_required
def edit_partner(partner_id):
    if not current_user.admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('getLogin'))

    partner = Partners.query.get_or_404(partner_id)
    form = UploadPartnerForm()

    if form.validate_on_submit():
        try:
            partner.name = form.name.data
            partner.website = form.website.data

            if form.logo.data:
                # Delete old logo if it exists
                if partner.logo and partner.logo.startswith('/static/files/uploaded_pictures/partners/'):
                    old_logo_path = os.path.join(
                        app.root_path, 
                        'static', 
                        'files', 
                        'uploaded_pictures',
                        'partners',
                        os.path.basename(partner.logo)
                    )
                    if os.path.exists(old_logo_path):
                        os.remove(old_logo_path)

                # Save new logo
                logo_path = save_uploaded_file(form.logo.data, 'partners')
                if logo_path:
                    partner.logo = logo_path

            db.session.commit()
            flash('Partner updated successfully!', 'success')
            return redirect(url_for('admin_partners'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating partner: {str(e)}', 'error')

    # Pre-fill form with existing data
    form.name.data = partner.name
    form.website.data = partner.website
    form.partner_id.data = partner.id
    
    return render_template('admin/edit_partner.html', form=form, partner=partner)


@app.route('/boris-christoff')
def boris_christoff():
    return render_template('boris-christoff.html', Title='Борис Христов')

@app.route('/projects/sport-against-aggression')
def sport_against_aggression():
    return render_template('projects/sport-against-aggression.html', Title='Спорт срещу агресия')

@app.route('/projects/together')
def together():
    return render_template('projects/together.html', Title='Заедно - спорт и изкуство')

def can_send_email():
    """Check if enough time has passed since the last email was sent"""
    last_email_time = session.get('last_email_time')
    if last_email_time:
        last_email_time = datetime.fromisoformat(last_email_time)
        time_passed = datetime.now() - last_email_time
        # Return remaining wait time in minutes, or None if can send
        if time_passed < timedelta(minutes=5):
            return 5 - int(time_passed.total_seconds() / 60)
    return None

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            # Check if user can send email
            wait_time = can_send_email()
            if wait_time:
                flash(f'Моля изчакайте {wait_time} минути преди да изпратите ново съобщение.', 'warning')
                return render_template('contact.html', Title='Свържете се с нас', form=form)

            # Prepare email message
            msg = Message(
                subject='New Contact Form Submission',
                recipients=[app.config['MAIL_USERNAME']],
                body=f"""
                New contact form submission:
                
                From: {form.first_name.data} {form.last_name.data}
                Email: {form.email.data}
                Message:
                {form.message.data}
                
                Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """,
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            
            # Send email
            mail.send(msg)
            
            # Store the time of successful email sending
            session['last_email_time'] = datetime.now().isoformat()
            
            # Clear form data after successful submission
            form.first_name.data = ''
            form.last_name.data = ''
            form.email.data = ''
            form.message.data = ''
            
            flash('Вашето съобщение беше изпратено успешно! Благодарим Ви за обратната връзка.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            app.logger.error(f"Email sending error: {str(e)}")
            flash('Възникна грешка при изпращането на съобщението. Моля, опитайте отново по-късно или се свържете с нас по друг начин.', 'error')
            return render_template('contact.html', Title='Свържете се с нас', form=form)
            
    return render_template('contact.html', Title='Свържете се с нас', form=form)

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Create database if it doesn't exist
    app.run(debug=True)
