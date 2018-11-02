import os
import csv

from flask import Flask, session, request, render_template
from Models import Books, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://qvlbjtpqmmijub:dc064bc8d031b0a037aa08bd2dea5c51f9a705dbd4bf5e9bd616351764796904@ec2-23-23-80-20.compute-1.amazonaws.com:5432/d8leq47d7jqsnk"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

		
def main():
	f = open("books.csv")
	reader = csv.reader(f)
	count = 0
	for isbn, title, author, year in reader:
		if not isbn == "isbn":
			book = Books(isbn=isbn, title=title, author=author, year=year)
			#book.addBook()
			count += 1
			#db.session.add(book)
			print(f"Count = {count}")
	db.session.commit()
	print(f"Total no of rows are {count}")
	
if __name__ == "__main__":
	with app.app_context():
		main()
	

'''
CREATE TABLE books
(
isbn int PRIMARY KEY,
title varchar(100) not null,
author varchar(100) not null,
year varchar(10) not null
);
'''
