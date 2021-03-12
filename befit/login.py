from flask import render_template,Flask,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,IntegerField,FileField, DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


app=Flask("__name__")

db = SQLAlchemy(app)
app.secret_key="f3er7677r7q3r5"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BEFITDB.sqlite3'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '****.com'
app.config['MAIL_PASSWORD'] = '****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)


class MyForm(FlaskForm):
    name = StringField('Name',[validators.Length(min=5, max=27)])
    username = StringField('Username', [validators.Length(min=5, max=27)])
    age = IntegerField('Age',validators=[DataRequired()])
    address= StringField('Address', [validators.Length(min=10, max=100)])
    contact = IntegerField('Contact', validators=[DataRequired()])
    email_id = StringField('Email id', validators=[DataRequired()])
    password = PasswordField('Password', [validators.EqualTo('passwor', message='Passwords must match')])
    passwor = PasswordField('Confirm', validators=[DataRequired()])
    # img = FileField('img', validators=[DataRequired()])
    # usertype = StringField('usertype', validators=[DataRequired()])
    # status = StringField('status', validators=[DataRequired()])

class BlogForm(FlaskForm):
    blog_id = IntegerField('Blog_id',validators=[DataRequired()],default=temp)
    username = StringField('Username', [validators.Length(min=4, max=27)])
    name = StringField('Name', [validators.Length(min=4, max=27)])
    image = StringField('Image',validators=[DataRequired()])
    title= StringField('Title', validators=[DataRequired()])
    des= StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()],default=date.today())
    
class BlogUpdateForm(FlaskForm):
    blog_id = IntegerField('Blog_id',validators=[DataRequired()],render_kw={'readonly': True})
    username = StringField('Username', validators=[DataRequired()],render_kw={'readonly': True})
    image = StringField('Image',validators=[DataRequired()])
    title= StringField('Title', validators=[DataRequired()])
    des= StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()],default=date.today())


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

#-----View Blog-----#
@app.route('/blog/<username>',methods=['GET','POST'])
def blog(username):
	if request.method=="POST":
		return redirect(url_for('update',username=username))

	result1=Blog.query.filter_by(username=username).first()
	return render_template("blog2.html",resul=result1)




@app.route('/update/<username>',methods = ['GET','POST'])
def update(username):
	
	update= Blog.query.filter_by(username=username).first()
	form = BlogUpdateForm(request.form)
	if request.method == 'POST':
		bpdb.set_trace()
		if update:
			db.session.delete(update)
			db.session.commit()
			update = Blog(username=form.username.data,title= form.title.data,image=form.image.data, des=form.des.data, date=form.date.data, blog_id=form.blog_id.data)
			db.session.add(update)
			db.session.commit()
			username=form.username.data
			return redirect(url_for('blog',username=username))
	result1=Blog.query.filter_by(username=username).first()
	return render_template('update2.html',result=result1,form=form)

@app.route('/delete/<blog_id>', methods=['GET','POST'])
def delete(blog_id):
    delperson= Blog.query.filter_by(blog_id=blog_id).first()
    if request.method == 'POST':
        if delperson:
            db.session.delete(delperson)
            db.session.commit()
            return render_template("home.html")
        return render_template("404.html")
 
    return render_template('delete2.html')


@app.route('/page404')
def page404():
    return render_template("404.html")

#-----Single Details-----#
@app.route('/all_blog')

def all_blog():
	# bpdb.set_trace()
	all_blog= Blog.query.all()
	return render_template('table.html',result1=all_blog)	

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
		
		# f = form.img.data
		# Images = secure_filename(f.Images)
		# f.save(os.path.join(app.instance_path, 'photos', Images))
		bpdb.set_trace()
		register = Register(username=form.username.data,name=form.name.data,gender=request.form['gender'],above_18=form.age.data,address=form.address.data,contact=form.contact.data,email_id=form.email_id.data,password=form.password.data,img="New_image",status="pending",usertype="trainer")	
		db.session.add(register)
		db.session.commit()
		result1=Register.query.all()
		msg = Message('Welcome', sender = '****.com', recipients =[form.email_id.data])
		msg.body = "Thank you for registering with us"
		mail.send(msg)
		return render_template('showall.html',result=result1)	
	return render_template('sign.html',form=form)	


@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1
    return "Total visits: {}".format(session.get('visits'))
    
@app.route('/delete-visits/')
def delete_visits():
	# session.clear()
    session.pop('visits', None) # delete visits
    return 'Visits deleted'

@app.route('/add_blog/<username>',methods=["GET","POST"])
def add_blog(username):
    
    form = BlogForm(request.form)
    if request.method =="POST":
    	bpdb.set_trace()
    	blog = Blog(username=form.username.data,title= form.title.data,image=form.image.data, des=form.des.data, date=form.date.data, blog_id=form.blog_id.data)
    	db.session.add(blog)
    	db.session.commit()
    	username=form.username.data
    	return redirect(url_for('blog',username=username))
    result1=Register.query.filter_by(username=username).first()
    return render_template('Add_Blog.html',result=result1,form=form) 
