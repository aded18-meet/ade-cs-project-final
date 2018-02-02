from flask import Flask, flash,redirect, render_template, request, session, abort
import os 
from flask_sqlalchemy import SQLAlchemy 
#from flask.ext.session import Session

##  
from sqlalchemy import create_engine
from database_initialize import User
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import session as login_session
##


app = Flask(__name__)
# app.debug=True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
app.secret_key = 'super secret key'


engine = create_engine('sqlite:///database.db')

Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

logged_in = False

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/math')
def math():
	return render_template("math.html")

@app.route('/physics')
def physics():
	return render_template("physics.html")

@app.route('/english')
def english():
	return render_template("english.html")

@app.route('/aboutus')
def aboutus():
	return render_template("aboutus.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user = User()
		user.name = request.form['username']
		user.password = request.form['password']
		session.add(user)
		session.commit()
		return render_template('signup.html' , user=user)
	else:
		return render_template("signup.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('home.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = session.query(User).filter_by(name=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return render_template("signup.html")
    login_session['id'] = registered_user.id
    login_session['username'] = registered_user.name
    login_session['password'] = registered_user.password
    logged_in = True
    flash('Logged in successfully')
    return render_template("home.html", logged_in=logged_in)


if __name__== '__main__':
	# app.secret_key = 'super secret key'
	# app.config['SESSION_TYPE'] 	= 'filesystem'
	app.run(debug=True)

