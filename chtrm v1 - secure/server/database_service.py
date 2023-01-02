import mysql.connector


def connect_database():
    database_connection = mysql.connector.connect(
    host = 'localhost',
    user = 'chat_admin',
    passwd = 'Voldemort77',
    database = 'chatappdb'
    )

    cursor_object = database_connection.cursor()

    return cursor_object, database_connection

# insert a new user
def register(name, password):
    cursor_object, database_connection = connect_database()
    sql  = 'INSERT INTO user (username, password) Values(%s, %s)'
    val = (name, password)

    cursor_object.execute(sql, val)
    database_connection.commit()

    print(f'user id: {cursor_object.lastrowid} inserted')
    database_connection.close()
    return cursor_object.lastrowid #return user id


#save salt
def save_salt(userid, salt):
    cursor_object, database_connection = connect_database()
    sql  = 'INSERT INTO salt (userid, salt) Values(%s, %s)'
    val = (userid, salt)

    cursor_object.execute(sql, val)
    database_connection.commit()

    # print(f'user id salt: {cursor_object.lastrowid} inserted')
    database_connection.close()

#secure way against sql injections
def verify_user(username, password):
    cursor_object, database_connection = connect_database()
    query = 'SELECT username, userid FROM user WHERE username = %s AND password = %s'
    val = (username, password)
    cursor_object.execute(query, val)
    result = cursor_object.fetchall()

    database_connection.close()
    if not result: #list of tuples is empty  NB: might not work on numpy arrays, must be explicit there
        return False
    else:
        return True

#search if username exists in database
def search_user(username):
    cursor_object, database_connection = connect_database()
    query = 'SELECT userid FROM user WHERE username = %s'
    val = (username, )
    cursor_object.execute(query, val)
    result = cursor_object.fetchone()
    database_connection.close()
    if result:
        return result
    else:
        return False

#search for salt in database
# The salts are stored in the same rows with the ids of the users that created them
def search_salt(userid):
    userid = int(userid[0]) #the function is called with the id as a tuple, the user id is [0]
    cursor_object, database_connection = connect_database()
    query = 'SELECT salt FROM salt WHERE userid = %s'
    val = (userid, )
    cursor_object.execute(query, val)
    result = cursor_object.fetchone()

    database_connection.close()
    if result: #function can only return a result that isn't a None type
        return result[0]


