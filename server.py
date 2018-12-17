import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_modus import Modus 

app=Flask(__name__)
UPLOAD_FOLDER = '/home/khsan/project/project_agri/'

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///agreed.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='thisissupposedtobesecret'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

modus=Modus(app)	
db=SQLAlchemy(app)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.'	in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file(filename):
	extension=filename.rsplit('.',1)[1].lower()
	return md5(filename.encode()).hexadigets() + '.' + extension


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model):
	__tablename__="user"
	id=db.Column(db.Integer, primary_key=True)
	first_name=db.Column(db.String(50))
	last_name=db.Column(db.String(50))
	email=db.Column(db.String(50))
	password=db.Column(db.String(50))
	merchand=db.relationship('Merchand', backref="user", lazy="dynamic")

	def __init__(self, first_name, last_name, email, password):

		
		self.first_name=first_name
		self.last_name=last_name
		self.generate_password(password)
		self.email = email
		
		
	def is_authenticated(self):
		return True
	def is_anonymous(self):
	    return True	
	def is_confirmed(self):
	    return self.confirmed
	def is_active (self):
		self.is_active=True
	def confirm_user(self):
	    self.confirmed = True
	def get_id(self):
	    return str(self.id)
	def generate_password(self , password):
	    self.password = generate_password_hash(password)
	def check_password(self , password):
	    return check_password_hash(self.password , password)
	def __repr__(self):
	    return "<User {}>".format(self.id)


class Merchand(db.Model):
	__tablename__="merchand"
	id=db.Column(db.Integer, primary_key=True)
	nama_merchand=db.Column(db.String(100))
	kategori_merchand=db.Column(db.String(100)) #mis, pertanian cabe, pertanian padi
	alamat_merchand=db.Column(db.String(100)) #mis, di padang
	dibuat_pada = db.Column(db.DateTime)
	gambar_toko=db.Column(db.String(100))
	dataset=db.relationship("Dataset", backref="merchand", lazy="dynamic")
	user_id=db.Column(db.Integer, db.ForeignKey(User.id))

	def __init__(self, nama_merchand, kategori_merchand, alamat_merchand,gambar_toko, user_id):
		self.nama_merchand=nama_merchand
		self.kategori_merchand=kategori_merchand
		self.alamat_merchand=alamat_merchand
		self.gambar_toko=gambar_toko
		self.user_id=user_id

	def __repr__(self):
		return "<nama merchand {}>".format(self.nama_merchand)


class Dataset(db.Model):
	__Dataset__="dataset"
	id=db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Text)
	title=db.Column(db.Text)
	name_gambar=db.Column(db.Text)
	description=db.Column(db.Text)
	published=db.Column(db.Boolean, default=False)
	#image=db.relationship("Image", backref="dataset", lazy="dynamic")
	merchand_id=db.Column(db.Integer, db.ForeignKey(Merchand.id))

	def __init__(self, price, title, name_gambar, description, merchand_id):
		self.price=price
		self.title=title
		self.name_gambar=name_gambar
		self.description=description
		self.merchand_id=merchand_id


	def __repr__(self):
		return "<dataset {}>".format(self.nama_merchand)

#class Image(db.Model):
#	id=db.Column(db.Integer, primary_key=True)
#	image = db.Column(db.String(100))
#	dataset_id=db.Column(db.Integer, db.ForeignKey(Dataset.id))

#	def __init__(self, image, dataset_id):
#		self.image=image
#		self.dataset_id=dataset_id
#
#	def __repr__(self):
#		return "<image {}>".format(self.image)
    
###########################################################################################
###################### Admin Area, Don't Disturbe. so many secret things a ################
###########################################################################################
@app.route("/")
def home_page():
	return render_template("home_page.html") #"the current_user is" + current_user.first_name   #

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method=="POST":
		first_name=request.form["firstname"]
		last_name=request.form["lastname"]
		email=request.form["email"]
		password=request.form["password"]
		if not User.query.filter_by(first_name=first_name).first():
			user=User(first_name=first_name, last_name=last_name, email=email, password=password)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect (url_for("success_register")) 
	return render_template("register.html")

