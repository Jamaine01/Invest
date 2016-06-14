from app import app
from flask import Flask, render_template, request, abort
import sqlite3

conn = sqlite3.connect('invest.db',check_same_thread=False)
db = conn.cursor()

def create_db():
	db.execute('''
		CREATE TABLE user (
		user_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		fname TEXT,
		lname TEXT,
		email TEXT,
		pwd TEXT
		)
		''')


def create_(fname, lname, email, pwd):
	db.execute('''
		INSERT INTO user(fname, lname, email, pwd) VALUES(?, ?, ?, ?)
		''', (fname, lname, email, pwd))
	conn.commit()


def check_(login_email):
	db.execute('''
		SELECT pwd AND fname FROM user WHERE email=login_email
		''', (login_email))


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/login', methods = ['POST'])
def create_user():
	if request.form['fname'] and request.form['lname'] and request.form['email'] and request.form['pwd'] != "" and " ":
		#create_db()
		firstname = request.form['fname']
		lastname = request.form['lname']
		user_email = request.form['email']
		password = request.form['pwd']
		create_(firstname, lastname, user_email, password)
		return render_template('login.html', fname = firstname)
	else:
		return render_template('signup.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login', methods =  ['POST'])
def login():
	if request.form['login_email'] != "" and request.form['login_pwd'] != "": 
		login_email = request.form['login_email']
		login_pwd = request.form['login_pwd']
		check_(login_email)
		if login_pwd == pwd:
			return render_template('profile.html')
		else:
			return render_template('login.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')