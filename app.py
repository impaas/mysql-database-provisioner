import json
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.rdbms.mysql_flexibleservers import MySQLManagementClient
from azure.mgmt.rdbms.mysql_flexibleservers.models import Server, ServerVersion
from flask import Flask, request
import adal
import pymysql
from msrestazure.azure_active_directory import AADTokenCredentials


def authenticate_username_password():
    """
    Authenticate using user w/ username + password.
    This doesn't work for users or tenants that have multi-factor authentication required.
    """
    authority_host_uri = "https://login.microsoftonline.com"
    tenant = "2b897507-ee8c-4575-830b-4f8267c3d307"
    authority_uri = authority_host_uri + "/" + tenant
    resource_uri = "https://management.core.windows.net/"
    username = "adminServerUser"
    password = "This_is_our_flexible_server!"
    client_id = "a8e6877c-314a-462d-94f6-5e73d80bb153"

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    mgmt_token = context.acquire_token_with_username_password(
        resource_uri, username, password, client_id
    )
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials


app = Flask(__name__)


# Acquire a credential object using CLI-based authentication.
credential = authenticate_username_password()

# Retrieve subscription ID from environment variable
subscription_id = "eb4736f9-8c8a-4296-9e7e-7b3365ecac1a"

# Constants we need in multiple places: the resource group name and the region
# in which we provision resources. You can change these values however you want.
RESOURCE_GROUP_NAME = "impaas-prod_group"
LOCATION = "uksouth"

# Step 1: Provision the resource group.
resource_client = ResourceManagementClient(credential, subscription_id)


# We use a random number to create a reasonably unique database server name.
# If you've already provisioned a database and need to re-run the script, set
# the DB_SERVER_NAME environment variable to that name instead.
#
# Also set DB_USER_NAME and DB_USER_PASSWORD variables to avoid using the defaults.
"""
db_admin_name = os.environ.get("DB_ADMIN_NAME", "adminServerUser")
db_admin_password = os.environ.get("DB_ADMIN_PASSWORD", "This_is_our_flexible_server!")

mysql_client = MySQLManagementClient(credential, subscription_id)

poller = mysql_client.databases.begin_create_or_update(RESOURCE_GROUP_NAME,
    "tsuru-flexible-db", "dummy database name", {})

db_result = poller.result()
"""

# @app.route("/resources/plans", methods=["GET"])
# def plans():
#     plans = [
#         {"name": "small", "description": "small instance"},
#         {"name": "medium", "description": "medium instance"},
#         {"name": "big", "description": "big instance"},
#         {"name": "giant", "description": "giant instance"},
#     ]
#     return json.dumps(plans)


# @app.route("/resources", methods=["POST"])
# def add_instance():
#     name = request.form.get("name")
#     plan = request.form.get("plan")
#     team = request.form.get("team")
#     # use the given parameters to create the instance

#     return "", 201


# @app.route("/resources/<name>/bind-app", methods=["POST"])
# def bind_app(name):
#     app_host = request.form.get("app-host")
#     # use name and app_host to bind the service instance and the #
#     application
#     envs = {"SOMEVAR": "somevalue"}
#     return json.dumps(envs), 201


# @app.route("/resources/<name>/bind-app", methods=["DELETE"])
# def unbind_app(name):
#     app_host = request.form.get("app-host")
#     # use name and app-host to remove the bind
#     return "", 200


# @app.route("/resources/<name>", methods=["DELETE"])
# def remove_instance(name):
#     # remove the instance named "name"
#     return "", 200


# @app.route("/resources/<name>/bind", methods=["POST", "DELETE"])
# def access_control(name):
#     app_host = request.form.get("app-host")
#     unit_host = request.form.get("unit-host")
#     # use unit-host and app-host, according to the access control tool, and
#     # the request method.
#     return "", 201


# @app.route("/resources/<name>/status", methods=["GET"])
# def status(name):
#     # check the status of the instance named "name"
#     return "", 204


if __name__ == "__main__":
    app.run()
