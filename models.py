from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Todo(db.Model):
    todo_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    completed=db.Column(db.Boolean,default=False)
    user_id=db.Column(db.Integer,unique=True)
    
    def __repr__(self):
        return f"<Todo {self.title}>"
    
class User(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    email = db.Column(db.String(120),unique=True)
    password= db.Column(db.String(20))
    