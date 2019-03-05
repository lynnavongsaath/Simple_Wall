from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UpperCasePassword_REGEX=re.compile(r'^(?=.*?[A-Z])')
NumericValue_REGEX=re.compile(r'^(?=.*?[0-9])')
app.secret_key = 'asdlkfj34tu-n;42no0[ekjhavea-9248n'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # first name validation
    if len(request.form['first_name']) < 1:
        flash("Required", "first_name")
    elif request.form['first_name'].isalpha()==False:
        flash("First name cannot contain numbers","first_name")
    elif len(request.form['first_name']) > 25:
        flash("First name is too long!", "first_name")
    session['first_name'] = request.form['first_name']
    
    # last name validation
    if len(request.form['last_name']) < 1:
        flash("Required", "last_name")
    elif request.form['last_name'].isalpha()==False:
        flash("Last name cannot contain numbers", "last_name")
    elif len(request.form['last_name']) > 30:
        flash("Last name is too long!", "last_name")
    session['last_name'] = request.form['last_name']
    
    # email validation
    if len(request.form['email']) < 1:
        flash("Required", "email")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", "email")
    session['email'] = request.form['email']
    
    # password validation
    if len(request.form['password']) < 1:
        flash("Required", "password")
    elif len(request.form['password']) < 8 or len(request.form['password']) > 15:
        flash("Password must be between 8-15 characters long", "password")
    elif not UpperCasePassword_REGEX.match(request.form['password']):
        flash("Must contain at least one uppercase letter", "password")
    elif not NumericValue_REGEX.match(request.form['password']):
        flash("Must contain at least one number", "password")
        
    # confirm password
    if request.form['password'] != request.form['confirm_pw']:
        flash("Password must match", "confirm_pw")
    
    # checking to see if anyone has logged in with the same email 
    mysql = connectToMySQL("simple_wall")
    exists_query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        'email': request.form['email']
    }
    users_list = mysql.query_db(exists_query, data)
    if len(users_list) > 0:
        flash("Email already in use", "email")

    # if there are any flashes (errors) then redirect to '/'
    if '_flashes' in session.keys():
        return redirect('/')
    else:
    # if there are no flashes & errors, then add the user into the database
        pw_hash = bcrypt.generate_password_hash(request.form['password'])

        mysql = connectToMySQL("simple_wall")
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(hashed_pw)s, NOW(), NOW())"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'hashed_pw': pw_hash
        }
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id
        flash("You have successfully registered!", "register")        
        return redirect('/home')
        
@app.route('/login', methods=['POST'])
def login():
    # checking to see if the email entered for the login is in the database
    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        'email': request.form['email']
    }
    mysql = connectToMySQL("simple_wall")
    users_list = mysql.query_db(query, data)
    
    # the users_list will return a list containing that email
    if len(users_list) > 0:
        user = users_list[0]
        # checking to see if the pw matches
        if bcrypt.check_password_hash(user['password'], request.form['password']):
            session['user_id'] = user['id']
            return redirect('/home')
    flash("Invalid email or password", "login")
    return redirect('/')

@app.route('/home')
def home():
    # a user_id must be in session in order to access the home page
    if 'user_id' not in session:
        return redirect('/')
    
    if session['user_id']:
        # getting infomation from current user; so all their messages are displayed
        mysql = connectToMySQL("simple_wall")
        query = "SELECT users2.first_name AS message_to, messages.id, messages.content, users.first_name AS message_from FROM messages LEFT JOIN users ON users.id = messages.messager_id LEFT JOIN users AS users2 ON users2.id = messages.messagee_id WHERE messages.messagee_id = %(user_id)s"
        data = {
            'user_id':session['user_id']
        }
        current_user = mysql.query_db(query,data)

        # this is to get the name of the user id from the database to be displayed on the home page
        mysql = connectToMySQL("simple_wall")
        user_query = "SELECT first_name FROM users WHERE id = %(user_id)s"
        matching_users = mysql.query_db(user_query, data)
        user = matching_users[0]

        #number of messages that belongs to the user
        mysql = connectToMySQL("simple_wall")
        msg_query = "SELECT COUNT(messages.content) AS num_msg FROM messages LEFT JOIN users ON users.id = messages.messager_id WHERE messages.messagee_id = %(user_id)s GROUP BY messages.messagee_id;"
        num_msg = mysql.query_db(msg_query, data)
        if num_msg is IndexError:
            num_messages = 0
        else:
            num_messages = num_msg[0]['num_msg']
        
        # name of all the registered users
        mysql = connectToMySQL("simple_wall")
        users_list_query = "SELECT id, first_name FROM users WHERE id != %(user_id)s"
        all_users_name = mysql.query_db(users_list_query, data)

    return render_template('home.html', name=user['first_name'], user_msg=current_user, all_users=all_users_name, num_of_msg=num_messages)

@app.route('/send_msg/<messagee_id>', methods=['POST'])
def newmsg(messagee_id):
    # insert a message into database with to the correct user
    mysql = connectToMySQL("simple_wall")
    newmsg_query = "INSERT INTO messages (messager_id, messagee_id, content, created_at, updated_at) VALUES ('%(messager_id)s', %(messagee_id)s, %(message)s, NOW(), NOW())"
    data = {
        'messager_id': session['user_id'],
        'messagee_id': messagee_id,
        'message': request.form['msg_tosend']
    }
    new_msg_id = mysql.query_db(newmsg_query, data)

    return redirect('/home')

@app.route('/delete/<delete_msgr_id>', methods=['POST'])
def delete(delete_msgr_id):
    mysql = connectToMySQL("simple_wall")
    deletemsg_query = "DELETE FROM messages WHERE messages.id = %(delete_msg_id)s"
    data = {
        'delete_msg_id': delete_msgr_id
    }
    delete_msg = mysql.query_db(deletemsg_query, data)
    print(delete_msg)
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    flash("You are successfully logged out", "logout")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)