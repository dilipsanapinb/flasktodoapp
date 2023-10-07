from flask import Flask,request,jsonify,render_template, redirect
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

@app.route('/', methods=["GET"])
def welcome():
    allTodo=Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

# add todo
@app.route('/add', methods=["POST","GET"])
def addTodos():
    if request.method=="POST":
        title=request.form['title']
        description=request.form['description']
        todo=Todo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    else:
        return "Use POST method to add a new todo"


# update todo
@app.route('/update/<int:id>',methods=["POST","GET"])
def updateTodo(id):
    todo=Todo.query.get(id)
    if request.method=="POST":
        title=request.form['title']
        description=request.form['description']
        # todo=Todo.query.filter_by(id=id).first()
        todo.title=title
        todo.description=description
        # db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return  render_template('update.html',todo=todo)



# delete todo
@app.route('/delete/<int:id>')
def deleteTodo(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug=True)