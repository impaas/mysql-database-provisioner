import json
import pymysql
import random
import string
from flask import Flask, request

app = Flask(__name__)
hostname = '20.117.188.21'

@app.route("/resources/plans", methods=["GET"])
def plans():
    plans = [{"name": "small", "description": "small instance"}]
    return json.dumps(plans)


@app.route("/resources", methods=["POST"])
def add_instance():
    name = request.form.get("name")
    plan = request.form.get("plan")
    team = request.form.get("team")
    # use the given parameters to create the instance
    conn = pymysql.connect(host=hostname,
                       user='root',
                       password='rootmysqltsuru')
    cursor = conn.cursor()

    #create database
    new_database_name = name
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {new_database_name}"
    cursor.execute(create_database_query)

    conn.commit()
    cursor.close()
    conn.close()
    return "", 201


@app.route("/resources/<name>/bind-app", methods=["POST"])
def bind_app(name):

    # name: name of instance (and name of database)
    # app_name
    # : name of app

    app_name = request.form.get("app-name")
    
    conn = pymysql.connect(host=hostname,
                    user='root',
                    password='rootmysqltsuru')
    cursor = conn.cursor()

    # create specific db user
    new_username = name + app_name
    new_user_password = app_name + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    create_user_query = f"CREATE USER '{new_username}'@'localhost' IDENTIFIED BY '{new_user_password}'"
    cursor.execute(create_user_query)
    
    ## Grant privileges to the new user on the new database
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON {name}.* TO '{new_username}'"
    cursor.execute(grant_privileges_query)

    envs = {"SOMEVAR": "somevalue",
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
    app_name = request.form.get("app-name")
    
    conn = pymysql.connect(host=hostname, user="root", password="rootmysqltsuru")

    cursor = conn.cursor()

    # Delete user
    user_to_delete = name + app_name
    delete_user_query = f"DROP USER IF EXISTS '{user_to_delete}'"
    cursor.execute(delete_user_query)

    conn.commit()
    cursor.close()
    conn.close()
    
    return "", 200


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
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
    return "", 200


@app.route("/resources/<name>/bind", methods=["POST", "DELETE"])
def access_control(name):
    app_host = request.form.get("app-host")
    unit_host = request.form.get("unit-host")
    # use unit-host and app-host, according to the access control tool, and
    # the request method.
    #TODO
    return "", 201


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    # check the status of the instance named "name
    # TODO
    return "", 204

if __name__ == "__main__":
    app.run()