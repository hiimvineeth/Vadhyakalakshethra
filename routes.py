from flask import Flask, render_template, request, redirect,  flash, abort, url_for
# from vadhyakalakshethra import app,db,bcrypt,mail
from vadhyakalakshethra import app,db,mail
from vadhyakalakshethra import app
from vadhyakalakshethra.models import *
from vadhyakalakshethra.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/admin_layout')
def admin_layout():
    return render_template("admin_layout.html")



@app.route('/user_layout')
def user_layout():
    return render_template("user_layout.html")



@app.route('/forgot_password', methods = ['GET','POST'])
def forgot_password():
   
    if request.method=="POST":
        email=request.form["email"]
        d=Login.query.filter_by(username=email).first()
        pass_mail(d.username,d.password)
        return redirect('/login')
    else:
    
        return render_template("forgot_password.html")
    



def pass_mail(email,password):
    msg = Message('Password ',
                  recipients=[email])
    msg.body = f'''Your Password is {password}  '''
    mail.send(msg)


@app.route('/')
def index():
    d=Login.query.filter_by(usertype="artist",status="approve").all()
    return render_template("index.html",d=d)



@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        subject = request.form['subject']
        message = request.form['message']
        my_data = Contact(name=name, email=email,contact=contact,subject=subject,message=message,usertype="user")
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/')
    else :
        return render_template("contact.html")


@app.route('/register')
def register():
    return render_template("register.html")



@app.route('/login', methods=["GET","POST"])
def login():
     if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         admin = Login.query.filter_by(username=username, password=password,usertype= 'admin').first()
         artist=Login.query.filter_by(username=username,password=password, usertype= 'artist',status="approve").first()
         user=Login.query.filter_by(username=username,password=password, usertype= 'user').first()
         if admin:
             login_user(admin)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/admin_index') 
             
         elif artist:
             login_user(artist)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/artist_index/'+str(artist.id))
         
         elif user:
             login_user(user)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/user_index/'+str(user.id)) 


         else:
             d="Invalid Username or Password" 
             return render_template("login.html",d=d)
    #  flash('Invalid Username and Password!')
     return render_template("login.html")





@app.route('/artist_register',methods=['GET', 'POST'])
def artist_register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        qualification=request.form['qualification']
        talents=request.form['talents']
        specialisation=request.form['specialisation']
        experience=request.form['experience']
        events=request.form['events']
        achievements=request.form['achievements']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        img=request.files['image']
        pic_file = save_picture(img)
        view = pic_file
        print(view)  

        my_data = Artist(aname=name, image=view,aaddress=address,aemail=email,acontact=contact,password=password,qualification=qualification,talents=talents,specialisation=specialisation,experience=experience,events=events,achievements=achievements,status="null")
        my_data1 = Login(name=name,image=view, address=address,username=email,contact=contact,password=password,usertype="artist",qualification=qualification,talents=talents,specialisation=specialisation,experience=experience,events=events,achievements=achievements,status="null")
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        reg_sendmail(email)
        flash("Registered successfully! Please Wait for Confirmation")
        return redirect('/artist_register')
        
    else :
        return render_template("artist_register.html")




@app.route('/artist_profile_update/<int:id>',methods=['GET', 'POST'])
def artist_profile_update(id):
    d=Login.query.filter_by(id=id).first()
    m=Artist.query.filter_by(aid=d.id).first()
    if request.method == 'POST':
        d.name = request.form['name']
        d.address = request.form['address']
        d.qualification=request.form['qualification']
        d.talents=request.form['talents']
        d.specialisation=request.form['specialisation']
        d.experience=request.form['experience']
        d.events=request.form['events']
        d.achievements=request.form['achievements']
        d.username = request.form['email']
        d.contact = request.form['contact']
        d.password = request.form['password']
        m.aname = request.form['name']
        m.aaddress = request.form['address']
        m.qualification=request.form['qualification']
        m.talents=request.form['talents']
        m.specialisation=request.form['specialisation']
        m.experience=request.form['experience']
        m.events=request.form['events']
        m.achievements=request.form['achievements']
        m.aemail = request.form['email']
        m.acontact = request.form['contact']
        m.password = request.form['password']
        # img=request.files['image']
        # pic_file = save_picture(img)
        # view = pic_file
        # print(view)  

        # my_data = Artist(aname=name, image=view,aaddress=address,aemail=email,acontact=contact,password=password,qualification=qualification,talents=talents,specialisation=specialisation,experience=experience,events=events,achievements=achievements,status="null")
        # my_data1 = Login(name=name,image=view, address=address,username=email,contact=contact,password=password,usertype="artist",qualification=qualification,talents=talents,specialisation=specialisation,experience=experience,events=events,achievements=achievements,status="null")
        # db.session.add(my_data) 
        # db.session.add(my_data1) 
        db.session.commit()
        return redirect('/artist_view_profile/'+str(d.id))
        
    else :
        return render_template("artist_profile_update.html",d=d,m=m)



