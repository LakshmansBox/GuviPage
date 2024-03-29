from flask import Flask, render_template, url_for, flash, redirect, request
from forms import GuviRegistration, GuviLogin, PersonalDetails
from flask_mysqldb import MySQL
import yaml

db = yaml.load(open('db.yaml'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea57e6b2ccd276540843ffeceb62929a'
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USERNAME'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/profile", methods=['GET','POST'])
def profile():
	form = GuviLogin()
	prof_form = PersonalDetails()
	if prof_form.validate_on_submit():
		dob = prof_form.dob.data
		contact = prof_form.contact.data
		age = prof_form.age.data
		cur = mysql.connection.cursor()
		query = cur.execute("INSERT INTO profile(dob,contact,age) VALUES(%s,%s,%s)",(dob,contact,age))
		mysql.connection.commit()
		cur.close()
	elif form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		cur = mysql.connection.cursor()
		query2 = "SELECT id from user where email=%s and password=%s"
		userlogin =(email,password)
		count = cur.execute(query2,userlogin)
		cur.close()
		if count>0:
			flash('Login Successful Update your Profile', 'success')
			return render_template('profile.html', title='Profile', form=prof_form)
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
			return render_template('login.html', title='Login', form=form)
	return render_template('profile.html', title='Profile', form=prof_form)

@app.route("/register" , methods=['GET','POST'])
def register():
	form = GuviRegistration()
	if form.validate_on_submit():
		
		if request.method == 'POST':
			name = form.username.data
			email = form.email.data
			password = form.password.data
			cur = mysql.connection.cursor()
			query2 = "SELECT id from user where email=%s"
			emailid =(email,)
			count = cur.execute(query2,emailid)
			if  count== 0 :
				query1 = cur.execute("INSERT INTO user(username,email,password) VALUES(%s,%s,%s)",(name,email,password))
				mysql.connection.commit()
				cur.close()
				flash(f'Account Created Successfully for {form.email.data}', 'success')
			else:
				flash(f'Account Exists for {form.email.data}', 'danger')
				return redirect(url_for('login'))
				
		return redirect(url_for('home'))
	return render_template('register.html', title = 'Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = GuviLogin()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		cur = mysql.connection.cursor()
		query2 = "SELECT id from user where email=%s and password=%s"
		userlogin =(email,password)
		count = cur.execute(query2,userlogin)
		if count>0:
			flash('You have been logged in!', 'success')
			return redirect(url_for('profile'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)