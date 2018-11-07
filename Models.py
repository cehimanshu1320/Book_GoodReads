from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Users(db.Model):
	__tablename__ = "users"
	user_id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, nullable = True)
	email = db.Column(db.String, nullable = False)
	password = db.Column(db.String, nullable = False)
	id_ = 0
	
	def addUser(self):
		#user = Users(name = name, email = email, password = password)
		#db.create_all()
		print(f"id is {Users.id_}")
		db.session.add(self)
		db.session.commit()

	def __init__(self, name, email, password):
		self.user_id = Users.id_ + 1
		Users.id_ += 1
		#self.id = self.user_id
		self.name = name
		self.email = email
		self.password = password
'''	
	def addReview(self, review, rating):
		r = Reviews(review = review, user_id = self.id_, isbn = Book.getBookIsbn)
		db.session.add(r)
		db.session.commit()
'''		
class Reviews(db.Model):
	__tablename__ = "reviews"
	review_id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
	review = db.Column(db.String, nullable = True)
	#rating = db.Column(db.Integer, nullable = True)
	book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable = False)
	id_ = 0

	def __init__(self, review, user_id, isbn):
		self.review_id = Reviews.id_ + 1
		Reviews.id_ += 1
		self.user_id = user_id
		self.review = review
		self.book_isbn = isbn
		#self.rating = rating
		
	def addReview(self):
		#r = Reviews(review = review, user_id = self.id_, isbn = Book.getBookIsbn)
		db.session.add(self)
		db.session.commit()

		
class Books(db.Model):
	__tablename__ = "books"
	isbn = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String, nullable = False)
	author = db.Column(db.String, nullable = False)
	year = db.Column(db.String, nullable = False)
	
	def addBook(self):
		#user = Users(name = name, email = email, password = password)
		#db.create_all()
		db.session.add(self)
		db.session.commit()
		
	def __init__(self, isbn, title, author, year):
		self.isbn = isbn
		self.title = title
		self.author = author
		self.year = year
	
	def getBookIsbn(self):
		return self.isbn
		
'''
CREATE TABLE users
(
user_id int PRIMARY KEY,
name varchar(50),
email varchar(100) not null,
password varchar(20) not null
)
CREATE TABLE reviews
(
review_id int PRIMARY KEY,
user_id int not null REFERENCES users(user_id),
review varchar(1000),
rating int DEFAULT 0
);
'''