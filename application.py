import os
import requests

from flask import Flask, session, request, render_template, jsonify
from flask_session import Session
from sqlalchemy import create_engine, and_
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
			return render_template("Looged_In.html", user_name = record.name, message = '')
		else:
			return render_template("error.html", message = "Incorrect Password")

@app.route("/book_search", methods = ["POST"])
def book_search():
	isbn = request.form.get("isbn")
	isbn_like = '%'+isbn+'%'
	print(f"isbn is {isbn}")
	
	title = request.form.get("title")
	title_like = '%'+title+'%'
	print(f"title is {title}")

	author = request.form.get("author")
	author_like = '%'+author+'%'
	print(f"author is {author}")
	
	if isbn == '' and title == '' and author == '':
		return render_template("error.html", message = "Enter value in any one column")
	else:
		print("Start")
		books_list = Books.query.filter(and_(Books.title.like(title_like), Books.isbn.like(isbn_like), Books.author.like(author_like))).all()
		if len(books_list) == 0:
			return render_template("error.html", message = "No Such Book")
		print(f"Length of book's list is {len(books_list)}")
		return render_template("book_search_results.html", books_list = books_list)

@app.route("/book_search/<string:book_isbn>")
def book_detail(book_isbn):
	print(f"Book ISBN is {book_isbn}")
	book = Books.query.get(book_isbn)
	review = Reviews.query.filter(and_(Reviews.user_id == session.get("logged_in_user_id"), Reviews.book_isbn == book_isbn)).first()
	rating_api = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "t7DlRZMWBsOLbw0596L8g", "isbns": book_isbn})
	
	if rating_api.status_code != 200:			#not successful
		return render_template("error.html", message = "No Such APIs")
	data = rating_api.json()
	rating_count = data["books"][0]["ratings_count"]
	avg_rating = data["books"][0]["average_rating"]
	
	#print(f"Review is {review.review}")
	if review is None:
		return render_template("book_detail.html", book = book, review = review, message = 'No_Review', rating_count = rating_count, avg_rating = avg_rating)
	else:
		return render_template("book_detail.html", book = book, review = review, message = '', rating_count = rating_count, avg_rating = avg_rating)

@app.route("/book_search/<string:book_isbn>", methods = ["POST"])
def add_review(book_isbn):
	review = request.form.get("review")
	r = Reviews(review = review, user_id = session.get("logged_in_user_id"), isbn = book_isbn)
	r.addReview()
	book = Books.query.get(book_isbn)
	review1 = Reviews.query.filter(and_(Reviews.user_id == session.get("logged_in_user_id"), Reviews.book_isbn == book_isbn)).first()
	print("In add_review")
	#print(f"isbn is {isbn}")
	return render_template("book_detail.html", book = book, review = review1, message = "Review Added")
	
@app.route("/api/<string:book_isbn>")
def book_api(book_isbn):
	book = Books.query.get(book_isbn)
	rating_api = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "t7DlRZMWBsOLbw0596L8g", "isbns": book_isbn})
	
	if rating_api.status_code != 200:			#not successful
		return render_template("error.html", message = "No Such APIs")
	data = rating_api.json()
	reviews_count = data["books"][0]["reviews_count"]
	avg_rating = data["books"][0]["average_rating"]	

	return jsonify({"title": book.title, "author": book.author, "year": book.year, "isbn": book_isbn, "review_count": reviews_count, "average_score": avg_rating })