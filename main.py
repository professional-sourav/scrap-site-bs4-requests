from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import requests
from bs4 import BeautifulSoup
import json
import logging
import sys

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, Worldss!'


@app.route('/scrap', methods=['GET', 'POST'])
def scrap():

    if request.form.get('headers'):
        headers = json.loads(request.form.get("headers"))
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.97 Safari/537.36"
        }

    # headers.pop("Set-Cookie")
    # headers.pop("Content-Security-Policy")

    # return headers

    url = request.form.get('url')

    page = requests.get(url, headers=headers)  # 'https://www.microsoft.com/en-in/'

    return {
        "content": page.text,
        "headers": dict(page.headers),
        "status": page.status_code
    }
