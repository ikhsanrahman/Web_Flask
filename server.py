from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///agreed.db'
app.config['SECRET_KEY']='thisissupposedtobesecret'

db=SQLAlchemy(app)

class admin(db.Mode):
	__tablename__="admin"
	id=db.Column(db.Integer, primary_key=True)
	admin=db.Column(db.String(10))
	password=db.Column(db.String(10))

class peneliti(db.Model):
	__tablename__="peneliti"
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(50))
	email=db.Column(db.String(50))
	password=db.Column(db.String(50))
	universitas=db.Column(db.String(50))
	minat=db.Column(db.String(50))
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


class petani(db.Model):
	__tablename__="petani"
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(50))
	email=db.Column(db.String(50))
	password=db.Column(db.String(50))
	Address=db.Column(db.String(50))
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

class upload_data(db.Model):
	__upload_data__="upload_data"
	id=db.Column(db.Integer, primary_key=True)
	gambar = db.Column(db.Text)
    
###########################################################################################
###################### Admin Area, Don't Disturbe. so many secret things a ################
###########################################################################################

@app.route("/admin/login")
def login_admin():
	return render_template ('login_admin.html', admin=admin)






#############################################################################
################### Peneliti dan Tani Area ##################################
#############################################################################


############# Login Area ####################



@app.route("/login/peneliti", methods=["GET","POST"])
def login():
    if request.method="POST":
    	email=request.form["username"]
    	password=request.form["password"]
    	user=peneliti.query.filter_by(email=email).first()
    	if user and check_password_hash(user.email, user.)


        return redirect(url_for("dashboard_login_peneliti"))
    return render_template("login_peneliti.html", title="Login")


@app.route("/login/petani", methods=["GET","POST"])
def login():
    if request.method="POST":
    	email=request.form["username"]
    	password=request.form["password"]
    	address=request.form['address']
    	jenis_petani=request.form['jenis_petani']	
    	user=petani.query.filter_by(email=email).first()
    	if user and petani.check_password(password):
    		return redirect(url_for("dashboard_login_petani"))
    return render_template("login_petani.html", title="Login")



################################# Register Area ##################################

@app.route("/register/peneliti", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        universitas=request.form.get("universitas")
        minat=request.form.get('minat')
        if not User.query.filter_by(email=email).first():

            user = User(nama=nama, email=email, alamat=alamat, sekolah=nama_sekolah,
                        jenis_kelamin=jenis_kelamin, kategori=kategori,
                        kab_kota=kab_kota, provinsi=provinsi, password=password)

            db.session.add(user)
            db.session.commit()
            return render_template("register_success.html", nama=nama, title="Registrasi Berhasil!")

        else:
            return render_template("register.html", msg="email sudah terdaftar")

    return render_template("register.html", title="Registrasi")



######################	PETANI 		############################################### 

@app.route("/register/petani", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        kategori_petani=request.form.get("kategori_petani")
        address=request.form['address']
        jenis_kelamin=request.form.get('jenis_kelamin')
        if not User.query.filter_by(email=email).first():

            user = User(nama=nama, email=email, alamat=alamat, sekolah=nama_sekolah,
                        jenis_kelamin=jenis_kelamin, kategori=kategori,
                        kab_kota=kab_kota, provinsi=provinsi, password=password)

            db.session.add(user)
            db.session.commit()
            return render_template("register_success.html", nama=nama, title="Registrasi Berhasil!")

        else:
            return render_template("register.html", msg="email sudah terdaftar")

    return render_template("register.html", title="Registrasi")

if __name__ == '__main__':
	app.run(debug=True)