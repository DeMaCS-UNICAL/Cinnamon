#!/usr/bin/python

#import MySQLdb 
import pyodbc

# Open database connection
#db = MySQLdb.connect("localhost","root","root","TESTDB" )
class DB_Manager:
	
	db = pyodbc.connect("DRIVER={myodbc_mysql}; SERVER=localhost; PORT=3306;DATABASE=cinnamon; UID=root; PASSWORD=root;")

	def insert_Ap(self, record):
		cursor = self.db.cursor()

		# for row in cursor.execute("select access_point_name from APs"):
		# 	print(row.access_point_name)

		try:
			cursor.execute("insert into APs values (?,?,?,?,?,?,?)", record.values())
			self.db.commit()
		except:
			self.db.rollback()


	def update_signal_AP(self, strength, access_point_address):
		cursor = self.db.cursor()
		try:
			cursor.execute("update APs set strength=? where access_point_address=?", strength, access_point_address)
			self.db.commit()
		except:
			print("ROOOOOOLBACK")
			self.db.rollback()


	def exists_AP(self, mac_address):
		cursor = self.db.cursor()
		#sql = "select exists (select 1 from APs where access_point_address = ?)"
		sql = "select * from APs where access_point_address = ?"
		count = cursor.execute(sql, mac_address).rowcount
		#print("MAC: ", mac_address, " ", count)
		if count > 0:
			return True
		return False


	def insert_Packet(self, record):
		cursor = self.db.cursor()
		try:
			cursor.execute("insert into Packets values (?,?,?,?,?,?,?,?,?,?,?)", record.values())
			self.db.commit()
		except:
			self.db.rollback()

	def insert_EAP(self, record):
		cursor = self.db.cursor()
		try:
			cursor.execute("insert into EAP values (?,?,?,?,?,?,?,?,?,?,?)", record.values())
			self.db.commit()
		except:
			self.db.rollback()


if __name__ == "__main__":
	DB_Man = DB_Manager();
	DB_Man.create_table();

	record = {
		'access_point_name': 'abababb',
		'access_point_address': '1234'
		}

	DB_Man.insert_Ap(record)

	# disconnect from server
	DB_Man.db.close()