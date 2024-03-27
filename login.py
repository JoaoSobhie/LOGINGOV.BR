from playwright.sync_api import Page, expect, sync_playwright, Playwright
import time
import os
import requests
from fake_useragent import UserAgent
import deathbycaptcha
import json

def solveHCaptcha(driver):
    client = deathbycaptcha.HttpClient('USERNAME', 'PASSWORD')

    # Put the proxy and hcaptcha data
    Captcha_dict = {
        'sitekey': '93b08d40-d46c-400a-ba07-6f91cda815b9',
        'pageurl': 'https://sso.acesso.gov.br/login'
    }

    # Create a json string
    json_Captcha = json.dumps(Captcha_dict)

    try:
        balance = client.get_balance()
        print(balance)

        # Put your CAPTCHA type and Json payload here:
        captcha = client.decode(type=7, hcaptcha_params=json_Captcha)
        if captcha:
            # The CAPTCHA was solved; captcha["captcha"] item holds its
            # numeric ID, and captcha["text"] its text token solution.
            print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
            driver.evaluate("document.getElementsByTagName('iframe')[0].setAttribute('data-hcaptcha-response', '"+ captcha["text"] +"')")
            driver.evaluate(f"document.getElementsByName('h-captcha-response')[0].textContent = '{captcha["text"]}'")
            driver.evaluate(f"document.getElementsByName('h-captcha-response')[0].value = '{captcha["text"]}'")
            return captcha["text"]

    except deathbycaptcha.AccessDeniedException:
        # Access to DBC API denied, check your credentials and/or balance
        print("error: Access to DBC API denied, check your credentials and/or balance")


def main():
    playwright = sync_playwright().start()
    args= [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--no-first-run",
        "--safebrowsing-disable-download-protection",
        "--disable-blink-features=AutomationControlled",
        "--start-normal",
        "--mute-audio",
        #"--headless=new"
        ]
    ua = UserAgent(["chrome", "edge", "firefox"], ["windows"], min_percentage=0.9)
    
    browser_type = playwright.chromium
    browser = browser_type.launch(args=args,headless=False, executable_path="/usr/bin/brave-browser")
    context = browser.new_context(user_agent=ua.random)
    page = context.new_page()
    #Verifica se o script está sendo identificado como robo
    page.goto("https://fingerprint.com/products/bot-detection")
    time.sleep(10)
   
    page.goto("https://login.esocial.gov.br/login.aspx")
    time.sleep(4)
    esoc = page.locator('//*[@id="login-acoes"]/div[2]/p/button').click()
    time.sleep(3)
    
    e = page.locator('//*[@id="login-certificate"]').bounding_box()
    url = page.url
    time.sleep(4)
    #Move o mouse randomicamente para emular comportamento humano
    page.mouse.move(0,200)
    page.mouse.move(10,110)
    page.mouse.move(110,10)
    page.mouse.move(250,35)
    page.mouse.move(221,70)
    
    #Seta os atributos necessarios para o envio da requisição
    page.evaluate('document.getElementById("operation-field").setAttribute("name", "operation");')
    page.evaluate('document.getElementById("operation-field").setAttribute("value", "login-certificate");')
    page.evaluate("document.getElementById('loginData').setAttribute('action','https://certificado.sso.acesso.gov.br/login?client_id=login.esocial.gov.br')")
    page.mouse.click(e["x"], e["y"])
    time.sleep(5)
    if url == page.url:
        solveHCaptcha(page)
        page.evaluate('document.getElementById("operation-field").setAttribute("name", "operation");')
        page.evaluate('document.getElementById("operation-field").setAttribute("value", "login-certificate");')
        page.evaluate("document.getElementById('loginData').submit()")
    

    cookies = context.cookies()
        
if __name__=="__main__":
    main()