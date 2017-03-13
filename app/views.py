"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
import time, os
from forms import ProfileForm
from models import Profile
from werkzeug.utils import secure_filename


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


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        file = request.files['picture']
        if file:
            file_folder = app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_folder, filename))
            name = filename
        else:
            name = 'default.jpg'
        user = Profile(form.firstname.data, form.lastname.data, form.age.data,
                     form.bio.data, name, form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)
 
def uploadfile(file):
    file_folder = app.config['UPLOAD_FOLDER']
    filename = secure_filename(file.filename)
    file_path = os.path.join(file_folder, filename)
    file.save(file_path)
    
    return filename
    
@app.route('/profiles', methods=['POST', 'GET'])
def profiles():
    return jsonify(users = [i.serialize for i in Profile.query.all()])

@app.route('/profile/<int:id>/', methods=['POST', 'GET'])
def get_profile(id):
    return jsonify(Profile.query.get(id).serialize)

def timeinfo():
    return time.strftime("%c")

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
