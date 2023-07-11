from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import requests
from bs4 import BeautifulSoup
import json
import logging
import sys
from seleniumwire import webdriver

# import seleniumwire.undetected_chromedriver as uc

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


@app.route('/headless', methods=['GET', 'POST'])
def headless():
    # other chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--window-size=1920,1200")

    ### This blocks images and javascript requests
    chrome_prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "javascript": 2,
        }
    }
    chrome_options.experimental_options["prefs"] = chrome_prefs
    ###

    driver = webdriver.Chrome(options=chrome_options)

    url = request.form.get('url')

    CUSTOM_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    SEC_CH_UA = '"Google Chrome";v="112", " Not;A Brand";v="99", "Chromium";v="112"'
    REFERER = 'https://google.com'

    # print(url)

    driver.get(url)

    response = ''

    for http_request in driver.requests:
        if http_request.url.strip('/') == url.strip('/'):
            print(http_request.url, url)
            response = http_request.response

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()

    # return dict(response.headers)

    return {
        "content": soup.html.decode(),
        "headers": dict(response.headers),
        "status": response.status_code
    }
