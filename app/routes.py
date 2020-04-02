from app import application
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
import os

class UploadFileForm(FlaskForm):
	file_selector = FileField('File', validators=[FileRequired()])
	submit = SubmitField('Submit')


@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', message='Welcome to Sparkle!')	

@application.route('/upload', methods=['GET', 'POST'])
def upload():
	"""
	Upload a file from the client machine.
	"""
	file = UploadFileForm()
	if file.validate_on_submit():
		f = file.file_selector.data
		filename = f.filename

		file_dir_path = os.path.join(application.instance_path, 'files')
		file_path = os.path.join(file_dir_path, filename)
		f.save(file_path)

		return redirect(url_for('index'))
	return render_template('upload.html', form=file)