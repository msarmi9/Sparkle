"""
Helper functions for testing a Flask application.
"""
from contextlib import contextmanager

from flask import template_rendered


# src: https://flask.palletsprojects.com/en/1.1.x/signals/
@contextmanager
def captured_templates(app):
    """Context manager to provide a list of templates rendered by a request."""
    templates = []

    def capture_template(sender, template, context, **kwargs):
        templates.append((template, context))

    template_rendered.connect(capture_template, app)
    try:
        yield templates
    finally:
        template_rendered.disconnect(capture_template, app)
