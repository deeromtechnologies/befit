from flask import render_template,Flask,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import bpdb
import uuid
import random
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,IntegerField,FileField
from wtforms.validators import DataRequired

id = uuid.uuid1()
n = random.randint(0,100)
temp=id.node
temp=temp+n


app=Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BEFITDB.sqlite3'
db = SQLAlchemy(app)
app.secret_key="f3er7677r7q3r5"



class MyForm(FlaskForm):
    name = StringField('Name',[validators.Length(min=5, max=27)])
    username = StringField('Username', [validators.Length(min=5, max=27)])
    # gender = StringField('gender', validators=[DataRequired()])
    age = IntegerField('Age',validators=[DataRequired()])
    address= StringField('Address', [validators.Length(min=10, max=100)])
    contact = IntegerField('Contact', validators=[DataRequired()])
    email_id = StringField('Email id', validators=[DataRequired()])
    password = PasswordField('Password', [validators.Length(min=6, max=15)])
    passwor = PasswordField('Confirm', [validators.Length(min=6, max=15)])
    # img = FileField('img', validators=[DataRequired()])
    # usertype = StringField('usertype', validators=[DataRequired()])
    # status = StringField('status', validators=[DataRequired()])

# @app.route('/submit', methods=('GET', 'POST'))
# def submit():
#     form = MyForm()
#     if form.validate_on_submit():
#         return "Successfully Validated"
    # return render_template('showall.html')

#-----Table Register: tablename-register-----#
class Register(db.Model):

	username = db.Column(db.String(80), primary_key=True)
	name = db.Column(db.String(80), unique=False, nullable=False)
	gender = db.Column(db.String(80), unique=False, nullable=False)
	above_18 = db.Column(db.String(50), unique=False, nullable=False)
	address = db.Column(db.String(200), unique=False, nullable=False)
	contact = db.Column(db.String(80), unique=True, nullable=False)
	email_id = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(80), unique=False, nullable=False)
	img = db.Column(db.String(100), nullable=False)
	usertype = db.Column(db.String(80), unique=False, nullable=False)
	status = db.Column(db.String(100), unique=False, nullable=False)

	def __init__(self, username, name, address, gender, above_18, contact, email_id, password, img, usertype, status):
		
		self.name = name
		self.username = username
		self.gender = gender
		self.above_18 = above_18
		self.address=address
		self.contact = contact
		self.email_id = email_id
		self.password = password
		self.img = img
		self.usertype = usertype
		self.status = status

#-----Table Blog: tablename-blog-----#
class Blog(db.Model):

	blog_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), db.ForeignKey('register'), nullable=False)
	image = db.Column(db.String(100), unique=False, nullable=False)
	title=db.Column(db.String(100), unique=False, nullable=False)
	des = db.Column(db.String(1000), unique=False, nullable=False)
	date = db.Column(db.DateTime, nullable=False)

	def __init__(self,blog_id, username, image, title, des, date):
		
		self.blog_id= blog_id
		self.username = username
		self.image = image
		self.title = title
		self.des = des
		self.date = date

#-----Home-----#
@app.route('/')
@app.route('/home/')
def home():
    return render_template("home.html")

#-----Details-----#
@app.route('/show_all')
def show_all():
	# bpdb.set_trace()
	result1=Register.query.all()
	return render_template('showall.html',result=result1 )

@app.route('/blog')
def blog():
	result1=Blog.query.all()
	return render_template("blog2.html",result=result1)

	


# -----Single Details-----#
# @app.route('/detail/<username>')

# def detail(username):
# 	# bpdb.set_trace()
# 	detail= Register.query.filter_by(username=username).first()
# 	return render_template('table.html',result=detail)	

#-----Edit Profile-----#
# @app.route('/edit_profile')
# def detail():
# 	detail= Register.query.filter_by(username=username).first()
# 	return render_template('detail.html',result=detail)	


#-----Login-----#
@app.route('/login',methods=['GET','POST'])
def login():
		if request.method =="POST":
			username=request.form['username']
			password=request.form['password']
			session["username"]=username
			session["password"]=password
			return redirect(url_for('add_blog',username=username))
		else:

			if "username" in session:
				return redirect(url_for('home'))

			return render_template("login.html")

#-----Logout-----#
@app.route("/logout")
def logout():
		# session.clear()
		session.pop("username",None)
		return redirect(url_for("login"))

#-----Signup-----#
@app.route('/signup',methods=['POST','GET'])
def signup():
	form = MyForm(request.form)

	if request.method =="POST" and form.validate_on_submit():
		# return "Successfully Validated"
		# bpdb.set_trace()
		register = Register(username=form.username.data,name=form.name.data,gender=request.form['gender'],above_18=form.age.data,address=form.address.data,contact=form.contact.data,email_id=form.email_id.data,password=form.password.data,img="no_image",status="pending",usertype="trainer")	
		db.session.add(register)
		db.session.commit()
		# bpdb.set_trace()
		# result1=Register.query.filter_by(username=request.form['username']).first()
		result1=Register.query.all()
		return render_template('showall.html',result=result1)	
	return render_template('sign.html',form=form)	



# @app.route('/signup',methods=["POST","GET"])
# def signup():
#     form=RegistrationForm(request.form)
#     #bpdb.set_trace()
#     if request.method =="POST" and form.validate():
#         #bpdb.set_trace()
#         user = signup(form.id.data, form.firstname.data, form.lastname.data, form.username.data, form.email.data,form.password.data,form.confirmpassword.data)
#         db.session.add(user)
#         return redirect(url_for('users'))
#     else:   
#         return render_template('signup.html',form=form) 



# @app.route('/visits-counter/')
# def visits():
#     if 'visits' in session:
#         session['visits'] = session.get('visits') + 1  # reading and updating session data
#     else:
#         session['visits'] = 1
#     return "Total visits: {}".format(session.get('visits'))
    
# @app.route('/delete-visits/')
# def delete_visits():
# 	# session.clear()
#     session.pop('visits', None) # delete visits
#     return 'Visits deleted'

@app.route('/add_blog/<username>',methods=["GET","POST"])
def add_blog(username):
    # bpdb.set_trace()
    
    if request.method == 'POST':
        blog = Blog(username=request.form['username'],title= request.form['title'],image=request.form['image'], des=request.form['des'], date=date.today(), blog_id=temp)
        db.session.add(blog)
        db.session.commit()
        # result1=Blog.query.filter_by(username=username).first()
        return redirect(url_for('blog'))
    result1=Register.query.filter_by(username=username).first()
    return render_template('addblog.html',result=result1) 
