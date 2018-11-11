from flask import Flask, render_template, url_for

app=Flask(__name__)

@app.route('/login')
def login():
	return render_template ('login.html')

@app.route
def register():
	return render_template ('register_agri.html')

if __name__ == '__main__':
	app.run(debug=True)