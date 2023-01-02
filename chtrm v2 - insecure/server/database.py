#script to be run only when setting up the server

import mysql.connector

#note: The database and user were created natively in mysql
database_connection = mysql.connector.connect(
    host = 'localhost',
    user = 'chat_admin',
    passwd = 'Voldemort77',
    database = 'chatappdb_insecure'
    )

cursor_object = database_connection.cursor()

#users table
user_table = '''
                CREATE TABLE user(
                    userid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(250) NOT NULL,
                    password VARCHAR(500) NOT NULL
                )
             '''
cursor_object.execute(user_table)

# #user salt table
# salt_table = '''
#                 CREATE TABLE salt(
#                     userid INT NOT NULL PRIMARY KEY,
#                     salt VARCHAR(500) NOT NULL
#                 )
#              '''
# cursor_object.execute(salt_table)

#change the database charachter encoding to utf8 to match the encoding used by the hashing functions
cursor_object.execute('ALTER DATABASE chatappdb_insecure CHARACTER SET utf8 COLLATE utf8_unicode_ci;')

database_connection.close()