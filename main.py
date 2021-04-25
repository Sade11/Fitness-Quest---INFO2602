from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, g, session
from flask_login import LoginManager, login_user
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
from models import db, Exercise, User,CreateRoutines, Routine
from werkzeug.utils import redirect
from form import SignUpForm, LoginForm
from flask_jwt import JWT


#Begin Flask login function
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
#End Flask login function


# begin boilerplate code

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  login_manager.init_app(app)
  db.init_app(app)
  CORS(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
#end boilerplate code#


# JWT set up here
def authenticate(uname, password):
    user = User.query.filter_by(username=uname).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
# JWT set up end


@app.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/exercises')
def show_exercises():
  exercises= Exercise.query.all()
  return render_template('exercises.html', exercises=exercises)

@app.route('/exercises/<id>')
def show_exercise(id):
  exercise= Exercise.query.get(id)
  return render_template('exercise.html', exercise=exercise)

@app.route('/data', methods=['GET'])
def exercises_data():
    logs = Exercise.query.all()
    logs = [ log.toDict() for log in logs]
    return jsonify(logs)

@app.route('/data/<id>', methods=['GET'])
def exercise_data(id):
    logs = Exercise.query.get(id)
    logs = logs.toDict()
    return jsonify(logs)  

@app.route('/', methods=['POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
      session.pop('users', None)
      if form.validate_on_submit():
        session['users'] = request.form["username"]
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):  # check credentials
            flash('Logged in successfully.')  # send message to next page
            login_user(user)  # login the user
            return redirect(url_for('about'))  # redirect to main page if login successful
    flash('Invalid credentials')
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET'])
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@app.route('/signup', methods=['POST'])
def signupAction():
    form = SignUpForm()
    if request.method == "POST":
      session.pop('users', None)
      if form.validate_on_submit():
        session['users'] = request.form["username"]
        data = request.form  # get data from form submission
        user = User(username=data['username'], email=data['email'])  # create user object
        user.set_password(data['password'])  # set password
        db.session.add(user)  # save new user
        db.session.commit()
        flash('Account Created!')  # send message
        return redirect(url_for('login'))  # redirect to login page
    flash('Error invalid input!')
    return redirect(url_for('signup'))

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/about')
# def about():
#   if g.users:
#     return render_template('about.html', users=session['users'])
#   return redirect(url_for('index'))

@app.before_request
def before_request():
    g.users = None
    if 'users' in session:
        g.users = session['users']

@app.route("/create_routine")
def create_routine():
  exercises= Exercise.query.all()
  return render_template('create_routine.html', exercises=exercises)

@app.route("/routines")
def show_create_routine():
    routines=CreateRoutines.query.all()
    return render_template('view_routine.html', routines=routines)

@app.route("/createroutines", methods=['POST'])
def my_form():
  data = request.form
  createroutine= CreateRoutines(routine_name=data['routine_name'], exercise_name=data['exercise_name'], description=data['description'], day=data['day'])
  db.session.add(createroutine)
  db.session.commit()
  return redirect(url_for('create_routine'))

@app.route("/createroutines", methods=['GET'])
def get_createroutines():
  createroutines = CreateRoutines.query.all()
  createroutines = [createroutine.toDict() for createroutine in createroutines]
  return jsonify(createroutines)

@app.route('/deleteLog/<id>', methods=['GET'])
def delete_action(id):
  log = CreateRoutines.query.get(id);
  db.session.delete(log)
  db.session.commit()
  return redirect(url_for('create_routine'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)