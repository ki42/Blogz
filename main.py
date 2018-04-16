import cgi
from datetime import datetime

from flask import Flask, redirect, render_template, request, session
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

        else:    #I showed up for the first time- working
            return render_template('blog.html', 
            head_title="My blog", 
            old_posts = get_old_blogs())

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost.html', head_title="New Post")
    


if __name__ == "__main__":
    app.run()

