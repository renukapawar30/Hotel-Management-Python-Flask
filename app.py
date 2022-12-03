
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_mail import Mail, Message




app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'email' in request.form and 'phone' in request.form and 'adults' in request.form and 'children' in request.form and 'check_in' in request.form and 'check_out' in request.form and 'rooms' in request.form and 'message' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        adults = request.form['adults']
        children = request.form['children']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        rooms = request.form['rooms']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM booking WHERE fname = % s', (fname, ))
        booking = cursor.fetchone()
        if booking:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', fname):
            msg = 'Firstname must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', lname):
            msg = 'Lastname must contain only characters and numbers !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'(0|91)?[6-9][0-9]{9}', phone):
            msg = 'Enter a valid phone number !'
        elif not fname or not lname or not email or not phone or not adults or not children or not check_in or not check_out or not rooms or not message:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO booking VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s,% s,% s)',
                           (fname, lname, email, phone, adults, children, check_in, check_out, rooms, message, ))
            mysql.connection.commit()
            msg = 'You have successfully booked the room !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("booking.html", msg=msg)


def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM booking ')
        b = cursor.fetchall()
        return render_template("booking.html")
    return redirect(url_for('login'))

@app.route('/reservation')
def reservation():
    return render_template("reservation.html")


@app.route('/navbar')
def navbar():
    return render_template('navbar.html')


@app.route('/index')
def index():
    msg = ''
    return render_template('index.html', msg=msg)


@app.route("/booking")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM booking ')
        b = cursor.fetchall()
        return render_template("booking.html")
    return redirect(url_for('login'))


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pawarrenukplanet30@gmail.com'
app.config['MAIL_PASSWORD'] = 'apyxoatdtcamtfuj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app)


@app.route("/contact" , methods =['GET','POST'])
def contact():
    msg = ''
    if request.method=='POST' and 'fname' in request.form and 'email' in request.form and 'phone' in request.form and 'subject' in request.form:
        fname=request.form['fname']
        email=request.form['email']
        phone=request.form['phone']
        subject=request.form['subject']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM contact WHERE fname = % s',(fname,))
        contact=cursor.fetchone()

        if contact:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', fname):
            msg = 'Firstname must contain only characters and numbers !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'(0|91)?[6-9][0-9]{9}', phone):
            msg = 'Enter a valid phone number !'
        elif not fname or  not email or not phone or not subject:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO contact VALUES (NULL, % s, % s, % s, % s)',
                           (fname,  email, phone, subject, ))
            mysql.connection.commit()
            msg = Message('Hello', sender = 'pawarrenukplanet30@gmail.com', recipients = ['renukapawar528@gmail.com'])
            msg.html = "Contact form submitted with data: \n\nName: {} \n\nE-mail: {}\n\nPhone: {} \n\nSubject: {}".format(fname, email, phone,subject)
            mail.send(msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("contact.html", msg=msg)



if __name__ == '__main__':

    app.run(debug=True)
