from flask import Flask, render_template, request, session, redirect, url_for
from models import db, household_account, Place
from forms import SignupForm, SigninForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost:3306/mpc_prod' % "G%21ng3rBr%23%40d"
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_PORT'] = '3306'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'G!ng3rBr#@d'
#app.config['MYSQL_DB'] = 'mpc_prod'
db.init_app(app)

app.secret_key = "testing_this_little_thing_out"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about/")
def about():
	return render_template("about.html")

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
	if 'account_name' in session:
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			new_household_account = household_account(form.account_name.data,form.account_password.data)
			db.session.add(new_household_account)
			db.session.commit()

			session['account_name'] = new_household_account.account_name
			return redirect(url_for('home'))
	elif request.method == "GET":
		return render_template('signup.html', form=form)

	return render_template("signup.html", form = form)


@app.route('/signin/', methods=['GET', 'POST'])
def signin():
	if 'account_name' in session:
		return redirect(url_for('home'))

	form = SigninForm()

	if request.method == "POST":
		if form.validate == False:
			return render_template("signin.html", form=form)
		else:
			user_name = form.user_name.data
			password = form.user_password.data

			user = household_account.query.filter_by(account_name=user_name).first()
			if user is not None and user.check_password(password):
				session['account_name'] = form.user_name.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('signin'))

	elif request.method == "GET":
		return render_template("signin.html", form=form)

	return render_template("signin.html")

@app.route('/logout')
def logout():
	session.pop('account_name', None)
	return redirect(url_for('index'))


@app.route('/home/', methods=['GET', 'POST'])
def home():
	if 'account_name' not in session:
		return redirect(url_for('signin'))

	form = AddressForm()

	places = []
	my_coordinates = (30.0000, 30.0000)

	if request.method == 'POST':
		if form.validate == False:
			return render_template("home.html", form=form)
		else:
			# get the address
			address = form.address.data
			# query for places around it
			p = Place()
			my_coordinates = p.address_to_latlng(address)
			places = p.query(address)
			# return those results
			return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)
	elif request.method == 'GET':
		return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

	return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)


if __name__ == "__main__":
	app.run(host='0.0.0.0')