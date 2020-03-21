import os, requests

from flask import Flask, session, redirect, render_template, url_for, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

app = Flask(__name__)

# decorater for checking if logged in and redirecting to login if not
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ''
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        try:
            check = db.execute("SELECT * FROM users WHERE username = :name AND password = :password",
            {"name": name, "password": password}).fetchone()
        except Exception as e:
           return render_template("error.html", error=e)

        if check is None:
            error = "Invalid username or password"
            return render_template("login.html", error=error) 
        else:
            session["user"] = name

        return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ''
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        try:
            check = db.execute("SELECT username FROM users WHERE username = :name", 
            {"name": name}).fetchall()
        except Exception as e:
            return render_template("error.html", error=e)

        if len(check) > 0:
            error = "username already exists"
            return render_template("signup.html", error=error)
        else:
            try:
                db.execute("INSERT INTO users(username, password) VALUES (:name, :password)", 
                {"name": name, "password": password})
                db.commit()
            except Exception as e:
                return render_template("error.html", error=e)
            session["user"] = name

        return redirect(url_for("index"))
    else:
        return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))

@app.route("/search", methods=["GET","POST"])
@login_required
def search():
    if request.method == "POST":
        search = request.form.get("search")
        
        try:
            books = db.execute("""SELECT * FROM books 
            WHERE isbn ILIKE :search OR title ILIKE :search OR author ILIKE :search""",
            {"search": '%'+search+'%'}).fetchall()
        except Exception as e:
            return render_template("error.html", error=e)

        return render_template("search.html", books=books, query=search)
    else:
        return render_template("search.html")

@app.route("/search/<isbn>", methods=["GET","POST","UPDATE"])
@login_required
def searchBook(isbn):
    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")

        try:
            check = db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn",
             {"username": session["user"], "isbn": isbn}).fetchone()

            if check is None:
                db.execute("""INSERT INTO reviews(isbn, uid, username, rating, review) VALUES 
                (:isbn, (SELECT uid FROM users WHERE username = :username), :username, :rating, :review)""", 
                {"isbn": isbn, "username": session["user"], "rating": rating, "review": review})
                db.commit()
            else:
                db.execute(""" UPDATE reviews SET rating = :rating, review = :review
                WHERE username = :username AND isbn = :isbn""", 
                {"isbn": isbn, "username": session["user"], "rating": rating, "review": review})
                db.commit()
        except Exception as e:
            return render_template("error.html", error=e)

        return redirect(url_for('searchBook', isbn=isbn)) 

    else:
        try:
            book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
            goodreads_review = requests.get("https://www.goodreads.com/book/review_counts.json", 
            params={"key": "oX2xT1YwCWw4eRVqQjFb4Q", "isbns": isbn}).json()
        
            reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",{"isbn": isbn}).fetchall()
            self_review = db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND username = :username", 
            {"isbn": isbn, "username": session["user"]}).fetchone()
        except Exception as e:
            return render_template("error.html", error=e)

        return render_template("book.html", 
        book=book, goodreads_review=goodreads_review, reviews=reviews, self_review=self_review)

@app.route("/api/<isbn>")
@login_required
def api(isbn):
    try:
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    except Exception as e:
        return render_template("error.html", error=e)

    if book is None:
        return jsonify({"error": "book not found"}), 422

    return jsonify({
    "title": book.title,
    "author": book.author,
    "year": book.year,
    "isbn": book.isbn,
    "review_count": book.review_count,
    "average_score": book.average_score
    })

if __name__ == "__main__":
    app.run(debug = True)