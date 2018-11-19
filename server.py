from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///agreed.db'
app.config['SECRET_KEY']='thisissupposedtobesecret'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

db=SQLAlchemy(app)

@login_manager.user_loader
def load_user(self_id):
	return Peneliti.query.get(self_id)

class Merchand(db.Model):
	__tablename__="Merchand"
	id=db.Column(db.Integer, primary_key=True)
	nama=db.Column(db.String(100))
	merchand_id=db.Column(db.Integer, )
	merchand=db.Column(db.String(100))

	def __repr__(self):
		return "<nama merchand {}>".format(self.merchand)



class User(db.Model):
	__tablename__="user"
	id=db.Column(db.Integer, primary_key=True)
	first_name=db.Column(db.String(50))
	last_name=db.Column(db.String(50))
	email=db.Column(db.String(50))
	password=db.Column(db.String(50))
	

	def __init__(self, first_name, last_name,email, password):

		self.first_name=first_name
		self.last_name=last_name
		self.generate_password(password)
		self.email = email
		
		
	def address(self, address):
		self.address=address
	def is_authenticated(self):
		return True
	def is_anonymous(self):
	    return True	
	def is_confirmed(self):
	    return self.confirmed
	def confirm_user(self):
	    self.confirmed = True
	def get_id(self):
	    return str(self.user_id)
	def generate_password(self , password):
	    self.password = generate_password_hash(password)
	def check_password(self , password):
	    return check_password_hash(self.password , password)
	def __repr__(self):
	    return "<User %r>"% (get_id)


class Image(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	nama=db.Column(db.String(100))
	image = db.Column(db.String(100))

	def __repr__(self):
		return "<image {}>".format(self.image)

class Upload_data(db.Model):
	__upload_data__="upload_data"
	id=db.Column(db.Integer, primary_key=True)
	gambar = db.Column(db.Text)
    
###########################################################################################
###################### Admin Area, Don't Disturbe. so many secret things a ################
###########################################################################################
@app.route("/")
def home_page():
	return render_template("home_page.html")



@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method=="POST":
		first_name=request.form["firstname"]
		last_name=request.form["lastname"]
		email=request.form["email"]
		password=request.form["password"]
		user=User(first_name=first_name, last_name=last_name, email=email, password=password)
		user.session.add(user)
		user.session.commit()
		return redirect (url_for("success_register.html")) 
	return render_template("register.html")

@app.route('/success_register')
def success_register():
	return render_template("success_register.html") #here, avalaible 1. your registration has been accepted	
													#2. direct to login , available for login button

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
    	email=request.form["email"]
    	password=request.form["password"]
    	user=User.query.filter_by(username=username).first()
    	if user and user.check_password(password):
    		#load_user_peneliti(user)
    		return redirect(url_for("landing_page"))
    return render_template("login.html")


@app.route("/landing_page")
@login_required
def landing_page():
	return render_template("landing_page.html") #here, available for market data Page, buka toko button and page, complete your profile,
												#keranjang belanja


@app.route("/register_merchand", methods=["GET", "POST"])
def merchand():
    if request.method == "POST":
        nama = request.form["nama"]
        merchand = request.form["email"]
        
        if not Merchand.query.filter_by(nama=nama).first():

            user = Merchand(nama=nama, merchand=merchand) 
            db.session.add(user)
            db.session.commit()
            return redirect (url_for("dashboard_petani"))
    return render_template("register_merchand.html")

@app.route("/success_merchand")
#@login_required
def dashboard_petani:
	return	render_template ("dashboard_petani.html") # here, avalaible for toko completing button,
				
@app.route('/add', methods=["GET", "POST"])
#@login_required
def add():
	if request.method=="POST":
		id=request.form["id"]
		nama=request.form["nama_gambar"]
		gambar=request.form["gambar"]
		image=Image(gambar=gambar, id=id, nama=nama)
		image.session.add(image)
		image.session.commit()
		return redirect(url_for("dashboard_petani"))
	else:
		return render_template('add.html')

@app.route("/ubah/<id>", methods=["GET", "POST"])
@login_required
def change(id):
	image=Image.query.filter_by(id=id).first()
	if request.method=="POST":
		image.id=request.form['id']
		image.nama=request.form["nama"]
		image.gambar=request.form["gambar"]
		db.session.add(image)
		db.session.commit()
		return redirect (url_for("dashboard_petani"))	
	else :
		return render_template("change.html")

@app.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
	image=Image.query,filter_by(id=id).first()
	db.session.delete(image)
	db.session.commit()
	return redirect (url_for("dashboard_petani"))												  

@app.route('/logout')
@login_required
def logout():
	return redirect(url_for("home_page"))









if __name__ == '__main__':
	app.run(debug=True)