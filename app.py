from flask import Flask, flash,redirect, render_template, request, session, abort
import os 
from flask_sqlalchemy import SQLAlchemy 
#from flask.ext.session import Session 




app = Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
app.secret_key = 'super secret key'

class User(db.Model):
      id = db.Column( db.Integer,primary_key=True, autoincrement=True)
      name = db.Column(db.String(100), nullable=False)
      password = db.Column(db.String(100), nullable=False)

      def __repr__(self):
        return '<User %r>' % self.name

db.create_all()

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
		db.session.add(user)
		db.session.commit()
		print(User.query.all())
		return render_template('signup.html' , user=user)
	else:
		return render_template("signup.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('home.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(name=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return render_template("signup.html")
    session['id'] = registered_user.id
    session['username'] = registered_user.name
    session['password'] = registered_user.password
    session['logged_in'] = True
    flash('Logged in successfully')
    return render_template("home.html", logged_in=session['logged_in'])


if __name__== '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] 	= 'filesystem'
	app.run(debug=True)

