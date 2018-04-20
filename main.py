import cgi
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, flash
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

    def __init__(self, title, body, owner_id, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.owner_id = owner_id
    
    def __repr__(self):
        return '<Blog %r>' % self.title

#handle another parameter in new_post?

# set a secret key here! 
app.secret_key = "dsjfhirwbrguakdbufbuwe"

def get_old_blogs():
    return Blog.query.all()

def get_users():
    return User.query.all()

@app.before_request
def require_login():  
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
           
@app.route('/')
def index():         #need to fix database syntax to show authors on index - posibly working now, test in a minute
    user_table = User.query.all()
    return render_template("index.html", user_table = user_table)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    else:  #it was a post request, I need to verify the correct data
        username = request.form["username"]
        password = request.form["password"]

    #I need to query the database  using the user name and password they submitted.   
    #this line needs to get the entire database of user-names
        user_name = User.query.all()

        for user in user_name:  
            if username == user.username:
                stored_id = user.id
                if password == user.password:
                    session['username'] = username
                    return redirect("/newpost")
                else:
                    #return flash message "Password is incorrect"
                   return redirect('/login', flash("Password is incorrect"))
            else:
                #return the flash message "This user name does not exist"
                return redirect('/login', flash("This user name does not exist"))


# signup handler
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
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
            session['username'] = username   
            user = User(username, password)
            db.session.add(user)
            db.session.commit()  
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
    del session['username']
    return redirect('/blog') #Just for me, flash message that "You have been logged out" ?

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST': #you have submitted a form validate it. If good save and render single post
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
       
        title_error=""
        body_error=""
        if not body:  #this line isn't working, it did, then I changed it to a textarea. 
            body_error = "Please enter something in the body."   
        if not title:   
            title_error = "Please remember to enter a title." 
           
        if not title_error and not body_error :  #this passes if the strings stay empty
            blog = Blog(title, body, owner.id)
            db.session.add(blog)
            db.session.commit()  
            after_submit = "/blog?id=" + str(blog.id)    
            return redirect(after_submit)

        else:                                   #it had an error
            return render_template("newpost.html",
                title=title,
                body=body,
                title_error = title_error,
                body_error = body_error
                )     
    
    if request.method =="GET":
        if request.args.get('id'): #how to show single posts from get request
            blog_id = request.args.get('id')
            blog = Blog.query.filter_by(owner_id = blog_id)
            owner = User.query.get(blog_id)
            return render_template("singlepost.html",
            head_title="My blog", 
            blog = blog, owner = owner)           

        if request.args.get('user'): #how to show single posts from a single author get request
            user_id = request.args.get('user')
            blog = Blog.query.get().all.sort_by("date desc")
            
             #this line should get all of the posts from that user_id
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
# so, I need some way to add/commit the owner_id with these posts. 
    user_name = session['username']    #can I get the current username out? 
    return render_template('newpost.html', head_title="New Post", username = user_name)
    


if __name__ == "__main__":
    app.run()

