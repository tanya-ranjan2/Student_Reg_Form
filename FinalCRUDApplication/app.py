import os
from flask import Flask, render_template, url_for, request ,flash
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import or_
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "regdatabase1.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Reg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),index=True, nullable=False)
    lastname = db.Column(db.String(50),index=True, nullable=False)
    email = db.Column(db.String(15))
    phno = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    course = db.Column(db.String(80))
    regno = db.Column(db.String(80))
    sem = db.Column(db.String(80))

@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/doc')
def doc():
    return render_template('documentation.html')    

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.form:
        try:
            book = Reg(title=request.form.get("title"),lastname=request.form.get("lastname"),email=request.form.get("email"),phno=request.form.get("phno"),gender=request.form.get("gender"),course=request.form.get("course"),regno=request.form.get("regno"),sem=request.form.get("sem"))
            db.session.add(book)
            db.session.commit()
            flash('Information Added successfully')
        except Exception as e:
            print('Error')
            flash('Please fill the below details')
    return render_template("Registration.html")


@app.route('/table', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/<int:page>', methods=['GET', 'POST'])
def table(page):
    page = page
    pages = 5
    #employees = Employees.query.filter().all()
    #employees = Employees.query.paginate(page,pages,error_out=False)
    books = Reg.query.order_by(Reg.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       #books = Book.query.filter(or_(Book.regno == '20BDA15')).paginate(per_page=pages, error_out=True) # OR: from sqlalchemy import or_  filter(or_(User.name == 'ednalan', User.name == 'caite'))
       books = Reg.query.filter(Reg.regno.like(search)).paginate(per_page=pages, error_out=False)
       return render_template('Table.html', books=books, tag=tag)
    return render_template('Table.html', books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        newlastname = request.form.get("newlastname")
        oldlastname = request.form.get("oldlastname")
        newemail = request.form.get("newemail")
        oldemail = request.form.get("oldemail")
        newphno = request.form.get("newphno")
        oldphno = request.form.get("oldphno")
        newgender = request.form.get("newgender")
        oldgender = request.form.get("oldgender")
        newcourse = request.form.get("newcourse")
        oldcourse = request.form.get("oldcourse")
        newregno = request.form.get("newregno")
        oldregno = request.form.get("oldregno")
        newsem = request.form.get("newsem")
        oldsem = request.form.get("oldsem")
        book = Reg.query.filter_by(title=oldtitle,lastname=oldlastname,email=oldemail,phno=oldphno,gender=oldgender,course=oldcourse,regno=oldregno,sem=oldsem).one()
        book.title = newtitle
        book.lastname = newlastname
        book.email = newemail
        book.phno = newphno
        book.gender = newgender
        book.course = newcourse
        book.regno = newregno
        book.sem = newsem
        db.session.add(book)
        db.session.commit()
        flash('Information Updated successfully')
    except Exception as e:
        flash('Could not update Information  ')
        print(e)
    return redirect("/table")

@app.route("/delete", methods=["POST"])
def delete():
    try:
        title = request.form.get("title")
        book = Reg.query.filter_by(title=title).first()
        db.session.delete(book)
        db.session.commit()
        flash('Information Deleted successfully')
    except Exception as e:
        flash('Could not Delete Information  ')
        print(e)
    return redirect("/table")

if __name__ == "__main__":
    app.run(host='0.0.0.0' ,port=5000 )
