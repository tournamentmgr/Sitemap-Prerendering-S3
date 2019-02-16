# pylint: disable=W0212,W0703,C0301,R0913
"""
A function to hold the Prerender class
"""
from os import environ
from logging import debug, error
from urllib.parse import urlparse
from urllib3 import disable_warnings

# External
from boto3 import resource, Session
from requests import get
from xmltodict import parse

class Prerender():
    """
    A class to query a root and underlying sitemaps, to capture all pages to prerender to S3
    """

    def __init__(self,
                 robots_url: str,
                 s3_bucket: str,
                 auth: (str, str)=(None, None),
                 query_char_deliminator: str = '?',
                 allowed_domains: [str] = None):

        # Disable Verify Warnings
        disable_warnings()

        # Set variables
        self.local = False
        self.robots_url = robots_url
        self.username = auth[0]
        self.password = auth[1]
        self.domain = urlparse(self.robots_url).netloc
        self.query_char_deliminator = query_char_deliminator
        self.bucket = s3_bucket

        if allowed_domains:
            environ['ALLOWED_DOMAINS'] = ",".join(allowed_domains)


    def _check_valid_xml(self, url):
        auth = (self.username, self.password) if (self.username and self.password) else None
        response = get(url, verify=False, auth=auth)
        if response.status_code > 201:
            raise ValueError(f"Non 200 status code reached for {url}")
        parse(response.text)

    def __get_html_content(self, url: str) -> any:
        """
        A function that takes in a url and invokes a function (local) and returns html
        """
        from scraper.scraper import query_url
        return query_url(url, username=self.username, password=self.password)

    def capture_page_and_upload(self, url):
        """
        A wrapper function to capture, and then archive content. If it throws an error, log an skip
        """
        try:
            response = self.__get_html_content(url)

            # Strip the domain, then strip the initial, final /
            path = url.split(self.domain)[1][1:]
            if path[-1:] == '/':
                path = path[:-1]

            # Archive the file
            debug("Archiving %s", url)
            self._archive_content(file_name=path, response=response)
        except Exception as exc:
            error(exc)

    def _archive_content(self, file_name: str, response: any):
        """
        A function to upload a response to a file in S3
        """
        try:
            if response:
                s3_client = Session().resource('s3')
                if urlparse(file_name).query:
                    file_name = f"{urlparse(file_name).path}{self.query_char_deliminator}{urlparse(file_name).query}"
                else:
                    file_name = urlparse(file_name).path
                debug("Creating file %s", file_name)
                obj = s3_client.Object(self.bucket, file_name)
                return obj.put(Body=response, ContentType='text/html')
            return None

        # pylint: disable=W0703
        except Exception as exc:
            raise exc

    def _analyze_site_map(self, body: str, url: str):
        """
        A function for analyzing a sitemap. Utilizing XML Dict parse the urlset to get all urls.
        Only return the urls in the matching domain, and then capture and upload each url
        """
        # pylint: disable=C0301
        urls = []
        items = parse(body).get('urlset', {}).get('url', {})
        urls = [item['loc'] for item in items if self.domain in item.get('loc')]
        urls = list(set(urls))
        debug("Found %s total urls to cache under %s", len(urls), url)
        for site in urls:
            self.capture_page_and_upload(site)


    def invalidate(self):
        """
        A function to invalidate cache
        """
        debug("invalidating cache")
        try:
            bucket = resource('s3').Bucket(self.bucket)
            bucket.objects.all().delete()
            debug("Cache successfully cleared")
        except Exception as exc:
            error("ERROR: S3 Deletion", exc)
            raise Exception('Invalidation Deletion Error')

    def capture(self):
        """
        A function to capture the initial site map and then send to analyze
        """
        debug("Capturing robots at %s", self.robots_url)
        auth = (self.username, self.password) if (self.username and self.password) else None
        res = get(self.robots_url, verify=False, auth=auth)
        res.raise_for_status()
        for line in res.text.split("\n"):
            if 'sitemap' in line.lower():
                url = line.split("map:")[1].strip()
                response = get(url, verify=False, auth=auth)
                response.raise_for_status()
                if '<html>' in response.text:
                    error(f"{url} is html, skipping")
                else:
                    self._analyze_site_map(response.text, url)
