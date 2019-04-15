#Main file of website code. Controls the rendering of templates and pages and contains the logic behind the website. 
#Library used: Flask, WTForms, SQLAlchemy

#Necessary Imports
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegistrationForm, LoginForm, PreferenceForm
from flask_sqlalchemy import SQLAlchemy
from graph import Graph, randomroom
from passlib.hash import sha256_crypt       #Hashing function

#Initial declarations
app=Flask(__name__)
app.config['SECRET_KEY']='development'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userdata.sqlite3'
db=SQLAlchemy(app)

#Global Variables
data=''
allocation=0

#Function to check if someone is currently logged in on server
def check_login():
    global data
    for student in UserData.query.all():
        if student.login=='True':
            data=student

#Home Page function
@app.route('/', methods=['GET', 'POST'])
def home():
    global data
    #Redirects to user home page if someone is logged in
    if data:
        return redirect(url_for('user_page'))

    return render_template('home.html')

#Login Page function
#If someone logged in, return redirect to user home page
#Otherwise if there is a form submit(POST HTTP method), check credentials and perform required action
#Otherwise if called with GET HTTP method, return login page template
@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    
    global data
    if data:
        return redirect(url_for('user_page'))
    
    if request.method=="POST":
        for student in UserData.query.all():
            if(student.username==request.form['username'].rstrip()):
                if(sha256_crypt.verify(request.form['password'], student.password)):
                    student.login='True'
                    db.session.commit()
                    check_login()
                    return redirect(url_for('user_page'))
                flash("Wrong password")
                return render_template('login.html', form=form)
        flash("Username for does not exist")
    
    return render_template('login.html', form=form)

#Registration Page function
@app.route('/reg', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    
    #If user is logged in, redirect to user home page
    global data
    if data:
        return redirect(url_for('user_page'))

    if request.method=="POST":
        error=0
        #Test for form validity using wtforms
        if form.validate()==False:
            error=1
        #Test for unique username
        if request.form['username'].rstrip() in list(student.username for student in UserData.query.all()):
            flash("Username already taken")
            error=1
        #Test for validity of roll number
        try:
            #Test for unique roll number
            if int(request.form['roll']) in list(student.roll for student in UserData.query.all()):
                flash("Roll Number already registered")
                error=1
        except:
            flash("Roll Number format invalid")
            error=1
        if error==1:
            return render_template('register.html', form=form)
        
        flash("User registered")
        #Adding new student data to database
        user = UserData(request.form['name'], request.form['username'].rstrip(), 
                        sha256_crypt.encrypt(request.form['password']), request.form['mail'], request.form['roll'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

#User home page function
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    global data, allocation
    #If allocation has been called by admin, return room template
    if allocation:
        return render_template('final_user.html', froom=data.froom, username=data.username)
    #If allocation not yet called, return normal user template
    else:
        return render_template('user_page.html', username=data.username)

#Make Preference page function
@app.route('/user/mkpref', methods=['GET', 'POST'])
def mkpref_page():
    form=PreferenceForm()
    global data
    if request.method=='POST':
        #Transform preferences into required form to be stored
        check_pref=list(request.form['p'+str(i)] for i in range(1,10))
        if choice_check(check_pref):  #Call choice_check to check if all preferences chosen are unique
            for student in UserData.query.all():    #If successful, update the database
                if student.username==data.username:
                    student.pref=str(list(request.form['p'+str(i)] for i in range(1,10)))
                    db.session.commit()
                    check_login()
                    flash("Preferences registered")
                    return redirect(url_for('user_page'))
        else:
            flash("Choices not unique")
            return render_template('mkpref.html', student=data, form=form, title='Change Preferences')
    else:
        if data.pref:
            flash("Choice already submitted once")
            return redirect(url_for('vwpref_page'))
        return render_template('mkpref.html', student=data, form=form, title='Make Preferences')

#Change preference function. Redirects to page for making preferences with suitable alert if no
# initial preeference registered. Otherwise renders required template.
@app.route('/user/chpref', methods=['GET', 'POST'])
def chpref_page():
    form=PreferenceForm()
    global data
    if not data.pref:
        flash("Preferences not yet registered")
        return redirect(url_for('mkpref_page'))    
    return render_template('mkpref.html', student=data, form=form, title='Change Preferences')
    
#View preferences function renders template for viewing prefernces stored if preferences have been
# made once. Otherwise redirects to page for making preferences with suitable alert.
@app.route('/user/vwpref', methods=['GET', 'POST'])
def vwpref_page():
    global data
    if data.pref:
        return render_template('vwpref.html', student=data, student_pref=data.pref.rstrip(']').lstrip('[').split(","))
    else:
        flash("Preferences not yet registered")
        return redirect(url_for('mkpref_page'))

#Logout function
@app.route('/logout')
def logout():
    global data
    for student in UserData.query.all():
        if student.username==data.username:
            student.login=False             #Updates database
            data=''                         #Updates variable
            db.session.commit()
            return redirect(url_for('home'))  #Redirects to website home page

#Function for profile info page. Renders user information template.
@app.route('/user/profile')
def profile():
    global data
    return render_template('profile.html', student=data)

#Function to transform the stored database into form required by graph(top trading cycle) function and 
# call the graph function. Also stores the final assignment of rooms into database. 
def allocate():
    students=list(student.username for student in UserData.query.all())
    initial=randomroom(students)    #Generates random initial allocation of rooms
    pref={}
    for student in UserData.query.all():
        pref[student.username]=list(int(student.pref.rstrip(']').lstrip('[').split(",")[i-1].lstrip(' \'').rstrip('\'')) for i in range(1,10))
    fallocation=Graph(students, initial, pref)
    for student in UserData.query.all():
        student.froom=fallocation.final[student.username]
        db.session.commit()

#Function to check all room choices entered are unique
def choice_check(choice):
    temp=[]
    for i in choice:
        if i in temp:
            return 0
        else:
            temp.append(i)
    return 1

##########################################################################################################
#Database class, contains the blueprint for the database table 
class UserData(db.Model):
    name=db.Column(db.String())
    username=db.Column(db.String())
    password=db.Column(db.String())
    mail=db.Column('e-mail', db.String())
    roll=db.Column('roll_no', db.Integer, primary_key=True)
    login=db.Column(db.String())                            #Stored the login status of each account
    pref=db.Column(db.String, nullable=True)                #Will later store preference list of student
    froom=db.Column(db.Integer, nullable=True)              #Will store the room number finally allocated

    def __init__(self, name, username, password, mail, roll, login='False', pref=''):
        self.name=name
        self.username=username
        self.password=password
        self.mail=mail
        self.roll=roll
        self.login=login
        self.pref=pref
##########################################################################################################

#Main control function
if (__name__=="__main__"):
    db.create_all()  #Instantiate database
    check_login()    #Check if someone was logged in last time server was closed
    allocation=0    #Command for admin to change phase of allocation process: 0 for preference filling phase
                     #                                                         1 for allocation phase
    if(allocation): 
        allocate()
    app.run(debug=True)     #Run application
