from flask import Flask,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:12345678@localhost:3306/todo"



db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    createdAt=db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self)->str:
        return f"{self.id}-{self.title}"

@app.route('/', methods=["POST","GET"])
def welcome():
    if request.method=="POST":
        title=request.form['title']
        description=request.form['description']
        print(title,description)
    allTodo=Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/alltodos')
def getAllTodos():
    allTodo=Todo.query.all()
    print(allTodo)
    return "All todos"
    


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug=True)