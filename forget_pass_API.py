# import Libraries
from itsdangerous import TimedSerializer,TimestampSigner
from flask import Flask,request,jsonify
from pymongo import MongoClient
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

# connect MongoDB for registered account and password 
client = MongoClient()
db = client.Email_data
app = Flask(__name__)
em = []
p = []

# logging 
log_form = '%(levelname)s - %(asctime)s - %(message)s'
logging.basicConfig(filename = "H:/logger_file/forget_password_logger.log",format = log_form, level = logging.DEBUG)
logger = logging.getLogger()

# routing for get Gmail 
@app.route('/' ,methods = ['POST'])
def pswrd():
	gmail_username = 'resetp48@gmail.com'
		

	if request.method == "POST":
		data = request.get_data(cache =False, as_text = True)
		try:
			data = json.loads(data)
			logger.info('data in json format')

		except:
			logger.info('data in text format')

		
		data = data["email"]
		s = TimedSerializer('secret')	
		tok =s.dumps(data)
		# check email account is rgistered or not
		for i in db.email_mongo.find():
			if data == i["email"]:
				try:
					re = "email matched"
					for i in db.email_update.find():
						ex = i["up"]
					db.email_update.update({"up":ex},{"up":data})

					#msg = "your octopus varification link is = "+tok
					msg = 'Hi!\nHow are you?\nHere is the link you wanted:\nfile:///C:/Users/hp/AppData/Local/Packages/Microsoft.SkypeApp_kzf8qxf38zg5c/LocalState/Downloads/Octopus_Forgot%20Password/reset-password.html'

					# send email 
					session = smtplib.SMTP('smtp.gmail.com', 587)
					session.starttls()
					session.login(gmail_username, 'octopus12345')
					session.sendmail(gmail_username, data, msg)
					session.quit()
					logger.info('varification link is sent in your registered account')
					break
				except:
					re = "enter your valid email address"
					logger.info('not a valid gmail account')
		return jsonify(re)
#roution for reset password 
@app.route('/reset' ,methods = ['POST'])
def reset():
	if request.method == "POST":

		new_pswrd = request.get_data(cache =False, as_text = True)
		new_pswrd = json.loads(new_pswrd)

		#store new password in two objects for checking they same or not 
		first_pass = new_pswrd["enter"]
		re_pass = new_pswrd["reenter"]
		if first_pass == re_pass:
			try:				
				for i in db.email_update.find():
					exx = i["up"]

				# update the new password in database
				for j in db.email_mongo.find():
					if exx == j["email"]:
						old_pass = j["password"]
						db.email_mongo.update({"email":exx,"password":old_pass},{"email":exx,"password":first_pass})
						logger.info('password changed')
				return jsonify("your password is successfully changed")
			except:
				print('password not changed')
		else:

			return jsonify("your password is not matched please check and re-enter your password")
		


if __name__ == '__main__':
    app.run(debug = True, port = 8080)

