# pylint: disable=W0212,W0703
"""
A function to hold the Prerender class
"""
import re
from logging import debug, error
from urllib.parse import urlparse
from urllib3 import disable_warnings

# External
from boto3 import resource, Session
from requests import get

class Prerender():
    """
    A class to query a root and underlying sitemaps, to capture all pages to prerender to S3
    """

    def __init__(self,
                 site_map_url: str,
                 s3_bucket: str,
                 check_valid: bool = True,
                 auth: (str, str)=(None, None)):

        # Disable Verify Warnings
        disable_warnings()

        # Set variables
        self.local = False
        self.site_map_url = site_map_url
        self.username = auth[0]
        self.password = auth[1]
        self.domain = urlparse(self.site_map_url).netloc
        self.bucket = s3_bucket

        # Check if sitemap is valid
        self.check = check_valid
        if check_valid:
            self.__check_valid_url(self.site_map_url)

    def __check_valid_url(self, url):
        auth = (self.username, self.password) if (self.username and self.password) else None
        if get(url, verify=False, auth=auth).status_code > 201:
            raise ValueError("Non 200 status code reached for {url}".format(url=url))

    def __get_html_content(self, url: str) -> any:
        """
        A function that takes in a url and invokes a function (local) and returns html
        """
        from scraper.scraper import query_url
        return query_url(url, username=self.username, password=self.password)

    def _capture_and_upload(self, url):
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
                    file_name = "{path}?{query}.html".format(path=urlparse(file_name).path, query=urlparse(file_name).query)
                else:
                    file_name = "{path}.html".format(path=urlparse(file_name).path)
                debug("Creating file %s", file_name)
                obj = s3_client.Object(self.bucket, file_name)
                return obj.put(Body=response)
            return None

        # pylint: disable=W0703
        except Exception as exc:
            raise exc

    def _analyze_site_map(self, body: str, url: str):
        """
        A function for analyzing a sitemap. With all https websites, map to pool
        """
        # pylint: disable=C0301
        urls = []
        for site in re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body):
            site = site.replace("</loc>", '')
            if ".xml" in site and url != site:
                content = get(site, verify=False).text
                self._analyze_site_map(content, url)
            else:
                urls.append(site)

        # Condense to unique
        urls = list(set(urls))
        debug("Found %s total urls to cache under %s", len(urls), url)
        for site in urls:
            self._capture_and_upload(site)


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
        debug("Capturing sitemap at %s", self.site_map_url)
        auth = (self.username, self.password) if (self.username and self.password) else None
        res = get(self.site_map_url, verify=False, auth=auth)
        res.raise_for_status()
        self._analyze_site_map(res.text, self.site_map_url)
