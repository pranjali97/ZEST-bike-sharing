from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, escape, jsonify
import models as dbHandler
import os
import qrcode
import base64
import io
import random


app = Flask(__name__)


@app.route('/', methods =['GET','POST'])
def index():
	return render_template('index.html')


@app.route('/team', methods=['GET','POST'])
def team():
	return render_template('team.html')	
	

@app.route('/register', methods=['POST', 'GET'])
def register():
	error = None
	if request.method=='POST':
		sap_id = request.form['sap_id']
		name=request.form['name']
		email = request.form['email']
		telephone= request.form['telephone']
		username = request.form['username']
		password = request.form['password']
		error = dbHandler.register(sap_id,name,email,telephone,username,password)
		if error == None:
			return index()
		else:
			return render_template('register.html', error=error)
	else:
		return render_template('register.html')  


@app.route('/rfidregister', methods=['POST','GET'])
def rfidregister():
	error = None
	if request.method=='POST':
		sap_id = request.form['sap_id']
		name=request.form['name']
		email = request.form['email']
		telephone= request.form['telephone']
		branch = request.form['branch']
		year = request.form['year']
		rfidno = request.form['rfidno']
		error = dbHandler.rfidregister(sap_id,name,email,telephone,branch,year,rfidno)
		return render_template('rfidregister.html', error=error)
	else:
		return render_template('rfidregister.html')  


@app.route('/report', methods=['POST','GET'])
def report():
	data=dbHandler.getdata()
	if data:
		return render_template('rfidregister.html',data=data)
	else:
		return render_template('rfidregister.html')



@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if 'username' in session:
		return redirect(url_for('profile'))
	else:
		if request.method == 'POST':
			username_in = request.form['username']
			password_in = request.form['password']
			if username_in == 'admin' and  password_in == 'adminpass':
				session['username'] = username_in
				return redirect(url_for('rfidregister'))
			else:
				error = dbHandler.login(username_in,password_in)
				if error == None:
					session['username'] = username_in
					return redirect(url_for('profile'))
				else:
					return render_template('login.html',error=error)
		else:
			return render_template('login.html')


@app.route('/profile', methods=['POST','GET'])
def profile():
	if 'username' in session:
		username_session = escape(session['username'])
		return render_template('profile.html', session_user_name=username_session)
	else:
		return redirect(url_for('index'))


@app.route('/qrcodes', methods=['POST','GET'])
def qrcodes():
	if 'username' in session:
		username_session = escape(session['username'])
		random_byte=os.urandom(10)
		random_str=int(random_byte.hex(),16)
		val = str(random_str)
		dbHandler.dock_info(username_session,val)
		img=qrcode.make(random_str)
		buffer = io.BytesIO()
		img.save(buffer, format="JPEG")
		img_str = base64.b64encode(buffer.getvalue())
		img_str = "data:image/jpeg;base64," + img_str.decode("utf-8")
		return render_template('profile.html', session_user_name=username_session, code=img_str)
		

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))


@app.errorhandler(500)
def handle_error(error):
	return render_template('error.html')


@app.route('/qrverify', methods = ['GET','POST'])
def qrverify():
	data = request.get_json(force=True)
	flag = dbHandler.qr_verify(data['string'])
	if flag == 1:
		resp = {'val':1}
	else:
		resp = {'val':0}

	return jsonify(resp)

@app.route('/updateds', methods = ['GET','POST'])
def updateds():
	data = request.get_json(force=True)
	cyclenm = data['cyclenm']
	dockst = data['dockst']
	dockno = data['dockno']
	qrstring = data['string']
	flag = dbHandler.update_docking_st(cyclenm,dockst,dockno,qrstring)
	if flag == 1:
		resp = {'val':1}
	else:
		resp = {'val':0}
	return jsonify(resp)	


@app.route('/rfidauth', methods = ['GET','POST'])
def rfidauth():
	data = request.get_json(force=True)
	flag = dbHandler.rfid_verify(data['string'])
	resp={'val':flag}
	if flag == 1:
		resp = {'val':1}
	else:
		resp = {'val':0}

	return jsonify(resp)
	

@app.route('/updaterfidtb', methods = ['GET','POST'])
def updaterfidtb():
	data = request.get_json(force=True)
	ride_id=data['ride_id']
	cyclenm = data['cyclenm']
	dockst = data['dockst']
	dockno = data['dockno']
	rfidstring = data['string']
	flag = dbHandler.update_rfid_tb(ride_id,cyclenm,dockst,dockno,rfidstring)
	if flag == 1:
		resp = {'val':1}
	else:
		resp = {'val':0}

	return jsonify(resp)


@app.route('/endride', methods = ['GET','POST'])
def endride():
	data = request.get_json(force=True)
	ride_id = data['ride_id']
	cyclenm = data['cyclenm']
	dockst = data['dockst']
	dockno = data['dockno']
	rfidstring = data['string']
	# status = False
	flag = dbHandler.end_ride(ride_id)
	# dbHandler.updatecycle_pos(dockst,dockno,cyclenm,status)
	if flag == 1:
		resp = {'val':1}
	else:
		resp = {'val':0}
	
	return jsonify(resp)	

		

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.config['TRAP_HTTP_EXCEPTIONS']=True
	app.run(debug=True,host='0.0.0.0', port=5000)