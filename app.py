from flask import Flask, render_template, request, make_response
from flask_mysqldb import MySQL
import yaml
import base64

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        detail = request.form
        username = detail['username']
        password = detail['password']
        enc_password = base64.b64decode(password).decode('utf-8')
        cur = mysql.connection.cursor()
        result = cur.execute("select * from login where username='%s' and password='%s'" % (username, enc_password))
        mysql.connection.commit()
        cur.close()
        if result > 0:
            resp = make_response(render_template("index.html"))
            resp.set_cookie(username, password)
            return resp
        return render_template('login.html')
    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def index():
    valid = len(request.cookies.get("shivam"))
    if valid > 0:
        if request.method == 'POST':
            userDetails = request.form
            name = userDetails['name']
            email = userDetails['email']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name,email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()
            return 'added_to_database'
        return render_template('index.html')
    else:
        return render_template("login.html")


@app.route('/users', methods=['GET'])
def users():
    valid = len(request.cookies.get("shivam"))
    if valid > 0:
        cur = mysql.connection.cursor()
        resultSet = cur.execute("SELECT * from users")
        if resultSet > 0:
            usersDetails = cur.fetchall()
            return render_template('index.html', usersDetails=usersDetails)
    else:
        return render_template("login.html")


@app.route('/delete', methods=['POST'])
def delete():
    valid = len(request.cookies.get("shivam"))
    if valid > 0:
        userDetails = request.form
        name = userDetails['delname']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE name = '%s'" % (name))
        mysql.connection.commit()
        cur.close()
        return render_template('index.html')
    else:
        return render_template("login.html")


@app.route('/update', methods=['POST'])
def update():
    valid = len(request.cookies.get("shivam"))
    if valid > 0:
        userDetails = request.form
        oldname = userDetails['oldname']
        newname = userDetails['updatename']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users set name='%s' WHERE name = '%s'" % (newname, oldname))
        mysql.connection.commit()
        cur.close()
        return render_template('index.html')
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
