import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pass",
    database="school"
)

cursor = con.cursor()

#make a function to access the db
def user_login(tup):
    try:
        cursor.execute("SELECT * FROM `users` WHERE `user`=%s AND `pass`=%s",tup)
        return (cursor.fetchone())
    except:
        return False