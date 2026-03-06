import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask import send_from_directory
from app.forms import LoginForm, UploadForm
from app.models import UserProfile
from app.forms import LoginForm, UploadForm
from werkzeug.security import check_password_hash


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = UploadForm()  # Instantiate the form

    if form.validate_on_submit():  # Validate form on submit
        uploaded_file = form.file.data  # Get the uploaded file
        filename = secure_filename(uploaded_file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(save_path)  # Save file to uploads folder

        flash('File Saved Successfully!', 'success')
        return redirect(url_for('upload'))  # Redirect to upload page

    return render_template('upload.html', form=form)  # Pass form to template


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    # Validate entire form submission
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query database for the user
        user = UserProfile.query.filter_by(username=username).first()

        # Check password hash
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('You have successfully logged in!', 'success')
            return redirect(url_for("upload"))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template("login.html", form=form)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

def get_uploaded_images():
    """
    Returns a list of image filenames from the uploads folder
    """
    image_files = []
    upload_folder = app.config['UPLOAD_FOLDER']

    # Iterate over files in the uploads folder
    for filename in os.listdir(upload_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_files.append(filename)
    return image_files


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.route('/uploads/<filename>')
@login_required
def get_image(filename):
    """
    Serve a specific uploaded image from the uploads folder
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/files')
@login_required
def files():
    """
    Display all uploaded images in a grid
    """
    images = get_uploaded_images()  # get list of filenames
    return render_template('files.html', images=images)

@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user, flash a message, and redirect to home
    """
    logout_user()  # log out the user
    flash("You have been logged out.", "info")  # optional flash message
    return redirect(url_for('home'))  # redirect to home page