from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///agreed.db'
app.config['SECRET_KEY']='thisissupposedtobesecret'

db=SQLAlchemy(app)

class Admin(db.Mode):
	__tablename__="admin"
	id=db.Column(db.Integer, primary_key=True)
	admin=db.Column(db.String(10))
	password=db.Column(db.String(10))

class Peneliti(db.Model):
	__tablename__="peneliti"
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(50))
	email=db.Column(db.String(50))
	password=db.Column(db.String(50))
	universitas=db.Column(db.String(50))
	kategori_penelitian=db.Column(db.String(50))
	jenis_kelamin=db.Column(db.Text)

	def __init__(self, username, email, password, universitas,
                 jenis_kelamin, kategori_penelitian):

        self.username = username
        self.set_password(password)
        self.email = email
        self.universitas=universitas
        self.kategori_penelitian=kategori_penelitian
        self.jenis_kelamin=jenis_kelamin
        self.authenticated = False
        self.confirmed = False
   
    def address(self, address):
    	self.address=address
    def 


    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return True

    def check_password(self, password):
        return check_password(self.password, password)

    def is_confirmed(self):
        return self.confirmed

    def confirm_user(self):
        self.confirmed = True

    def get_id(self):
        return str(self.user_id)

    def generate_password(self , password):
        self.password = generate_password_hash(password, methods='sha256')

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def __repr__(self):
        return "<User %r>"% (self.nama)


class Petani(db.Model):
	__tablename__="petani"
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(50))
	email=db.Column(db.String(50))
	password=db.Column(db.String(50))
	address=db.Column(db.String(50))
	kategori_petani=db.Column(db.String(50))
	jenis_kelamin=db.Column(db.Text)

	def __init__(self, username, email, password, Address,
                 jenis_kelamin, kategori_petani):

        self.username = username
        self.set_password(password)
        self.email = email
        self.Address=Address
        self.kategori_petani=kategori_petani
        self.jenis_kelamin=jenis_kelamin
        self.authenticated = False
        self.confirmed = False
   
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return True

    def check_password(self, password):
        return check_password(self.password, password)

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
        return "<User %r>"% (self.nama)

class Upload_data(db.Model):
	__upload_data__="upload_data"
	id=db.Column(db.Integer, primary_key=True)
	gambar = db.Column(db.Text)
    
###########################################################################################
###################### Admin Area, Don't Disturbe. so many secret things a ################
###########################################################################################

@app.route("/login/admin")
login_required(admin)
def login_admin():
	return render_template ('login_admin.html', admin=admin)






#############################################################################
################### Peneliti dan Tani Area ##################################
#############################################################################


############# Login Area ####################



@app.route("/login/peneliti", methods=["GET","POST"])
login_required(peneliti)
def login():
    if request.method="POST":
    	email=request.form["username"]
    	password=request.form["password"]
    	user=peneliti.query.filter_by(email=email).first()
    	if user and user.check_password(password):
    		return redirect(url_for("page_market_place"))
    return render_template("login_peneliti.html", title="Peneliti Login")


@app.route("/login/petani", methods=["GET","POST"])
login_required(petani)
def login():
    if request.method="POST":
    	email=request.form["username"]
    	password=request.form["password"]
    	address=request.form['address']
    	jenis_petani=request.form['jenis_petani']	
    	user=petani.query.filter_by(email=email).first()
    	if user and petani.check_password(password):
    		return redirect(url_for("dashboard_login_petani"))
    return render_template("login_petani.html", title="Petani Login")



############## Dashboard Petani #######################

@app.route('/dashboard_login_petani')
def dashboard_login_petani():
	if current_user.role='user':
		return render_template('dashboard_login_petani.html', controller='controller for petani')

@app.route('/page_market_place')
def page_market_place():
	if current_user.role='user':
		return render_template ('page_market_place.html')




################################# Register Area ##################################


################################# REGISTER PENELITI ###############################

@app.route("/register/peneliti", methods=["GET", "POST"])
def register_peneliti():

    if request.method == "POST":
        username = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        universitas=request.form["universitas"]
        kategori_penelitian=request.form['kategori_penelitian']
        jenis_kelamin = request.form.get("jenis_kelamin")
        if not Penelti.query.filter_by(email=email).first():

            user = Peneliti(nama=nama, email=email, kategori_penelitian=kategori_penelitian, 
            			universitas=universitas,
                        jenis_kelamin=jenis_kelamin, 
                         password=password)

            db.session.add(user)
            db.session.commit()
            return render_template("register_peneliti_success.html", nama=nama, title="Registrasi Berhasil!")

        else:
            return render_template("register_peneliti.html", msg="petani sudah terdaftar")

    return render_template("register.html", title="Registrasi")



######################	REGISTRAI PETANI 		############################################### 

@app.route("/register/petani", methods=["GET", "POST"])
def register_petani():

    if request.method == "POST":
        username = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        kategori_petani=request.form.get("kategori_petani")
        address=request.form['address']
        jenis_kelamin=request.form.get('jenis_kelamin')
        if not User.query.filter_by(email=email).first():

            user = User(username=username, email=email, address=address, jenis_kelamin=jenis_kelamin, 
            			 kategori_petani=kategori,
                         password=password)

            db.session.add(user)
            db.session.commit()
            return render_template("register_peneliti_success.html", username=username, title="Registrasi Berhasil!")

        else:
            return render_template("register_petani.html", msg="petani sudah terdaftar")

    return render_template("register.html", title="Registrasi")

if __name__ == '__main__':
	app.run(debug=True)