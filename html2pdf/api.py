#! /usr/bin/env python
from os import environ
from io import BytesIO, StringIO
from tempfile import tempdir

import mimerender
from flask import Flask, make_response, request, Response
from jinja2 import Environment
from xhtml2pdf import pisa

api = Flask(__name__)

mimerender.register_mime('pdf', ('application/pdf',))
mimerender = mimerender.FlaskMimeRender(global_charset='UTF-8')


def render_pdf(html):
    pdf = BytesIO()
    pisa.CreatePDF(StringIO(html), pdf)
    resp = pdf.getvalue()
    pdf.close()
    return resp

@api.route('/', methods=['GET'])
@mimerender(
    default='pdf',
    html=lambda html: html,
    pdf=render_pdf,
    override_input_key='format'
)
def generate_pdf():
    """Given HTML as __string, take the rest of kwargs and generate pdf."""
    data = request.args
    __string = data.get('__string')

    __filename = 'output.pdf'
    data = {k:v for k,v in data.items() if k != '__string'}

    html = Environment().from_string(__string).render(**data)
    return {'html': html}

if __name__ == '__main__':
    DEBUG = True if environ['STAGE'] != 'prod' else False
    api.run(debug=DEBUG)
