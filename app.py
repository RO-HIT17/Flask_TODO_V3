from flask import redirect,url_for,render_template,request,Flask
from models import db,Todo,User

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
    return render_template('dashboard.html',data=data)

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
    todos = Todo.query.filter_by(user_id=user_id).all()
    return render_template('index.html', todos=todos,user_id=user_id)

@app.route('/add/<int:user_id>', methods=['POST'])
def add_todo(user_id):
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title,user_id=user_id)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index',user_id=user_id)) 

@app.route('/clear/<int:user_id>')
def clear_all(user_id):
    todo_lst=Todo.query.all()
    for i in todo_lst:
        if i.completed == True:
            db.session.delete(i)
    db.session.commit()
    return redirect(url_for('index',user_id=user_id)) 

@app.route('/complete/<int:user_id>/<int:todo_id>')
def complete_todo(user_id,todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = not todo.completed
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