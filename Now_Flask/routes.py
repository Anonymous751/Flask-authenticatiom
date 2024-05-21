from Now_Flask import app, db, bcrypt, mail
from Now_Flask.models import Contacts, User, Blog_posts
from flask import render_template, request, flash, redirect, url_for
from Now_Flask.forms import RegisterForm, LoginForm, ResetRequestForm, ResetPasswordForm, AccountUpdateForm
from flask_login import login_user, logout_user, current_user
import json
import os
from flask_mail import Message
from datetime import datetime
from PIL import Image, ImageDraw



with open('Now_Flask/templates/config.json') as c:
    params = json.load(c)["params"]

@app.route("/")
def hello_world():
    show_list_items = True
    return render_template("slider.html", title ='Programming Languages', params=params, show_list_items=show_list_items)

@app.route("/about")
def about():
    show_list_items = True
    return render_template("about.html", title ='About', params=params, show_list_items=show_list_items)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    show_list_items = True
    if request.method == "POST":
        # Add entry to the database
        name = request.form.get('name')
        phn_no = request.form.get('phn_no')
        email = request.form.get('email')
        message = request.form.get('message')
        

        entry = Contacts(name=name, phn_no=phn_no, email=email, message=message, date_created = datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for contacting us! We will get back to you soon!", "success")
      
    return render_template("contact.html", title ='Contact', params=params, show_list_items =show_list_items)

@app.route("/register", methods=['GET', 'POST'])
def register():
    show_list_items = True
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        # Form is valid, process form data
        # For example:
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('login'))
    else:
        print("Form data:", form.data)  # Print form data
        print("Validation errors:", form.errors) 
    return render_template("register.html", title='Register', params=params, form=form, show_list_items=show_list_items)



@app.route("/login", methods=['GET', 'POST'])
def login():
    show_list_items = True
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        authuser = User.query.filter_by(email=form.email.data).first()
        if authuser and bcrypt.check_password_hash(authuser.password, form.password.data):
            login_user(authuser)
            flash(f'You have been logged in as {form.email.data}!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')
            return redirect(url_for('login'))
    return render_template("login.html", title ='Login', params=params, form=form, show_list_items=show_list_items)


def save_picture(form_picture):
    # Get the filename and path
    picture_name = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)

    # Save the original image
    form_picture.save(picture_path)

    # Open the saved image using Pillow
    img = Image.open(picture_path)

    # Define the desired dimensions for resizing
    output_size = (150, 150)  # Adjust this according to your requirements

    # Resize the image
    img.thumbnail(output_size)

    # Create a mask for the circular shape
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Calculate the coordinates for the bounding box to create a circle
    diameter = min(img.size)
    left = (img.size[0] - diameter) // 2
    top = (img.size[1] - diameter) // 2
    right = left + diameter
    bottom = top + diameter
    
    # Draw a white circle on the mask
    draw.ellipse((left, top, right, bottom), fill=255)

    # Apply the mask to the image
    round_img = Image.new("RGB", img.size, (255, 255, 255, 0))  # Initialize transparent image
    round_img.paste(img, (0, 0), mask)

    # Save the resized and circular-shaped image, overwriting the original
    round_img.save(picture_path)

    # Return the filename
    return picture_name
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    form = AccountUpdateForm()
    print(form)
    if form.validate_on_submit():
        image_file = save_picture(form.picture.data)
        current_user.image_file = image_file
        db.session.commit()
        return redirect(url_for('dashboard'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    print('photo', image_file)    
    show_list_items = False
    return render_template("dashboard.html", title ='dashboard', params=params, show_list_items=show_list_items, form=form, image_file=image_file)


   

@app.route("/logout")
def logout():
    show_list_items = True
    logout_user()
    return render_template("logout.html", title ='dashboard', params=params, show_list_items=show_list_items)





@app.route("/blog", methods=['GET'])
def blog():

    post = Blog_posts.query.all()
    print("your Data", post)
    if post:
        show_list_items = True
        return render_template("blog.html", title='Blog', params=params, show_list_items=show_list_items, post=post)
    else:
        flash("Post not found.", "danger")
        return redirect(url_for("hello_world"))  # Redirect to home page or another suitable page

def sent_mail(user):
   token = user.get_token()
   reset_token = url_for('reset_token', token=token, _external=True)
   msg = Message('Password Reset Request', sender='Param', recipients=[user.email])
   msg.body = f'''To reset your password, visit the following link:
   {reset_token}
   If you did not make this request then simply ignore this email and no changes will be made.
   '''
   mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    show_list_items = True
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            sent_mail(user)
            flash(f"An email has been sent to {form.email.data} account to reset password.", "info")
            return redirect(url_for('login'))
    return render_template("reset_password.html", title ='About', params=params, show_list_items=show_list_items, form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password =  hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("change_password.html", title ='About', params=params, form=form)



@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    show_list_items = False
    return render_template("dashboard.html", title ='dashboard', params=params, show_list_items=show_list_items)