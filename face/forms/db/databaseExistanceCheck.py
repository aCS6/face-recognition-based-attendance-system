import mysql.connector as mysql

def tableExist():
	#table check if existed
	connection = mysql.connect(host="localhost",user="root",password="pass",database="student")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='std'")
	tablesInfo =  cursor.fetchall()
	if len(tablesInfo)!=0:
		print(tablesInfo) #table Exist
	else:
		print("Table Not Exist")
		cursor.execute(" CREATE TABLE `student`.`std` (`id` INT NOT NULL,`name` VARCHAR(255) NULL,`phone` VARCHAR(255) NULL,`email` VARCHAR(255) NULL,`photo` VARCHAR(45) NULL,PRIMARY KEY (`id`)) ")
		print("Table Created")

try:
	connection = mysql.connect(host="localhost",user="root",password="pass")
	cursor = connection.cursor()
	cursor.execute("SHOW DATABASES LIKE 'student' ")
	row = cursor.fetchall()
	if len(row)!=0:
		print(row) #database exists
		tableExist()
	else:
		print("Database Not Exist")
		cursor.execute("CREATE DATABASE student")
		print("Database Created")
		## create table in the database
		cursor.execute(" CREATE TABLE `student`.`std` (`id` INT NOT NULL,`name` VARCHAR(255) NULL,`phone` VARCHAR(255) NULL,`email` VARCHAR(255) NULL,`photo` VARCHAR(45) NULL,PRIMARY KEY (`id`)) ")
		print("Table created at new database.")

except mysql.ProgrammingError as e:
	if "Unknown database" in str(e):
		print("Database not found")
	elif "Access denied" in str(e):
		print("Username or password is invalid")
	else:
		print(e)

except mysql.InterfaceError as e:
	print("Connection not Established")




	

