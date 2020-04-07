import datetime
from flask import Flask
from flask import render_template, render_template_string, redirect
import urllib.request
import boto3
import time


application = Flask(__name__)


def read_s3_obj(bucket_name, output_file):
    """
    reads from an s3 bucket.
    """
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name, output_file)
        body = obj.get()['Body'].read().decode('utf-8')
        return body
    except BaseException:
        return ""


@application.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the index.html web page.
    """
    return render_template('index.html', message='Sparkle 0.0.1 - SwiftUI ftw')


if __name__ == '__main__':
    application.jinja_env.auto_reload = True
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.debug = True
    application.run()
