import datetime
from flask import Flask
from flask import render_template, render_template_string, redirect
import simplejson
import urllib.request
import boto3
import time


application = Flask(__name__)

def read_s3_obj(bucket_name, output_file):
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name, output_file)
        body = obj.get()['Body'].read().decode('utf-8')
        return body
    except:
        return ""

@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', message='Get ready to Sparkle!')

if __name__ == '__main__':
    application.jinja_env.auto_reload = True
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.debug = True
    application.run()
