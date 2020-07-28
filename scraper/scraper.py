# pylint: disable=W0613
"""
A function designed to take in a url and return the rendered html
"""
from os import environ
from logging import debug
from asyncio import get_event_loop
from pyppeteer import launch


def block_request(url):
    """
    A function to determine if url should be blocked based on environment variable
    """
    allowed_domains = environ.get('ALLOWED_DOMAINS', None)
    if allowed_domains:
        allowed_domains = allowed_domains.split(",")
        for domain in allowed_domains:
            if domain in url:
                return False
        return True
    return False


async def interception(req):
    """
    A function to intercept url requests and block if specified
    """
    if block_request(req.url):
        debug("blocking url %s", req.url)
        await req.abort()
    else:
        await req.continue_()


async def __get_page(url: str, username: str = None, password: str = None):
    """
    A function to get a url
    """
    browser = await launch(ignoreHTTPSErrors=True,
                           headless=True,
                           args=[
                               '--no-sandbox',
                               '--disable-setuid-sandbox',
                               '--disable-gpu'
                           ])
    page = await browser.newPage()
    if username and password:
        await page.authenticate({'username': username, 'password': password})

    debug("Setting page interception")
    await page.setRequestInterception(True)
    page.on('request', interception)
    debug("loading page %s", url)
    await page.goto(url, waitUntil=['load', 'networkidle0'])
    content = await page.content()
    await browser.close()
    return content


def query_url(url, loop=None, username: str = None, password: str = None):
    """
    A function to query the async function that gets the page
    """
    if not loop:
        loop = get_event_loop()

    results = loop.run_until_complete(__get_page(url, username, password))
    return results
