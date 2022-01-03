from logging import debug
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import flask
from flask import request
import json
import re
from urllib.parse import urlparse
import tldextract

PATH = '/Users/tunguyen/Documents/Development/crawler/chromedriver'
LOGIN_NAME = "trinhhuuhuong911"
LOGIN_PWD = "thhuong911"

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/endpoint', methods=['POST'])
def home():
    hello = {"code": 200, "message": "API Endpoint"}
    return hello

@app.route('/api/v1/resources/price', methods=['POST'])

def api_all():
    data = "hello"
    if request.method == "POST":
        url = request.form['url']
        domain = tldextract.extract(url).domain
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-automation']) 
        browser = webdriver.Chrome(PATH, options=options)

        if domain == "taobao":
            # options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
            browser.get(url)
            browser.find_element_by_xpath("//*[@id=\"fm-login-id\"]").send_keys( LOGIN_NAME ); 
            browser.find_element_by_xpath("//*[@id=\"fm-login-password\"]").send_keys( LOGIN_PWD ); 
            browser.find_element_by_xpath("//*[@id=\"login-form\"]/div[4]/button").click()
            
            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'tb-title')))
                title = browser.find_element_by_class_name('tb-main-title').text
                price = browser.find_elements_by_class_name('tb-rmb-num')
                if len(price) > 2:
                    price = price[1].text
                else: price = price[0].text
                data = {
                    "price": price,
                    "title": title,
                    "domain": domain
                    # "src": src
                }    
            except TimeoutException:
                data = "Loading took too much time!"
            
        if domain == "1688":
            url = request.form['url']
            domain = tldextract.extract(url).domain
            options = webdriver.ChromeOptions()
            browser.get(url)
            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, 'mod-detail-title')))
                price = browser.find_element_by_class_name('price-now').text
                title = browser.find_element_by_css_selector('#mod-detail-title > h1').text
                data = {
                    "price": price,
                    "title": title,
                    "domain": domain
                    # "src": src
                }    
            except TimeoutException:
                data = "Loading took too much time!"
            
        if domain == "tmall":
            url = request.form['url']
            domain = tldextract.extract(url).domain
            options = webdriver.ChromeOptions()
            browser.get(url)
            try:
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'baxia-dialog-close')))
                browser.find_element_by_class_name("baxia-dialog-close").click()
                price = browser.find_element_by_class_name('tm-price').text
                title = browser.find_element_by_class_name('tb-detail-hd').text
                data = {
                    "price": price,
                    "title": title,
                    "domain": domain
                    # "src": src
                }    
            except TimeoutException:
                data = "Loading took too much time!"
    return data

app.run()





