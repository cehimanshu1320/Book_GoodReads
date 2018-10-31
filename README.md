# Book_GoodReads
Flask Project, Using ORM, REST APIs and SQL to interact with database present on Heroku

Building an Online Library with user registration service available.
After Logging in users will be able to search for books using ISBN, title or author name
Book Details like author, publication year, ISBN etc will be extracted and displayed using Goodreads REST APIs
Users will be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review. 
Users will not be able to submit multiple reviews for the same book.
On a book page, (if available) the average rating and number of ratings the work has received from Goodreads will be displayed
If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, website will return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
