from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
app = Flask(__name__)

# This is all for database connentivity ....from here to 

# adding configuration for using a sqlite database (to connect DB with flask)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 

# to enable or disable tracking modifications of objects
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance / initialize the app with the extension
db = SQLAlchemy(app)
app.app_context().push()


# here 

class Todo(db.Model):
    srno=db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow )

  # repr method represents how one object of this datatable
    # will look like
    def __repr__(self) ->str:
        return f"{self.srno}-{self.title}"

# from app import db
# db.create_all()



@app.route('/',methods=["GET","POST"])
def home():
    if request.method=="POST":
        title= request.form['title']
        desc= request.form['desc']

        todo=Todo(title = title , desc = desc)

        db.session.add(todo)
        db.session.commit()
    allTodo= Todo.query.all()
    # print(allTodo)
    return render_template("index.html",allTodo=allTodo)
    

@app.route('/show')
def products():
    # allTodo= Todo.query.all()
    # print(allTodo) #this is print todo text in terminal using __repr__method when we use in browser /show after  http://127.0.0.1:8000/show
    return 'This is product..!'  

@app.route('/update/<int:srno>',methods=["GET","POST"])
def update(srno):
     if request.method=="POST":
        title= request.form['title']
        desc= request.form['desc']

        todo= Todo.query.filter_by(srno=srno).first()
        todo.title=title
        todo.desc=desc

        db.session.add(todo)
        db.session.commit()
        return redirect("/")

     allTodo= Todo.query.filter_by(srno=srno).first()

     return render_template("update.html",allTodo=allTodo)

@app.route('/delete/<int:srno>')
def delete(srno):
    allTodo= Todo.query.filter_by(srno=srno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")
  

if __name__=='__main__':
    app.run(debug=True,port=8000)