from flask import redirect,url_for,render_template,request,Flask
from models import db,Todo,User
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 
   
with app.app_context():
    db.create_all()
    
@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login(): 
    user_email=request.form.get('username') 
    password=request.form.get('password')
    result = User.query.filter_by(email=user_email).first()
    if result:
        passkey= result.password
        user_id=result.user_id
        if passkey==password:
            return redirect(url_for('index',user_id=user_id)) 
        else:
            error="Invalid Password"    
            return render_template('login.html' , error_message=error)
    else:
        error="Username not registered"
        return render_template('login.html' , error_message=error)
        
@app.route('/new')
def register():
    return render_template('register.html',val=0)

@app.route('/forgot')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    data=User.query.filter_by(user_id=user_id).first()
    todolist1 = Todo.query.filter_by(user_id=user_id).all()
    todolist2 = Todo.query.filter_by(user_id=user_id).filter_by(completed=True).all()
    todolist3 = Todo.query.filter_by(user_id=user_id).filter_by(completed=False).all()
    tasks=len(todolist1)
    comp=len(todolist2)
    if tasks!=0:
        per=(comp*100)//tasks 
    else:
        per=0
    #print(todolst,tasks)
    return render_template('dashboard.html',data=data,len=tasks,com=comp,comdata=todolist2,per=per,todolist3=todolist3)

@app.route('/reset' , methods=['POST'])
def reset_password():
    email=request.form.get('email')
    new_password=request.form.get('newpassword')
    update=User.query.filter_by(email=email).first()
    if update:
        update.password=new_password
        db.session.commit()
        return render_template('forgot_password.html', message="Password Changed Successfully",val=1)
    else:
        error="Username not registered"
        return render_template('forgot_password.html', er_message=error,val=1)

@app.route('/register', methods=['GET','POST'])
def register_user():
    fname=request.form.get('fname')
    lname=request.form.get('lname')
    email=request.form.get('email')
    password=request.form.get('password')
    phone=request.form.get('phone')
    confirm_pass=request.form.get('confirm_pass')
    
    if password==confirm_pass:
        result = User.query.filter_by(email=email).first()
        if not result:
            new_user=User(fname=fname,lname=lname,email=email,phone=phone,password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('register.html' , disp_message="Registered Successfully" , val=1)
        else:
            return render_template('register.html' , error_message="User Already Exists",val=1)
    else:
        return render_template('register.html' , error_message="Password Didn't Match",val=0)

@app.route('/index/<int:user_id>')
def index(user_id):
    todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).all()
    return render_template('index.html', todos=todos,user_id=user_id)

@app.route('/filter/<int:user_id>',methods=['POST'])
def filter(user_id):
    priority=request.form.get('priority1')
    #print(priority)
    todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).filter_by(priority=priority).all()
    return render_template('index.html', todos=todos,user_id=user_id)

@app.route('/sort/<int:user_id>/<string:button>',methods=['GET'])
def sort(user_id,button):
    if button=="Title":
        todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).order_by(Todo.title.asc()).all()
        return render_template('index.html', todos=todos,user_id=user_id)
    if button=="Priority":
        todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).order_by(Todo.priority.asc()).all()
        return render_template('index.html', todos=todos,user_id=user_id)
    if button=="Deadline":
        todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).order_by(Todo.deadline.asc()).all()
        return render_template('index.html', todos=todos,user_id=user_id)
    
@app.route('/add/<int:user_id>', methods=['POST'])
def add_todo(user_id):
    title = request.form.get('title')
    priority=request.form.get('priority')
    deadline_str = request.form['deadline']  # Get the deadline from form input
    deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    if title:
        new_todo = Todo(title=title,user_id=user_id,priority=priority,deadline=deadline_date)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index',user_id=user_id)) 

@app.route('/clear/<int:user_id>')
def clear_all(user_id):
    todo_lst=Todo.query.filter_by(user_id=user_id).all()
    for i in todo_lst:
        if i.completed == True:
            i.clear=True
    db.session.commit()
    return redirect(url_for('index',user_id=user_id)) 

@app.route('/search/<int:user_id>', methods=['GET'])
def search(user_id):
    query = request.args.get('query')
    if query:
        todos = Todo.query.filter(Todo.user_id == user_id, Todo.title.ilike(f'%{query}%')).all()
    else:
        todos = Todo.query.filter_by(user_id=user_id).all()
    
    return render_template('dashboard.html', todos=todos, query=query)

@app.route('/complete/<int:user_id>/<int:todo_id>')
def complete_todo(user_id,todo_id):
    todo = Todo.query.get(todo_id)
    now = datetime.now()
    formatted_datetime = now.strftime('%d-%m-%Y %H:%M %p')
    #print(formatted_datetime)
   
    if todo:
        todo.completed = not todo.completed
        todo.completed_date=formatted_datetime
        db.session.commit()
    return redirect(url_for('index',user_id=user_id)) 

if __name__ == '__main__':
    app.run(debug=True)

#@app._got_first_request
#def create_tables():
#    db.create_all()

# @app.route('/delete/<int:todo_id>')
# def delete_todo(todo_id):
#     todo = Todo.query.get(todo_id)
#     if todo:
#         db.session.delete(todo)
#         db.session.commit()
#     return redirect(url_for('index'))