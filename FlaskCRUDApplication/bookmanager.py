import os
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import or_
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase8.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), primary_key=True)
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(15))
    phno = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    course = db.Column(db.String(80))
    regno = db.Column(db.String(80))
    sem = db.Column(db.String(80))


    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"),lastname=request.form.get("lastname"),email=request.form.get("email"),phno=request.form.get("phno"),gender=request.form.get("gender"),course=request.form.get("course"),regno=request.form.get("regno"),sem=request.form.get("sem"))
            db.session.add(book)
            db.session.commit()
            print("Success")
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("Registration.html", books=books)

@app.route('/table', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/<int:page>', methods=['GET', 'POST'])
def table(page):
    page = page
    pages = 5
    #employees = Employees.query.filter().all()
    #employees = Employees.query.paginate(page,pages,error_out=False)
    books = Book.query.order_by(Book.regno.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       #books = Book.query.filter(or_(Book.regno == '20BDA15')).paginate(per_page=pages, error_out=True) # OR: from sqlalchemy import or_  filter(or_(User.name == 'ednalan', User.name == 'caite'))
       books = Book.query.filter(Book.regno.like(search)).paginate(per_page=pages, error_out=False)
       return render_template('Table.html', books=books, tag=tag)
    return render_template('Table.html', books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/table")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/table")

if __name__ == "__main__":
    app.run(host='0.0.0.0' ,port=5000 )
    
