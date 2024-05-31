from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'admin1234'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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
    admin = db.Column(db.Integer, nullable=False, default=0)  # Default to 0 for non-admin users

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})  # Fixed typo
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})  # Fixed typo
    
    submit = SubmitField("Login")

@app.route('/', methods=["GET"])
def getIndex():
    return render_template('index.html', Title="Home"), 200  # Changed to 200

@app.route('/who-we-are', methods=["GET"])
def getManagementAndTeam():
    return render_template('whoWeAre.html', Title="Who We Are"), 200  # Changed to 200

@app.route('/partners', methods=["GET"])
def getPartners():
    return render_template('partners.html', Title="Partners"), 200  # Changed to 200

@app.route('/login', methods=["GET", "POST"])
def getLogin():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/admin_dashboard')

    return render_template('login.html', form=form), 200  # Changed to 200

@app.route('/admin_dashboard', methods=["GET", "POST"])
@login_required
def admin_dashboard():
    if current_user.admin == 1:
        return render_template('admin.html', user=current_user), 200  # Changed to 200
    else:
        return render_template('/includes/404.html'), 404

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/register', methods=["GET", "POST"])
def getRegister():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, admin=0)  # Default admin to 0
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html', form=form), 200  # Changed to 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
