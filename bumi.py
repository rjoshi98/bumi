from sys import argv, exit, stderr
from flask import Flask, request, make_response, redirect, url_for, jsonify, abort, redirect, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from database import Database
from auth import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = 'podesta1'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://xrauczsvsmptxh:c156cb8cf731f4ba4c0658a9c66822604ad0ac71a75ab4fbb7160f203cb3e4a7@ec2-3-209-176-42.compute-1.amazonaws.com/d7f4b8erkrgp2b"

Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(19))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    location = db.Column(db.String(35))
    specialty = db.Column(db.String(35))
    education = db.Column(db.String(35))
    experience = db.Column(db.String(35))
    hospital = db.Column(db.String(35))
    procedures = db.Column(db.String(500))

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.id == 1
        else:
            return 0
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.id == 1
        else:
            return 0
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('home', next=request.url))

admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Doctors, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    html = render_template('index.html')
    response = make_response(html)

    return response 

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))

    html = render_template('login.html', form=form)
    response = make_response(html)

    return response

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    html = render_template('register.html', form=form)
    response = make_response(html)

    return response

@app.route('/about', methods=['GET'])
def about():
    html = render_template('about.html')
    response = make_response(html)

    return response

@app.route('/partnerships', methods=['GET'])
def partnerships():
    html = render_template('partnerships.html')
    response = make_response(html)

    return response

@app.route('/success', methods=['GET'])
def success():
    html = render_template('success.html')
    response = make_response(html)

    return response

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/doctors', methods=['GET', 'POST'])
@login_required
def doctors():
    finder_db = Database()

    docs = finder_db.get_doctors()

    html = render_template('doctors.html', data=docs)

    if request.method == 'POST':
        saved_docs = request.form.getlist('doctors')

        if len(saved_docs) > 0:
            finder_db.add_saved(current_user.email, saved_docs)
 
    response = make_response(html)

    return response

@app.route('/yourDoctors', methods=['GET', 'POST'])
@login_required
def savedDoctors():
    docs_info = []

    finder_db = Database()

    docs = finder_db.get_saved(current_user.email)

    if docs:
        for doc in docs:
            docs_info.append(finder_db.get_doctors1(doc))
    
    if request.method == 'POST':
        doc = request.form.get('doctors')
        print(doc)
        finder_db.delete_saved(current_user.email, doc)
        return redirect(url_for('savedDoctors'))

    return make_response(render_template('yourDoctors.html', data=docs_info))

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)

    if argv[1].isdigit() == False:
        print('Port must be an integer', file=stderr)
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)