@app.route('/edit_artistpic/<int:id>', methods = ['GET','POST'])
def edit_artistpic(id):
    d = Login.query.filter_by(id=id).first()
    m = Artist.query.filter_by(aid=d.id).first()
    if request.method == 'POST':
        img=request.files['image']
        pic_file = save_picture(img)
        view = pic_file
        print(view) 
        d.image=view
        m.image=view
        db.session.commit()
        return redirect('/artist_view_profile/'+str(d.id))
    else :
        return render_template("edit_artistpic.html",d=d)


@app.route('/user_register',methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        my_data = User(name=name, address=address,email=email,contact=contact,password=password)
        my_data1 = Login(name=name, address=address,username=email,contact=contact,password=password,usertype="user")
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        user_sendmail(email)
        flash("Registered successfully! Please Login..")
        return redirect('/login')
        
    else :
        return render_template("user_register.html")


@app.route('/user_profile_update/<int:id>',methods=['GET', 'POST'])
def user_profile_update(id):
    d = Login.query.filter_by(id=id).first()
   
    if request.method == 'POST':
        d.name = request.form['name']
        d.address = request.form['address']
        d.username = request.form['email']
        d.contact = request.form['contact']
        d.password = request.form['password']
        db.session.commit()
        return redirect('/user_view_profile/'+str(d.id))
        
    else :
        return render_template("user_profile_update.html",d=d)


def user_sendmail(email):
    msg = Message('Registeration  Successfull',
                  recipients=[email])
    msg.body = f''' Your Registeration  is Successfully Completed.You can now Login using Email and Password'''
    mail.send(msg)



@login_required
@app.route('/user_contact/<id>', methods = ['GET','POST'])
def user_contact(id):
    d=Login.query.filter_by(id=id).first()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        subject = request.form['subject']
        message = request.form['message']
        my_data = Contact(name=name, email=email,contact=contact,subject=subject,message=message,usertype="User")
        db.session.add(my_data) 
        db.session.commit()
   
        return redirect('/user_index/'+str(current_user.id))
    else :
        return render_template("user_contact.html",d=d)


@login_required
@app.route('/artist_contact/<id>', methods = ['GET','POST'])
def artist_contact(id):
    d=Login.query.filter_by(id=id).first()
 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        subject = request.form['subject']
        message = request.form['message']
        my_data = Contact(name=name, email=email,contact=contact,subject=subject,message=message,usertype="Artist")
        db.session.add(my_data) 
        db.session.commit()

        return redirect('/artist_index/'+str(current_user.id))
    else :
        return render_template("artist_contact.html",d=d)



@app.route('/services')
def services():
    return render_template("services.html")


@login_required
@app.route('/admin_index')
def admin_index():
    return render_template("admin_index.html")


@login_required
@app.route('/vadhyams')
def vadhyams():
    return render_template("vadhyams.html")


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/usuccess')
def usuccess():
    return render_template("usuccess.html")



@login_required
@app.route('/admin_view_bookings')
def admin_view_bookings():
    return render_template("admin_view_bookings.html")



@login_required
@app.route('/artist_layout')
def artist_layout():
    return render_template("artist_layout.html")



@login_required
@app.route('/user_bookings')
def user_bookings():
    return render_template("user_bookings.html")



@login_required
@app.route('/user_index/<id>')
def user_index(id):
    return render_template("user_index.html")


@login_required
@app.route('/artist_index/<aid>')
def artist_index(aid):
    return render_template("artist_index.html")



@login_required
@app.route('/artist_view_profile/<id>')
def artist_view_profile(id):
    d= Login.query.get_or_404(id)
    return render_template("artist_view_profile.html",d=d)



@login_required
@app.route('/artist_buy_vadhyam/<id>', methods = ['GET','POST'])
def artist_buy_vadhyam(id):
    d= Order.query.get_or_404(id)
    if request.method == 'POST':
        uid=request.form['uid']
        uname = request.form['uname']
        uaddress = request.form['uaddress']
        ucontact=request.form["ucontact"]
        uemail = request.form['uemail']
        name=request.form['name']
        type = request.form['type']
        image=request.form['image']
        material = request.form['material']
        price=request.form["price"]
        cardno=request.form["cardno"]
        expmonth=request.form["expmonth"]
        expyear=request.form["expyear"]
        cvc=request.form["cvc"]
        obj1 = Payment(uid=uid,uname=uname,image=image,ucontact=ucontact, uemail=uemail,uaddress=uaddress,name=name,type=type, material=material,price=price,cardno=cardno,expmonth=expmonth,expyear=expyear,cvc=cvc)
        db.session.add(obj1)
        db.session.delete(d)
        db.session.commit()
        bsendmail()
        return redirect('/success')
    else :
        return render_template("artist_buy_vadhyam.html",d=d)




@login_required
@app.route('/user_buy_vadhyam/<id>', methods = ['GET','POST'])
def user_buy_vadhyam(id):
    d= Order.query.get_or_404(id)
    if request.method == 'POST':
        uid=request.form['uid']
        uname = request.form['uname']
        uaddress = request.form['uaddress']
        ucontact=request.form["ucontact"]
        uemail = request.form['uemail']
        name=request.form['name']
        image=request.form['image']
        type = request.form['type']
        material = request.form['material']
        price=request.form["price"]
        cardno=request.form["cardno"]
        expmonth=request.form["expmonth"]
        expyear=request.form["expyear"]
        cvc=request.form["cvc"]
        obj1 = Payment(uid=uid,uname=uname,ucontact=ucontact,image=image, uemail=uemail,uaddress=uaddress,name=name,type=type, material=material,price=price,cardno=cardno,expmonth=expmonth,expyear=expyear,cvc=cvc)
        db.session.add(obj1)
        db.session.delete(d)
        db.session.commit()
        bsendmail()
        return redirect('/usuccess')
    else :
        return render_template("user_buy_vadhyam.html",d=d)

@login_required
@app.route('/artist_view_orders/<id>')
def artist_view_orders(id):
    obj= Order.query.filter_by(uid=id).all()
    return render_template("artist_view_orders.html",obj=obj)


@login_required
@app.route('/user_view_orders/<id>')
def user_view_orders(id):
    obj= Order.query.filter_by(uid=id).all()
    return render_template("user_view_orders.html",obj=obj)


@login_required
@app.route('/artist_view_payments/<id>')
def artist_view_payments(id):
    obj= Payment.query.filter_by(uid=id).all()
    return render_template("artist_view_payments.html",obj=obj)



@login_required
@app.route('/user_view_payments/<id>')
def user_view_payments(id):
    obj= Payment.query.filter_by(uid=id).all()
    return render_template("user_view_payments.html",obj=obj)


@login_required
@app.route('/user_view_profile/<id>')
def user_view_profile(id):
    d= Login.query.get_or_404(id)
    return render_template("user_view_profile.html",d=d)




@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')





@app.route('/approve/<int:id>')
def approve(id):
    c= Login.query.get_or_404(id)
    c.status = 'approve'
    db.session.commit()
    a_sendmail(c.username)
    return redirect('/approved_artists')

@app.route('/reject/<int:id>')
def reject(id):
    c= Login.query.get_or_404(id)
    c.status = 'reject'
    db.session.commit()
    r_sendmail(c.username)
    return redirect('/rejected_artists')


def reg_sendmail(email):
    msg = Message('Registered Successfully',
                  recipients=[email])
    msg.body = f''' Congratulations , Your  Registeration is completed successfully.Please wait for Approval '''
    mail.send(msg)

# @app.route('/artist_approve/<int:id>')
# def artist_approve(id):
#     c= BookArtist.query.get_or_404(id)
#     c.status = 'approve'
#     db.session.commit()
#     artapp_sendmail()
#     return redirect('/approved_bookings')


# @app.route('/artist_reject/<int:id>')
# def artist_reject(id):
#     c= BookArtist.query.get_or_404(id)
#     c.status = 'reject'
#     db.session.commit()
#     artrej_sendmail()
#     return redirect('/rejected_bookings')

def a_sendmail(username):
    msg = Message('Approved Successfully',
                  recipients=[username])
    msg.body = f''' Congratulations , Your  Registeration is approved successfully... Now You can login using username and password '''
    mail.send(msg)

def r_sendmail(username):
    msg = Message('Registeration Rejected',
                  recipients=[username])
    msg.body = f''' Sorry , Your  Registeration is rejected. '''
    mail.send(msg)


# def artapp_sendmail():
#     msg = Message('Approved Successfully',
#                   recipients=[current_user.username])
#     msg.body = f''' Congratulations , Your  Booking is approved successfully... Now You can login using username and password '''
#     mail.send(msg)

# def artrej_sendmail():
#     msg = Message('Booking Rejected',
#                   recipients=[current_user.username])
#     msg.body = f''' Sorry , Your  Booking is rejected. '''
#     mail.send(msg)


@login_required
@app.route('/registered_artists',methods=["GET","POST"])
def registered_artists():
    obj = Login.query.filter_by(status="null").all()
    return render_template("registered_artists.html",obj=obj)





@login_required
@app.route('/view_artist_profile/<int:id>',methods=["GET","POST"])
def view_artist_profile(id):
    d = Login.query.get_or_404(id)
    return render_template("view_artist_profile.html",d=d)


@login_required
@app.route('/user_view_artist_profile/<int:id>',methods=["GET","POST"])
def user_view_artist_profile(id):
    d = Login.query.get_or_404(id)
    return render_template("user_view_artist_profile.html",d=d)


@login_required
@app.route('/approved_artist_profile/<int:id>',methods=["GET","POST"])
def approved_artist_profile(id):
    d = Login.query.get_or_404(id)
    return render_template("approved_artist_profile.html",d=d)



@login_required
@app.route('/approved_artists',methods=["GET","POST"])
def approved_artists():
    obj = Login.query.filter_by(status="approve").all()
    return render_template("approved_artists.html",obj=obj)


@login_required
@app.route('/user_view_artists',methods=["GET","POST"])
def user_view_artists():
    obj = Login.query.filter_by(status="approve").all()
    return render_template("user_view_artists.html",obj=obj)


@login_required
@app.route('/rejected_artists',methods=["GET","POST"])
def rejected_artists():
    obj = Login.query.filter_by(status="reject").all()
    return render_template("rejected_artists.html",obj=obj)


@login_required
@app.route('/admin_view_users',methods=["GET","POST"])
def admin_view_users():
    obj = Login.query.filter_by(usertype="user").all()
    return render_template("admin_view_users.html",obj=obj)


@login_required
@app.route('/admin_view_payments',methods=["GET","POST"])
def admin_view_payments():
    obj = Payment.query.all()
    return render_template("admin_view_payments.html",obj=obj)



@login_required
@app.route('/admin_view_vadhyam_bookings',methods=["GET","POST"])
def admin_view_vadhyam_bookings():
    obj = Order.query.all()
    return render_template("admin_view_vadhyam_bookings.html",obj=obj)


@login_required
@app.route('/admin_view_orders',methods=["GET","POST"])
def admin_view_orders():
    obj = Order.query.all()
    return render_template("admin_view_orders.html",obj=obj)


@login_required
@app.route('/admin_view_artists',methods=["GET","POST"])
def admin_view_artists():
    return render_template("admin_view_artists.html")




@app.route('/admin_add_vadhyam',methods=['GET', 'POST'])
@login_required
def admin_add_vadhyam():
    form=AddVadhyam()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            view = pic_file
        print(view)  
        obj1 = Vadhyam(name=form.name.data,image=view,type=form.type.data,material = form.material.data,price = form.price.data)
        my_data1 = Login(name=form.name.data,type=form.type.data,material = form.material.data,price = form.price.data )
        db.session.add(my_data1)
        db.session.add(obj1)
        db.session.commit()
        return redirect('/admin_index')
    return render_template("admin_add_vadhyam.html",form=form)




@app.route('/artist_add_vadhyams',methods=['GET', 'POST'])
@login_required
def artist_add_vadhyams():
    form=AddVadhyam()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            view = pic_file
        print(view)  
        obj1 = Vadhyam(name=form.name.data,image=view,type=form.type.data,material = form.material.data,price = form.price.data)
        my_data1 = Login(name=form.name.data,type=form.type.data,material = form.material.data,price = form.price.data )
        db.session.add(my_data1)
        db.session.add(obj1)
        db.session.commit()
        return redirect('/artist_view_vadhyams')
    return render_template("artist_add_vadhyams.html",form=form)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@login_required
@app.route('/admin_edit_vadhyam/<int:id>', methods=['GET', 'POST'])
def admin_edit_vadhyam(id):
    obj = Vadhyam.query.get_or_404(id)
    if request.method == 'POST':
        obj.name = request.form['name']
        obj.type = request.form['type']
        obj.material = request.form['material']
        obj.price = request.form['price']
        db.session.commit()
        return redirect('/admin_view_vadhyam')
    return render_template('admin_edit_vadhyam.html', obj=obj)




@app.route('/admin_delete_vadhyam/<int:id>')
@login_required
def admin_delete_vadhyam(id):
    delet = Vadhyam.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/admin_view_vadhyam')
    except:
        return 'There was a problem deleting that task'




@app.route('/cancel_artist_booking/<int:id>')
@login_required
def cancel_artist_booking(id):
    delet = BookArtist.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/user_view_artists')
    except:
        return 'There was a problem deleting that task'


@app.route('/artist_cancel_order/<int:id>')
@login_required
def artist_cancel_order(id):
    delet = Order.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/artist_view_vadhyams')
    except:
        return 'There was a problem deleting that task'



@app.route('/user_cancel_order/<int:id>')
@login_required
def user_cancel_order(id):
    delet = Order.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/user_view_vadhyams')
    except:
        return 'There was a problem deleting that task'



@login_required
@app.route('/admin_view_vadhyam',methods=["GET","POST"])
def admin_view_vadhyam():
    obj = Vadhyam.query.all()
    return render_template("admin_view_vadhyam.html",obj=obj)






@login_required
@app.route('/user_view_vadhyams',methods=["GET","POST"])
def user_view_vadhyams():
    obj = Vadhyam.query.all()
    return render_template("user_view_vadhyams.html",obj=obj)



@login_required
@app.route('/artist_view_vadhyams',methods=["GET","POST"])
def artist_view_vadhyams():
    obj = Vadhyam.query.all()
    return render_template("artist_view_vadhyams.html",obj=obj)


@login_required
@app.route('/admin_view_feedbacks',methods=["GET","POST"])
def admin_view_feedbacks():
    obj = Contact.query.all()
    return render_template("admin_view_feedbacks.html",obj=obj)



@login_required
@app.route('/admin_view_artist_bookings',methods=["GET","POST"])
def admin_view_artist_bookings():
    obj = BookArtist.query.all()
    return render_template("admin_view_artist_bookings.html",obj=obj)



@login_required
@app.route('/user_view_bookings/<uid>',methods=["GET","POST"])
def user_view_bookings(uid):
    obj = BookArtist.query.filter_by(uid=uid).all()
    return render_template("user_view_bookings.html",obj=obj)





@login_required
@app.route('/artist_view_bookings/<aid>',methods=["GET","POST"])
def artist_view_bookings(aid):
    obj = BookArtist.query.filter_by(aid=aid).all()
    return render_template("artist_view_bookings.html",obj=obj)

@login_required
@app.route('/artist_view_feedbacks',methods=["GET","POST"])
def artist_view_feedbacks():
    obj = Contact.query.filter_by(usertype="user").all()
    return render_template("artist_view_feedbacks.html",obj=obj)




@app.route('/user_book_artist/<id>/<aid>',methods = ['GET','POST'])
def user_book_artist(id,aid):
    w=Login.query.filter_by(id=id).first()
    a=Login.query.filter_by(id=aid).first()
    
    if request.method == 'POST':
        aid=request.form['aid']
        name = request.form['name']
        address = request.form['address']
        contact=request.form["contact"]
        email = request.form['email']
        aname=request.form['aname']
        aaddress=request.form['aaddress']
        aemail = request.form['aemail']
        acontact=request.form['acontact']
        bookdate=request.form['bookdate']
        booktime=request.form['booktime']
        bookfor=request.form['bookfor']
        venue=request.form['venue']

        obj1 = BookArtist(uid=current_user.id,aid=aid,name=name,contact=contact, email=email,address=address,aname=aname,acontact=acontact, aemail=aemail,aaddress=aaddress,bookdate=bookdate,booktime=booktime,bookfor=bookfor,venue=venue)
        db.session.add(obj1)
        db.session.commit()
        ssendmail()
        return redirect('/user_view_bookings/'+str(w.id))
    else :
        return render_template("user_book_artist.html",a=a,w=w)

def ssendmail():
    msg = Message('Booking  Successfull',
                  recipients=[current_user.username])
    msg.body = f''' Your Artist Booking is Successfully done'''
    mail.send(msg)

def bsendmail():
    msg = Message('Payment  Successfull',
                  recipients=[current_user.username])
    msg.body = f''' Payment successfully done'''
    mail.send(msg)



@app.route('/artist_order_vadhyams/<id>/<uid>',methods = ['GET','POST'])
def artist_order_vadhyams(id,uid):
    w=Login.query.filter_by(id=id).first()
    a=Vadhyam.query.filter_by(id=uid).first()
    
    if request.method == 'POST':
        uid=request.form['uid']
        uname = request.form['uname']
        uaddress = request.form['uaddress']
        ucontact=request.form["ucontact"]
        image=request.form['image']
        uemail = request.form['uemail']
        name=request.form['name']
        type = request.form['type']
        material = request.form['material']
        price=request.form["price"]
        obj1 = Order(uid=current_user.id,uname=uname,image=image,ucontact=ucontact, uemail=uemail,uaddress=uaddress,name=name,type=type, material=material,price=price)
        db.session.add(obj1)
        db.session.commit()
        # bsendmail()
        return redirect('/artist_view_orders/'+str(w.id))
    else :
        return render_template("artist_order_vadhyams.html",a=a,w=w)



@app.route('/user_order_vadhyams/<id>/<uid>',methods = ['GET','POST'])
def user_order_vadhyams(id,uid):
    w=Login.query.filter_by(id=id).first()
    a=Vadhyam.query.filter_by(id=uid).first()
    
    if request.method == 'POST':
        uid=request.form['uid']
        uname = request.form['uname']
        uaddress = request.form['uaddress']
        image=request.form['image']
        ucontact=request.form["ucontact"]
        uemail = request.form['uemail']
        name=request.form['name']
        type = request.form['type']
        material = request.form['material']
        price=request.form["price"]
        obj1 = Order(uid=current_user.id,uname=uname,image=image,ucontact=ucontact, uemail=uemail,uaddress=uaddress,name=name,type=type, material=material,price=price)
        db.session.add(obj1)
        db.session.commit()
        # bsendmail()
        return redirect('/user_view_orders/'+str(w.id))
    else :
        return render_template("user_order_vadhyams.html",a=a,w=w)
