from prerender.prerender import Prerender
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pyppeteer').setLevel(logging.ERROR)
logging.getLogger('websockets').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)

pre = Prerender(
    site_map_url="https://www.google.com/gmail/sitemap.xml",
    s3_bucket="google-prerender"
)
pre.invalidate()
pre.capture()
