from flask import Flask,render_template, request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import os
from flask_mail import Mail

app = Flask(__name__)

app.secret_key = os.urandom(24) 

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "harshpandya677@gmail.com",
    MAIL_PASSWORD = "gphuvtlxzcmlpyxq"
)
mail = Mail(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:Harsh%402004%40@localhost/portfolio'
# app.config["SQLALCHEMY_MODIFICATION_TRACK"]
db = SQLAlchemy(app)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    p_name = db.Column(db.String(100), nullable = False)
    p_category = db.Column(db.String(50), nullable = False)
    p_desc = db.Column(db.String(300), nullable = False) 
    p_start_date = db.Column(db.String(30), nullable = False)
    img_url = db.Column(db.String(100),nullable=True)
    p_url = db.Column(db.String(255), nullable = False)
    img_1 = db.Column(db.String(200))
    img_2 = db.Column(db.String(200))
    img_3 = db.Column(db.String(200))
    img_4 = db.Column(db.String(200))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/projects")
def portfolio():
    projects = Projects.query.all()
    return render_template("portfolio.html",projects=projects)

@app.route("/project_details/<string:p_name>",methods = ["GET"])
def portfolio_detail(p_name):
    project = Projects.query.filter_by(p_name=p_name).first()
    return render_template("portfolio-details.html",project=project)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']        

        mail.send_message("New Message From : "+ name,
        sender = email,
        recipients = ["harshpandya677@gmail.com"],
        body = subject + "\n" + message 
        )

        flash("✅ Your message has been sent successfully!", "success")
        return redirect("/contact")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True,port=8000)   