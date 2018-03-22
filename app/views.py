"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, filefolder
from flask import render_template, request, redirect, url_for, flash,session, abort, send_from_directory
from forms import CreateForm
from models import UserProfile
from werkzeug.utils import secure_filename
import os
import datetime


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
    return render_template('about.html')


@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = CreateForm()
    if request.method == "POST" and form.validate_on_submit():
        now = datetime.datetime.now()
        firstname = form.firstname.data
        lastname = form.lastname.data
        gender = form.gender.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        f = form.upload.data
        filename = secure_filename(f.filename)
        user = UserProfile(first_name=firstname, last_name=lastname, gender=gender, email=email, location=location, biography=biography, photo_name=filename, date_created=now)
        db.session.add(user)
        db.session.commit()
        f.save(os.path.join(filefolder, filename))
        flash('Successfully added.', 'success')
        return redirect(url_for('profiles')) 
    return render_template("profile.html", form=form)
    
    
def get_uploaded_images():
    image_names= os.listdir(filefolder)
    image=[]
    for x in image_names:
        a,b= x.split(".")
        if b == "jpg" or b == "png":
            image.append(x)
    return image


@app.route("/profiles")
def profiles():
    image_names= get_uploaded_images()
    users = UserProfile.query.all()
    return render_template('profiles.html', users=users, image_names=image_names)
    
    
@app.route("/profiles/<filename>")
def user_profile(filename):
    user = UserProfile.query.filter_by(id=filename).first()
    image_names= get_uploaded_images()
    return render_template('user_profile.html', user=user, image_names=image_names)
    
  

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session


###
# The functions below should be applicable to all Flask apps.
###


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
