import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from Models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://qvlbjtpqmmijub:dc064bc8d031b0a037aa08bd2dea5c51f9a705dbd4bf5e9bd616351764796904@ec2-23-23-80-20.compute-1.amazonaws.com:5432/d8leq47d7jqsnk"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")
	
@app.route("/logout")
def logout():
	print(session.get("logged_in_user_id"))
	if session.get("logged_in_user_id") is not None:
		session["logged_in_user_id"] = None
	print(session.get("logged_in_user_id"))
	return render_template("logout.html")
	
@app.route("/registered", methods = ["POST"])
def register():
	name = request.form.get("users_name")
	print(f"Name is {name}")
	email = request.form.get("email")
	print(f"email is {email}")
	password = request.form.get("password")
	print(f"password is {password}")
	
	user = Users(name = name, email = email, password = password)	
	
	#Adding User
	#user.addUser(name, email, password)
	user.addUser()
	
	return render_template("success.html")
	
@app.route("/login", methods = ["POST"])
def log_in():
	email = request.form.get("email")
	
	if Users.query.filter_by(email = email).count() == 0:
		return render_template("error.html", message = "No Such User")
	else:
		password = request.form.get("password")
		record = Users.query.filter_by(email = email).first()
		if password == record.password:
			session["logged_in_user_id"] = record.user_id
			return render_template("Looged_In.html", message = record.name)
		else:
			return render_template("error.html", message = "Incorrect Password")

@app.route("/book_search", methods = ["POST"])
def log_in():
	isbn = request.form.get("isbn")
	#print(f"isbn is {isbn}")
	title = request.form.get("title")
	#print(f"title is {title}")
	author = request.form.get("author")
	#print(f"author is {author}")
	
	if isbn is None and title is None and author is None:
		return render_template("error.html", message = "Enter value in any one column")
	else:
		Reviews.query.filter_by(and(Reviews.isbn.like("%isbn%")))
	

