from playwright.async_api import Page, expect, async_playwright, Playwright, Route, Request
import time
import os
import requests
from fake_useragent import UserAgent
import deathbycaptcha
import json
from OpenSSL import crypto  # type: ignore

def handle_request(self, route: Route, request: Request):
        resp = self._requestCall(
            request.url,
            request.method,
            data=request.post_data,
            allow_redirects=False,
            cert=self.__cert,
            headers=request.headers,
            fromOtherDomain=True,
        )
        route.fulfill(status=resp.status_code, headers=resp.headers, body=resp.content)


async def main():
    args = [
        "--no-sandbox",
        "--disable-gpu",
        "--disable-setuid-sandbox",
        "--no-first-run",
        # "--safebrowsing-disable-download-protection",
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        "--disable-webgl",
        "--disable-3d-apis",
        "--disable-accelerated-2d-canvas",
        "--disable-2d-canvas-image-chromium",
        "--disable-reading-from-canvas",
        #"--incognito"
    ]
    
    wss = os.getenv("WEB UNLOCKER") 
    playwright = await async_playwright().start()
    browser = playwright.chromium.connect_over_cdp(wss)
    context = browser.new_context()
    page = context.new_page()

    await page.goto("https://login.esocial.gov.br/login.aspx")
    await page.locator('//*[@id="login-acoes"]/div[2]/p/button').click()
    await page.wait_for_load_state()
    time.sleep(4)
    await page.screenshot(path='\\temp\\screenshot.png', full_page=True)
    url = page.url

    await page.mouse.move(0, 200)
    await page.mouse.move(10, 110)
    await page.mouse.move(110, 10)
    await page.mouse.move(250, 35)
    await page.mouse.move(221, 70)

    await page.evaluate('document.getElementById("operation-field").setAttribute("name", "operation");')
    await page.evaluate('document.getElementById("operation-field").setAttribute("value", "login-certificate");')
    certificateButton = await page.locator('//*[@id="login-certificate"]')
    form_action = certificateButton.get_attribute("formaction")
    await page.evaluate(f"document.getElementById('loginData').setAttribute('action','{form_action}')")
    await page.evaluate("function onHcaptchaCallback(token) {}")
    e = await page.locator('//*[@id="login-certificate"]').bounding_box()

    context.route(form_action, handle_request)

    await page.screenshot(path='\temp\\screenshot.png', full_page=True)

    await page.mouse.click(e["x"]+5, e["y"]+5)
        
if __name__=="__main__":
    main()
