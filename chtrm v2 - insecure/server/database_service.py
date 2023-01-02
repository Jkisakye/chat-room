import mysql.connector


def connect_database():
    database_connection = mysql.connector.connect(
    host = 'localhost',
    user = 'chat_admin',
    passwd = 'Voldemort77',
    database = 'chatappdb_insecure'
    )

    cursor_object = database_connection.cursor()

    return cursor_object, database_connection

# insert a new user
def register(name, password):
    cursor_object, database_connection = connect_database()
    sql  = "INSERT INTO user (username, password) Values('%s', '%s')" % (name, password)

    cursor_object.execute(sql)
    database_connection.commit()

    print(f'user id: {cursor_object.lastrowid} inserted')
    database_connection.close()
    return cursor_object.lastrowid #return user id



def verify_user(username, password):
    cursor_object, database_connection = connect_database()
    query = "SELECT username, userid FROM user WHERE username = '%s' AND password = '%s'" % (username, password)
    cursor_object.execute(query)
    result = cursor_object.fetchall()

    database_connection.close()
    if not result: #list of tuples is empty  NB: might not work on numpy arrays, must be explicit there
        return False
    else:
        return True

#search if username exists in database
def search_user(username):
    cursor_object, database_connection = connect_database()
    query = "SELECT userid FROM user WHERE username = '%s'" % (username)
    cursor_object.execute(query)
    result = cursor_object.fetchone()
    database_connection.close()
    if result:
        return result
    else:
        return False



