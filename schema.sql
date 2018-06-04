drop table if exists person;
	create table person(
		sap_id integer primary key,
		name text not null,
		email varchar(50) not null unique,
		telephone integer not null,
		username varchar(50) unique,
		password varchar(50) not null
		);


drop table if exists docking_station;
	create table docking_station(
		cycle_name varchar(50) ,
		dockin_st_no integer,
		dock_no integer,
		username varchar(50),
        qrcode_str text 
		);
	
drop table if exists rfidusers;
	create table rfidusers(
		sap_id integer primary key unique,
		name text not null,
		email varchar(50) not null unique,
		telephone integer not null,
		branch varchar(20) not null,
		year integer not null,
		rfidno integer not null
		);	

drop table if exists rfidtb;
	create table rfidtb(
		ride_id integer primary key,
		sap_id integer,
		rfid_code integer,
		dockin_st_no integer,
		dock_no integer,
		cycle_name varchar(50),
		starttime TIMESTAMP DEFAULT NULL,
		endtime TIMESTAMP DEFAULT NULL
		);	

drop table if exists cyclepos_tb;
	create table cyclepos_tb(
		cycle_name varchar(50) primary key,
		dockin_st_no integer,
		dock_no integer,
		cycle_status boolean
		);


