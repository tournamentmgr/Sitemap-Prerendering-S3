# pylint: disable=W0613
"""
A function designed to take in a url and return the rendered html
"""
from logging import debug
import asyncio
from pyppeteer import launch


async def __get_page(url: str, username: str = None, password: str = None):
    """
    A function to get a url
    """
    browser = await launch(headless=True,
                           args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'])
    page = await browser.newPage()
    if username and password:
        await page.authenticate({'username': username, 'password': password})
    debug("loading page %s", url)
    await page.goto(url, waitUntil=['load'])
    content = await page.content()
    await browser.close()
    return content


def query_url(url, loop=None, username: str = None, password: str = None):
    """
    A function to query the async function that gets the page
    """
    if not loop:
        loop = asyncio.get_event_loop()

    results = loop.run_until_complete(__get_page(url, username, password))
    return results
