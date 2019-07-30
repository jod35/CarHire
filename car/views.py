from car import app,db
#importing the  app and the SQLAlchemy instance
from car.models import User,Car
#importing our database models
from flask import render_template,request,flash,redirect
#flask libraries for some backend functionality
from flask_bcrypt import Bcrypt
#for password hashing
from flask_login import current_user,login_user,logout_user,login_required
#for managing the logins

bcrypt=Bcrypt(app)

@app.route('/')
def index():
   cars=Car.query.all()
   return render_template('index.html',cars=cars)


@app.route('/signup',methods=['GET', 'POST'])
def SignUp():

   if request.method=='POST':
      name=request.form.get('name')
      email=request.form.get('email')
      password=request.form.get('password')
      passwd=bcrypt.generate_password_hash(password)
      new_user=User(name=name,email=email,password=passwd)
      db.session.add(new_user)
      db.session.commit()
      flash('Account created for %s You can now login..'%name)
      return redirect ('/signup')
   return render_template('signup.html')

@app.route('/login',methods=['GET', 'POST'])
def Login():
   if request.method=='POST':
      name=request.form.get('name')
      password_candidate=request.form.get('password')
      user=User.query.filter_by(name=name).first()

      if user and bcrypt.check_password_hash(user.password,password=password_candidate):
         login_user(user)
         return redirect('/')
      else:
         flash('Invalid Credentials, Check Your email or password,\nSign Up if You lack an account')

   return render_template('login.html')

@app.route('/logout')
def LogOut():
   logout_user()
   return redirect('/')

@app.route('/cars',methods=['GET', 'POST'])
@login_required
def AddCars():
   if request.method=='POST':
      name=request.form.get('name')
      car_type=request.form.get('type')
      price=request.form.get('price')
      image_url=request.form.get('image_url')
      new_car=Car(name=name,car_type=car_type,hire_price=price,image_url=image_url,owner=current_user)
      db.session.add(new_car)
      db.session.commit()
      flash('Added Successfully')
      return redirect('/cars')

   return render_template('mycars.html')

@app.route('/manage')
def Manage():
    cars=Car.query.all()
    return render_template('manage.html',cars=cars)

@app.route('/update/<int:id>',methods=['GET', 'POST'])
@login_required
def Update(id):
   car=Car.query.get_or_404(id)
   if request.method=='POST':
      car.name=request.form.get('name')
      car.hire_price=request.form.get('price')
      car.car_type=request.form.get('type')
      car.image_url=request.form.get('image_url')
      try:
         db.session.commit()
         flash('Info updated Successfully!!')
         return redirect('/manage')
      except:
         flash('There is a problem!!!')
         return redirect('/manage')
   return render_template('update.html',car=car)


@app.route('/delete/<int:id>',methods=['GET', 'POST'])
def Delete(id):
   car_to_be_deleted=Car.query.get_or_404(id)
   db.session.delete(car_to_be_deleted)
   db.session.commit()
   return redirect('/manage')
