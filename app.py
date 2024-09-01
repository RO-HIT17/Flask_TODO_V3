from flask import redirect,url_for,render_template,request,Flask
from models import db,Todo,User

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#@app._got_first_request
#def create_tables():
#    db.create_all()
    
with app.app_context():
    db.create_all()
    
    
@app.route('/register', methods=['GET','POST'])
def register_user():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    new_user=User(name=name,email=email,password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))
#Own Function
@app.route('/clear')
def clear_all():
    todo_lst=Todo.query.all()
    for i in todo_lst:
        if i.completed == True:
            db.session.delete(i)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)