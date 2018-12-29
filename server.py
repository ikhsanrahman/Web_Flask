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
	confirmed = db.Column(db.Boolean, default=False)
	merchand=db.relationship('Merchand', backref="user", lazy="dynamic")

	def __init__(self, first_name, last_name, confirmed, email, password):

		
		self.first_name=first_name
		self.last_name=last_name
		self.generate_password(password)
		self.email = email
		self.confirmed = False
		
		
	def is_authenticated(self):
		return True
	def is_anonymous(self):
	    return True	
	def is_confirmed(self):
	    return self.confirmed
	def set_confirm (self):
		self.confirmed=True
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
	nama_gambar_toko=db.Column(db.String(100))
	dataset=db.relationship("Dataset", backref="merchand", lazy="dynamic")
	confirmed = db.Column(db.Boolean, default=False)
	user_id=db.Column(db.Integer, db.ForeignKey(User.id))

	def __init__(self, nama_merchand, kategori_merchand, confirmed, alamat_merchand, nama_gambar_toko, user_id):
		self.nama_merchand = nama_merchand
		self.kategori_merchand = kategori_merchand
		self.alamat_merchand = alamat_merchand
		self.nama_gambar_toko = nama_gambar_toko
		self.user_id=user_id
		self.confirmed = False

	def set_confirm_merchand(self):
		self.confirmed = True
	def is_confirmed(self) :
		return self.confirmed

	def __repr__(self):
		return "<nama merchand {}>".format(self.nama_merchand)	


class Dataset(db.Model):
	__Dataset__="dataset"
	id=db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Text)
	title=db.Column(db.Text)
	name_gambar=db.Column(db.Text)
	description=db.Column(db.Text)
	published=db.Column(db.Boolean, default = False)
	confirmed = db.Column(db.Boolean,default = False)
	image=db.relationship("Image", backref="dataset", lazy="dynamic")
	merchand_id=db.Column(db.Integer, db.ForeignKey(Merchand.id))

	def __init__(self, price, title, confirmed = False, name_gambar, description, merchand_id):
		self.price=price
		self.title=title
		self.name_gambar=name_gambar
		self.description=description
		self.merchand_id=merchand_id
		self.confirmed = confirmed

	def set_confirm(self):
		self.confirmed = True 
	def is_confirmed(self) :
		return self.confirmed

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
	merchands = Merchand.query.all()
	return render_template("success_register.html", merchands=merchands, user=user) #home_page di tambah navbar (buat kebun, login, logout, tentang)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
    	email=request.form["email"]
    	password=request.form["password"]
    	user=User.query.filter_by(email=email).first()
    	if user and user.check_password(password):
    		user.is_confirmed()
    		login_user(user)
    		return redirect(url_for("landing_page", id=current_user.id))
    return render_template("login.html") ##home_page di tambah navbar (buat kebun, login, logout, tentang)


@app.route("/landing_page/<int:id>")
@login_required
def landing_page(id):
	merchands = Merchand.query.all()
	return render_template("landing_page.html", merchands=merchands) #here, available for market data Page, buka toko button and page, complete your profile,
											#keranjang belanja

@app.route('/logout')
@login_required
def log_out():
	logout_user()
	return redirect(url_for("home_page"))

@app.route('/merchand_view/<int:user_id>/merchand')
@login_required
def show_merchand(user_id):
	user=User.query.get(user_id)
	return render_template('show_merchand.html', users=user)#filename=filename)


'''def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)'''

@app.route("/register_merchand/<int:id>/merchand", methods=["GET", "POST"])
@login_required
def register_merchand(id):	
	if request.method == "POST":
		nama_merchand = request.form["nama merchand"]
		kategori_merchand=request.form["kategori merchand"]
		alamat_merchand=request.form["alamat"]
		file=request.files['file']
		#if not Merchand.query.filter_by(nama_merchand=nama_merchand).first():
		if file and allowed_file(file.filename) and not Merchand.query.filter_by(nama_merchand=nama_merchand).first():
			filename=secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			new_merchand = Merchand(nama_merchand=nama_merchand,kategori_merchand=kategori_merchand, alamat_merchand=alamat_merchand,
								nama_gambar_toko=filename,
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

@app.route('/edit_your_merchand/<int:merchand_id>', methods=['POST'])
@login_required
def edit_merchand(merchand_id) :
	if current_user.merchand:
		new_merchand = Merchand.query.get(merchand_id) 
		if merchand_id :
			if request.method == "POST" :
				new_nama_merchand = request.form['new_nama_merchand']
				new_kategori_merchand = request.form['new_kategori_merchand']
				new_alamat_merchand = request.form['new_alamat_merchand']
				file = request.files['file']
				if new_nama_merchand and  new_kategori_merchand and new_alamat_merchand  and file and allowed_file(file.filename):
					new_merchand.nama_merchand = new_nama_merchand
					new_merchand.kategori_merchand = new_kategori_merchand
					new_merchand.alamat_merchand = new_alamat_merchand
					filename=secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					db.session.commit()
					return redirect(url_for("show_merchand"))
				return render_template ("edit_merchand.html", msg="you have a blank field")
	return render_template("edit_merchand.html")				


@app.route('/delete/<int:merchand_id>', methods=['DELETE'])
@login_required
def delete_merchand(merchand_id):
	merchand_id = Merchand.query.get(merchand_id)
	if request.method == "DELETE" :
		db.session.delete(merchand_id)
		db.session.commit()
		return redirect(url_for("show_merchand"))

@app.route('/<int:merchand_id>/datasets' )
@login_required
def show_datasets(merchand_id):
	if current_user.merchand :
		merchand = Merchand.query.get(merchand_id)
		return render_template ("show_merchand.html", merchand=merchand)
				
@app.route('/merchand/<int:merchand_id>/datasets', methods=["GET", "POST"])
@login_required
def add_dataset(merchand_id):
	merchands=Merchand.query.get(merchand_id)
	if current_user.merchand:
		if request.form == "POST":
			nama_buah = request.form['nama_buah']
			price = request.form['price']
			file = request.files['file']
			description = request.form['description']
			if file and allowed_file (file.filename) and not Dataset.query.filter_by(title=title).first():
				filename=secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				new_dataset = Dataset ( title=nama_buah, price=price, nama_gambar=filename,
										description=description)
				db.session.add(new_dataset)
				db.session.commit()
				return redirect(url_for("show_dataset", merchans=merchands))
		return render_template('dataset_index.html', merchands=merchands)

@app.route('/merchand/<int:merchand_id>/datasets/<int:dataset_id>/edit', methods=["POST"])
@login_required
def edit_dataset(merchand_id):
	merchand. = Merchand.query.get(dataset_id)
	if request.method == "POST" :
		new_nama_buah = request.form['new_nama_buah']
		new_price = request.form['new_price']
		new_description = request.form['new_description']
		new_file = request.files ['new_file']
		if new_kategori_merchand and new_price and new_description and new_file and allowed_file(file.filename) :
			new_filename = secure_filename (new_file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
			merchand.title = new_nama_buah
			merchand.price = new_price
			merchand.nama_gambar = new_filename
			merchand.description = new_description
			db.session.commit()
			return redirect(url_for("show_dataset"))
	return render_template('dataset_new.html', merchand=merchands)


@app.route("/delete/<dataset_id>", methods=["DELETE"])
@login_required
def delete(id):
	if request.method == "DELETE" :
		image=Image.query,filter_by(id=id).first()
		db.session.delete(image)
		db.session.commit()
		return redirect (url_for("dashboard_petani"))												  


if __name__ == '__main__':
	app.run(port=0000,debug=True)
