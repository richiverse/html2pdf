#! /usr/bin/env python
from os import environ

from flask import Flask, make_response, request
from jinja2 import Environment
import pdfkit

api = Flask(__name__)

config = pdfkit.configuration(wkhtmltopdf='./wkhtmltox/bin/wkhtmltopdf')

@api.route('/', methods=['POST'])
def generate_pdf():
    """Given HTML as __string, take the rest of kwargs and generate pdf."""
    data = request.json
    __string = data.pop('__string')

    try:
        __filename = data.pop('__filename')
    except KeyError:
        __filename = 'output.pdf'

    rendered = Environment().from_string(__string).render(**data)
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={__filename}'

    return response

if __name__ == '__main__':
    DEBUG = True if environ['STAGE'] != 'prod' else False
    api.run(debug=DEBUG)
