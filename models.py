import sqlite3 as sql
from flask import jsonify
import json
from datetime import datetime

con = sql.connect("database_new.db")
cur=con.cursor()

def register(sap_id,name,email,telephone,username,password):
	error = None
	con = sql.connect("database_new.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM person WHERE sap_id= (?);", (sap_id,))
	if cur.fetchone() is not None:
		error = "Sap ID already registered! Sign In?"
	else:
		cur.execute("SELECT * FROM person WHERE username= (?);", (username,))
		if cur.fetchone() is not None:
			error = "Username already taken! try another?"
		else:
			cur.execute("SELECT * FROM person WHERE email= (?);", (email,))
			if cur.fetchone() is  not None:
				error = "Email ID already registered! Sign In? "
			else:
				cur.execute("INSERT INTO person VALUES (?,?,?,?,?,?);" , (sap_id,name,email,telephone,username,password))
				con.commit()
	con.close()
	return error	

def rfidregister(sap_id,name,email,telephone,branch,year,rfidno):
	error = None
	con = sql.connect("database_new.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM rfidusers WHERE sap_id= (?);", (sap_id,))
	if cur.fetchone() is not None:
		error = "Sap ID already registered!"
	else:
		cur.execute("INSERT INTO rfidusers VALUES (?,?,?,?,?,?,?);" , (sap_id,name,email,telephone,branch,year,rfidno,))
		con.commit()
		error = "User Registered"
	con.close()
	return error	


def getdata():
	con = sql.connect("database_new.db")
	cur = con.cursor()
	cur.execute("SELECT*FROM rfidtb")
	data = cur.fetchall()
	con.close()
	return data

def login(usernm,passwd):
	error = None
	con = sql.connect("database_new.db")
	cur = con.cursor()
	cur.execute("SELECT COUNT(username) FROM person WHERE username = (?);",(usernm,))
	if cur.fetchone()[0]:
		cur.execute("SELECT password FROM person WHERE username = (?);",(usernm,))
		for row in cur.fetchall():
			if passwd == row[0]:
				error = None
			else:
				error = "Incorrect Password! try again?"
	else:
		error = "Incorrect Credentials"			
	con.close()
	return error


def dock_info(usernm,qr_string):
	con = sql.connect("database_new.db")
	cur = con.cursor()
	cur.execute("INSERT INTO docking_station VALUES (?,?,?,?,?);" ,(0,0,0,usernm,qr_string))	
	con.commit()
	con.close()

def qr_verify(qrstring):
	flag = 0
	con = sql.connect("database_new.db")
	cur=con.cursor()
	cur.execute("SELECT username FROM docking_station WHERE qrcode_str = (?);", (qrstring,))
	for row in cur.fetchall():
			if row[0] == None:
				flag = 0
			else:
				flag = 1
	con.close()
	return flag

def update_docking_st(cyclenm,dockst,dockno,qrstring):
	flag = 0
	con = sql.connect("database_new.db")
	cur=con.cursor()
	cur.execute("UPDATE docking_station SET cycle_name=(?), dockin_st_no=(?), dock_no=(?) WHERE qrcode_str =(?);", (cyclenm,dockst,dockno,qrstring,))
	flag = 1
	con.commit()
	con.close()
	return flag	

def rfid_verify(rfidstr):
	flag = 0
	con = sql.connect("database_new.db")
	cur = con.cursor()
	cur.execute("SELECT sap_id FROM rfidusers WHERE rfidno = (?);", (rfidstr,))	
	for row in cur.fetchall():
		if row[0] == None:
			flag = 0
			# authentication failed
		else:
			flag = 1
			# authentication successful
	con.close()
	return flag

def update_rfid_tb(ride_id,cyclenm,dockst,dockno,rfidstring):
	flag = 0
	con = sql.connect("database_new.db")
	cur=con.cursor()
	now = datetime.now()
	cur.execute("SELECT sap_id FROM rfidusers WHERE rfidno=(?);",(rfidstring,))
	for row in cur.fetchall():
		sap_num=row[0]
	cur.execute("INSERT INTO rfidtb VALUES (?,?,?,?,?,?,?,?);", (ride_id,sap_num,rfidstring,dockst,dockno,cyclenm,now,'NULL'))
	flag = 1
	con.commit()
	con.close()
	return flag


def end_ride(ride_id):
	flag= 0
	con = sql.connect("database_new.db")
	cur=con.cursor()
	now = datetime.now()
	cur.execute("UPDATE rfidtb SET endtime =(?) WHERE ride_id=(?);",(now,ride_id,))	
	flag = 1
	con.commit()
	con.close()
	return flag

def updatecycle_pos(dockst,dockno,cyclenm,status):
	con = sql.connect("database_new.db")
	cur=con.cursor()
	cur.execute("UPDATE cyclepos_tb SET dockin_st_no=(?), dock_no=(?), cycle_status= (?) WHERE cycle_name=(?);",(dockst,dockno,status,cyclenm,))
	con.commit()
	con.close()	
