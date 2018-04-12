import cgi
from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.DateTime)

    def __init__(self, title, body, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date
    
    def __repr__(self):
        return '<Blog %r>' % self.title


def get_old_blogs():
    return Blog.query.all()

@app.route('/blog.html', methods=['POST', 'GET'])
def index():
     
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
         #2 arguments when expecting 1
        return render_template("singlepost.html",
        head_title="My blog", 
        blog_id = blog_id)

    if request.method =="GET":
        if request.args.get('id'):
            id = int(request.args.get('id'))
            blog = Blog.query.filter_by(date).first  
            blog_id = blog.id
            return render_template("singlepost.html",
            head_title="My blog", 
            blog_id = blog_id)
        else:    
            return render_template('blog.html', 
            head_title="My blog", 
            old_posts = get_old_blogs())

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost.html', head_title="New Post")

@app.route('/validate', methods=['POST'])
def validate_data():
    title = request.form["title"]
    body = request.form["body"] 

    title_error=""
    body_error=""

    if not title:   
        title_error = "Please remember to enter a title." 
    if body == "NONE":  #this line isn't working, it did, then I changed it to a textarea. 
        body_error = "Please enter something in the body."      
    if not title_error and not body_error :  #this passes if the strings stay empty
        blog_post = Blog(title, body)
        db.session.add(blog_post)
        db.session.commit()  
        after_submit = Blog.query.filter_by(date).first 
        submitted_id = after_submit.id
         #this line still broken
# instead of rendering blog, render singlepost with the correct id:
        return render_template("singlepost.html",
            head_title="My blog", 
            blog_id = submitted_id)
   
    else:  #it had an error
        return render_template("newpost.html",
            title=title,
            body=body,
            title_error = title_error,
            body_error = body_error
            )  

if __name__ == "__main__":
    app.run()
