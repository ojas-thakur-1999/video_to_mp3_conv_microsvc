import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# setting config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    credentials = request.authorization
    if not credentials:
        return "missing credentials", 401

    # check if user exists in auth.users table
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT username, password, is_admin FROM users WHERE username = %s", (credentials.username, )
    )

    if res > 0:
        user_row = cur.fetch_one()
        username = user_row[0]
        password = user_row[1]
        is_admin = user_row[2]

        if credentials.username != username or credentials.password != password:
            return "invalid credentials", 403
        else:
            return createJWT(credentials.username, os.environ.get("JWT_SECRET"), is_admin)

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithm=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200

def createJWT(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "is_admin": is_admin
        },
        secret,
        algorithm="HS25"
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)