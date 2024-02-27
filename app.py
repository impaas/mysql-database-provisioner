import os
import json
import pymysql
import random
import string
import base64
from flask import Flask, request

app = Flask(__name__)
hostname = '20.117.188.21'
username_required = "mysqlrootuser"
password_required = "nthbqHOcF3tQM6K"

@app.route("/resources/plans", methods=["GET"])
def plans():
    plans = [{"name": "Database", "description": "A MySQL database instance"}]
    return json.dumps(plans)


@app.route("/resources", methods=["POST"])
def add_instance():

    # Extracting password from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Basic '):
        encoded_credentials = auth_header[len('Basic '):]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        print("\nUsername:", username)
        print("Password:", password)
	if username != username_required or password != password_required:
		return "Incorrect credentials provided\n", 400


    # Printing request body
    print("\nRequest Body:")
    print(request.get_data(as_text=True))


    name = request.form.get("name")
    # use the given parameters to create the instance
    conn = pymysql.connect(host=hostname,
                       user='root',
                       password='rootmysqltsuru')
    cursor = conn.cursor()

    #create database
    if not name:
        return "Name not provided\n", 400
    # TODO: Error handling; check if database already exists
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {name}"
    print(create_database_query)
    cursor.execute(create_database_query)

    conn.commit()
    cursor.close()
    conn.close()
    return f"The Database: {name} has been created!", 201


@app.route("/resources/<name>/bind-app", methods=["POST"])
def bind_app(name):
        # Extracting password from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Basic '):
        encoded_credentials = auth_header[len('Basic '):]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        print("\nUsername:", username)
        print("Password:", password)
        if username != username_required or password != password_required:
                return "Incorrect credentials provided\n", 400
    # use name and app-name to bind the service instance and the 
    # application
    app_name = request.form.get("app-name")
    if not app_name:
        return "No app-name provided\n", 400
    
    conn = pymysql.connect(host=hostname,
                    user='root',
                    password='rootmysqltsuru')
    cursor = conn.cursor()

    # create specific db user
    new_username = name + app_name
    new_username = new_username[:31]
    new_user_password = app_name + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    create_user_query = f"CREATE USER '{new_username}'@'%' IDENTIFIED BY '{new_user_password}'"
    cursor.execute(create_user_query)
    
    ## Grant privileges to the new user on the new database
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON {name}.* TO '{new_username}'"
    cursor.execute(grant_privileges_query)

    envs = {
    "MYSQL_PORT" : "3306",
    "MYSQL_PASSWORD": new_user_password,
    "MYSQL_USER": new_username,
    "MYSQL_HOST": hostname,
    "MYSQL_DATABASE_NAME": name
    }

    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps(envs), 201


@app.route("/resources/<name>/bind-app", methods=["DELETE"])
def unbind_app(name):
        # Extracting password from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Basic '):
        encoded_credentials = auth_header[len('Basic '):]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        print("\nUsername:", username)
        print("Password:", password)
        if username != username_required or password != password_required:
                return "Incorrect credentials provided\n", 400
    app_name = request.form.get("app-name")
    if not app_name:
        return "No app-name provided\n", 400

    conn = pymysql.connect(host=hostname, user="root", password="rootmysqltsuru")

    cursor = conn.cursor()

    # Delete user
    user_to_delete = name + app_name
    delete_user_query = f"DROP USER IF EXISTS '{user_to_delete}'"
    cursor.execute(delete_user_query)

    conn.commit()
    cursor.close()
    conn.close()
    
    return f"{user_to_delete} has been removed; application unbound", 200


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
        # Extracting password from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Basic '):
        encoded_credentials = auth_header[len('Basic '):]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        print("\nUsername:", username)
        print("Password:", password)
        if username != username_required or password != password_required:
                return "Incorrect credentials provided\n", 400

    # remove the instance named "name"
    # Delete database
    conn = pymysql.connect(host=hostname, user="root", password="rootmysqltsuru")
    cursor = conn.cursor()

    database_to_delete = name
    delete_database_query = f"DROP DATABASE IF EXISTS {database_to_delete}"
    cursor.execute(delete_database_query)

    conn.commit()
    cursor.close()
    conn.close()
    return f"Database: {name} has been deleted", 200


@app.route("/resources/<name>/bind", methods=["POST", "DELETE"])
def access_control(name):
    # app_host = request.form.get("app-host")
    # unit_host = request.form.get("unit-host")
    # use unit-host and app-host, according to the access control tool, and
    # the request method.
    #TODO
    return "Server does not support this operation", 400


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
#     # check the status of the instance named "name
#     # TODO
    return "Server does not support this operation", 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 4999)))
