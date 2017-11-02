from flask_sqlalchemy import SQLAlchemy
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

import geocoder
import urllib
import json

db = SQLAlchemy()
#db = MySQL()

class household_account(db.Model):
	__tablename__ = 'household_account'
	uid = db.Column('account_id', db.Integer, primary_key=True)
	account_name = db.Column('account_username', db.String(85))
	account_password = db.Column('account_password', db.String(85))

	def __init__(self, account_name, account_password):
		self.account_name = account_name
		self.set_password(account_password)

	def set_password(self, password):
		self.account_password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.account_password, password)

class Place(object):
	def meters_to_walking_time(self, meters):
		# 80 meters is ~ one minute walking time
		return int(meters/80)

	def wiki_path(self, slug):
		return urllib.parse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
	
	def address_to_latlng(self, address):
		g = geocoder.google(address)
		return(g.lat, g.lng)

	def query(self, address):
		lat, lng = self.address_to_latlng(address)

		query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
		g = urllib.request.urlopen(query_url)
		results = str(g.read(),"utf-8")
		g.close()

		data = json.loads(results)

		places = []
		for place in data['query']['geosearch']:
			name = place['title']
			meters = place['dist']
			lat = place['lat']
			lng = place['lon']

			wiki_url = self.wiki_path(name)
			walking_time = self.meters_to_walking_time(meters)

			d = {
				'name': name,
				'url': wiki_url,
				'time': walking_time,
				'lat': lat,
				'lng': lng
			}

			places.append(d)

		return places