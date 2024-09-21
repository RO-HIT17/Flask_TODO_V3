from flask import redirect,url_for,render_template,request,Flask,send_from_directory
from models import db,Todo,User
from datetime import datetime
from flask_mail import Mail, Message
import random
import os
from werkzeug.utils import secure_filename
from celery import Celery
from datetime import datetime, timedelta
from celery_tasks import make_celery

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6380/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6380/0'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mithrans8c@gmail.com'
app.config['MAIL_PASSWORD'] = 'bzio tgqs ijkm bnde'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

celery = make_celery(app)

@celery.task
def send_due_date_reminder(email, task_name, due_date):
    """Send an email reminder about the due date."""
    print("Hel1lo")
    with app.app_context():
        print("Hello")
        msg = Message('Task Due Reminder', sender='mithrans8c@gmail.com', recipients=[email])
        msg.body = f'Reminder: Your task {task_name} is due on {due_date}.'
        mail.send(msg)




UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

verification_code=0
def verification():
    global verification_code 
    verification_code = random.randint(100000, 999999) 
    return verification_code

@app.route('/edit_task/<int:user_id>', methods=['POST'])
def edit_task(user_id):
    task_id = request.form['task_id']
    title = request.form['title']
    priority = request.form['priority']
    deadline_str = request.form.get('deadline')
    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()  

    task = Todo.query.get(task_id)
    if task:
        task.title = title
        task.priority = priority
        task.deadline = deadline
        db.session.commit()
    return redirect(url_for('index',user_id=user_id))
    
@app.route('/send_verification', methods=['POST'])
def send_verification():
    email = request.form['email']  
    update=User.query.filter_by(email=email).first()
    if update:  
        verification_code=verification()
        
        msg = Message('Your Verification Code', sender='mithrans8c@egmail.com', recipients=[email])
        msg.body = f'Your verification code is {verification_code}.'
        try:
            mail.send(msg)
        except Exception as e:
            return str(e)
        
        return render_template('forgot_password.html',em=email, message=f'Verification code sent to {email}',val=1,ver=1)
    else:
        error="Username not registered"
        return render_template('forgot_password.html', er_message=error,val=1)

@app.route('/reset' , methods=['POST'])
def reset_password():
    email=request.form.get('email')
    new_password=request.form.get('newpassword')
    verification=request.form.get('verification')
    update=User.query.filter_by(email=email).first()
    if update:
        print(verification,verification_code)
        if int(verification)==int(verification_code):
            update.password=new_password
            db.session.commit()
            return render_template('forgot_password.html',em=email,np=new_password, message="Password Changed Successfully",val=1)
        else:
            error="Verification Code Not Matched"
            return render_template('forgot_password.html', er_message=error,val=1)

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
    if priority:
        todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).filter_by(priority=priority).all()
        return render_template('index.html', todos=todos,user_id=user_id)
    else:
        todos = Todo.query.filter_by(user_id=user_id).filter_by(clear=False).all()
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
    user=User.query.get(user_id)
    email=user.email
    title = request.form.get('title')
    priority=request.form.get('priority')
    deadline_str = request.form['deadline']  
    deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = filename
    else:
        file_url = None 

    if title:
        new_todo = Todo(title=title, user_id=user_id, priority=priority, deadline=deadline_date, file_url=file_url)
        db.session.add(new_todo)
        db.session.commit()
        #reminder_time = deadline_date - timedelta(days=1)
        #send_due_date_reminder.apply_async(args=[email, title, deadline_date], eta=reminder_time)
        #send_due_date_reminder.delay(email, title, deadline_date)


    return redirect(url_for('index', user_id=user_id))

@app.route('/delete/<int:user_id>/<int:todo_id>', methods=['GET'])
def delete_todo(user_id, todo_id):
    todo = Todo.query.get(todo_id)
    
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index', user_id=user_id))

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
        todos = Todo.query.filter(Todo.user_id == user_id , Todo.title.ilike(f'%{query}%')).filter_by(clear=False).all()
    else:
        todos = Todo.query.filter_by(user_id=user_id).all()
    return render_template('index.html', todos=todos, query=query,user_id=user_id)

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

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/rankings')
def rankings():
    user_rankings = (
        db.session.query(User.fname, User.lname, db.func.count(Todo.todo_id).label('task_count'))
        .join(Todo, User.user_id == Todo.user_id)
        .filter(Todo.completed == True)
        .group_by(User.user_id)
        .order_by(db.desc('task_count'))
        .all()
    )

    ranked_users = []
    for index, user in enumerate(user_rankings, start=1):
        ranked_users.append({
            'rank': index,
            'fname': user[0],
            'lname': user[1],
            'task_count': user[2]
        })

    return render_template('rankings.html', ranked_users=ranked_users)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

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


# Define an upload folder outside the static folder
#UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx'}

#def allowed_file(filename):
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#if not os.path.exists(app.config['UPLOAD_FOLDER']):
#    os.makedirs(app.config['UPLOAD_FOLDER'])

# Define the folder where uploaded files will be saved