@app.route('/success_register/')
@login_required
def success_register():
	user=User.query.all()
	return render_template("success_register.html", user=user) #home_page di tambah navbar (buat kebun, login, logout, tentang)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
    	email=request.form["email"]
    	password=request.form["password"]
    	user=User.query.filter_by(email=email).first()
    	if user and user.check_password(password):
    		user.is_active
    		login_user(user)
    		return redirect(url_for("landing_page", id=current_user.id))
    return render_template("login.html") ##home_page di tambah navbar (buat kebun, login, logout, tentang)


@app.route("/landing_page/<int:id>")
@login_required
def landing_page(id):
	return render_template("landing_page.html") #here, available for market data Page, buka toko button and page, complete your profile,
											#keranjang belanja

@app.route('/logout')
@login_required
def log_out():
	logout_user()
	return redirect(url_for("home_page"))



@app.route("/register_merchand/<int:id>/merchand", methods=["GET", "POST"])
@login_required
def register_merchand(id):	
	if request.method == "POST":
		#print(request.form)
		#rint(request.files)
		nama_merchand = request.form["nama merchand"]
		kategori_merchand=request.form["kategori merchand"]
		alamat_merchand=request.form["alamat"]
		file=request.files['file']
		#if not Merchand.query.filter_by(nama_merchand=nama_merchand).first():
		if file and allowed_file(file.filename) and not Merchand.query.filter_by(nama_merchand=nama_merchand).first():
			filename=secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			new_merchand = Merchand(nama_merchand=nama_merchand,kategori_merchand=kategori_merchand, alamat_merchand=alamat_merchand,
								gambar_toko=filename,
									user_id=id)
			db.session.add(new_merchand)
			db.session.commit()
			return redirect(url_for("show_merchand", user_id=current_user.id))

		#if file and allowed_file(file.filename):
		#	filename = secure_filename(file.filename)
		#	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#	return redirect(url_for('show_merchand', user_id=current_user.id, filename=filename))
			

	return render_template("register_merchand.html")	
				#return redirect (url_for('show_image', filename=filename))
	

@app.route('/uploaded_file/<filename>')
@login_required
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/show_image/<filename>')
@login_required
def show_image(filename):
	img=Merchand.query.filter_by(gambar_toko=filename).first()
	return redirect(url_for("show_merchand", filename=filename, img=img))


@app.route('/merchand_view/<int:user_id>/merchand')
@login_required
def show_merchand(user_id):
	user=User.query.get(user_id)
	img=Merchand.query.all()
	return render_template('show_merchand.html', users=user, img=img)#filename=filename)
				
@app.route('/merchand/<int:merchand_id>/datasets', methods=["GET", "POST"])
@login_required
def dataset_index(merchand_id):
	merchand_id=Merchand.query.get(merchand_id)
	if current_user.merchand:
		if request.form == "POST":
			nama_buah = request.form['nama_buah']
			price = request.form['price']
			file = request.files['file']
			description = request.form['description']
			if file and allowed_file (file.filename) and not Dataset.query.filter_by(title=title).first():
				filename=secure_filename(nama_gambar.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				new_dataset = Dataset ( title=nama_buah, price=price,nama_gambar=file,
										description=description, merchand_id=merchand_id)
				db.session.add(new_dataset)
				db.session.commit()
				return redirect(url_for("dataset_index", merchand_id=merchand_id))
		return render_template('dataset_index.html', merchand=Merchand.query.get(merchand_id))

@app.route('/merchand/<int:merchand_id>/datasets/new', methods=["GET", "POST"])
@login_required
def dataset_new(merchand_id):
	return render_template('dataset_new.html', merchand=Merchand.query.get(merchand_id))


@app.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
	image=Image.query,filter_by(id=id).first()
	db.session.delete(image)
	db.session.commit()
	return redirect (url_for("dashboard_petani"))												  


if __name__ == '__main__':
	app.run(port=0000,debug=True)
