import cgi
from datetime import datetime

from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:l@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
         self.username = username
         self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date
    
    def __repr__(self):
        return '<Blog %r>' % self.title

#handle another parameter in new_post?
#TODO create a session
#TODO set a secret key here! 

def get_old_blogs():
    return Blog.query.all()

@app.before_request()
    def require_login():
        #allowed_routes 'login', 'blog', 'index', 'signup' #these are the function names NOT the handler names
        #request.endpoint()   is the name of the function not the url path
        #if the user is trying to go anywhere else, and not logged in    ....if user not in session:
        return redirect('/login')
           
@app.route('/')
def index(): 
    return render_template("index.html", get_old_blogs())

@app.route('/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
#right here I need to query the database  using the user name and password they submitted.    
    user-names = User.request #this line needs to get the entire database of user-names

    if username not in #databaseObject.username:
        #return the flash message "This user name does not exist"
    if password not in #databaseObject.password:
        #return flash message "Password is incorrect"

        #how to make sure they were in the same entry in the database? A loop that checks one entry at a time?
    if #it actually is a match in the database:
       #TODO store their user name in the session 
        return redirect("/newpost")


# signup handler
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    verifypass = request.form["verifypass"] 

    username_error=""
    password_error =""
    verifypass_error =""

    #I may change this to flash messages
    #if they leave it blank the message is supposed to read "One or more fields are invalid"
    #if password and verifypass are different "Passwords do not match"
    #if len(username) <3:   Username invalid, too short
    #if len(password) <3:   Password


    if not username:   
        username_error = "Please enter a username." 
    elif len(username) < 3:
        username_error = "Must be more than 3 characters."       
    else:
        username = username

    if not password:   
        password_error = "Please enter a password."  
        password = ""
    elif len(password) < 3:
        password_error = "Must be more than 3 characters."       
        password = ""
    else:
        password = password
    
    if not verifypass:   
        verifypass_error = "Please enter a verify password." 
        verifypass = ""   
    elif password != verifypass:
        verifypass_error = "Password and verify password must be the same."       
        verifypass = ""
    else:
        verifypass = verifypass
        
    if not username_error and not password_error and not verifypass_error:  #this passes if the strings stay empty
       #TODO store their user name in the session 
        return redirect("/newpost")
    
    else:  #it had an error
        return render_template("signup.html", 
            username=username,
            username_error=username_error,
            password_error=password_error,
            verifypass_error=verifypass_error,
            )  
#This is the end of of the User-signin

@app.route('/logout')
def logout():
    #delete username from session
    return redirect('/blog') #Just for me, flash message that "You have been logged out" ?

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST': #you have submitted a form validate it. If good save and render single post
        title = request.form['title']
        body = request.form['body']
        title_error=""
        body_error=""
        if body == "                ":  #this line isn't working, it did, then I changed it to a textarea. 
            body_error = "Please enter something in the body."   
        if not title:   
            title_error = "Please remember to enter a title." 
           
        if not title_error and not body_error :  #this passes if the strings stay empty
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()  
            after_submit = "/blog?id=" + str(blog.id)    #stored here, not using it
            return redirect(after_submit)

        else:  #it had an error
            return render_template("newpost.html",
                title=title,
                body=body,
                title_error = title_error,
                body_error = body_error
                )     
    
    if request.method =="GET":
        if request.args.get('id'): #how to show single posts from get request
            blog_id = request.args.get('id')
            blog = Blog.query.get(blog_id)
            return render_template("singlepost.html",
            head_title="My blog", 
            blog = blog)

        if request.args.get('user'): #how to show single posts from a single author get request
            user_id = request.args.get('user')
            blog = Blog.query.get(user_id)  #this line should get all of the posts from that user_id
            #is there away right here to sort by date as the blog object is created?
            return render_template("singlepost.html",
            head_title="My blog", 
            blog = blog)

        else:    #I showed up for the first time- working
            return render_template('blog.html', 
            head_title="My blog", 
            old_posts = get_old_blogs())

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost.html', head_title="New Post")
    


if __name__ == "__main__":
    app.run()

