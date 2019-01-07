from unittest import TestCase
from unittest.mock import patch, Mock
from prerender.prerender import Prerender
import botocore
import responses

class PrerenderTestCase(TestCase):
    def test_request_local(self):
        prerender = Prerender(
            site_map_url = "https://example.com",
            s3_bucket = "some-bucket",
            check_valid = False
        )
        self.assertEqual(prerender.bucket, "some-bucket")

    def test_domain_with_subdomain(self):
        prerender = Prerender(
            site_map_url = "https://subdomain.example.com/sitemap.xml",
            s3_bucket = "some-bucket",
            check_valid = False
        )
        self.assertEqual(prerender.domain, "subdomain.example.com")

    @patch('botocore.client.BaseClient._make_api_call')
    def test_upload_to_S3(self, boto_mock):
        boto_mock.side_effect =  [{"VersionId": 1,
                                  "ResponseMetadata": {"HTTPStatusCode": 200}}]
        response = Prerender(
            site_map_url = "https://subdomain.example.com/sitemap.xml",
            s3_bucket = "some-bucket",
            check_valid = False
        )._archive_content(
            file_name="test", response="some tezt"
        )
        self.assertEqual(response['VersionId'], 1)

    @responses.activate
    @patch.object(Prerender, '_capture_and_upload')
    def test_subsite_recursive_called(self, prerender):
        responses.add(responses.GET, 'https://subdomain.example.com/page1/sitemap.xml',
                  json={}, status=200)
        responses.add(responses.GET, 'https://subdomain.example.com/page2/sitemap.xml',
                  json={}, status=200)
        
        # .json.return_value = {}
        prerender.return_value = None
        Prerender(
            site_map_url = "https://subdomain.example.com/sitemap.xml",
            s3_bucket = "some-bucket",
            check_valid = False
        )._analyze_site_map(
            body="https://subdomain.example.com/page1/sitemap.xml https://subdomain.example.com/page2/sitemap.xml", 
            url="https://subdomain.example.com/sitemap.xml"
        )
        self.assertEqual(len(responses.calls), 2)
    
    @responses.activate
    @patch.object(Prerender, '_capture_and_upload')
    def test_capture_calls(self, prerender):
        responses.add(responses.GET, 'https://subdomain.example.com/sitemap.xml',
                  json={}, status=200)
        
        # .json.return_value = {}
        prerender.return_value = None
        Prerender(
            site_map_url = "https://subdomain.example.com/sitemap.xml",
            s3_bucket = "some-bucket",
            check_valid = False
        ).capture()
        self.assertEqual(len(responses.calls), 1)


    @patch.object(Prerender, '_archive_content')
    @patch('scraper.scraper.query_url')
    def test_html_query_local(self, query, archive):
        query.return_value = "test"
        archive.return_value = ""
        prerender = Prerender(
            site_map_url = "https://example.com/sitemap.xml",
            s3_bucket = "some-bucket",
            check_valid = False
        )._capture_and_upload("https:/example.com/home/test/")
        args, kwargs = call = archive.call_args_list[0]
        self.assertEqual(kwargs['file_name'], "home/test")
        self.assertEqual(kwargs['response'], "test")

    @patch.dict('os.environ', {})
    @patch.object(Prerender, '_capture_and_upload')
    def test_analyze_site_to_get_urls(self, capture):
        urls = ["https://example.com/sub/page1", "http://example.com/sub/page2"]
        capture.return_value = None
        prerender = Prerender(
            site_map_url = "https://example.com/sitemap.xml",
            s3_bucket = "some-bucket",
            check_valid = False,
        )._analyze_site_map(' '.join(urls), "https://www.google.com/gmail/sitemap.xml")
        results = [result[0][0] for result in capture.call_args_list]
        self.assertEqual(results.sort(), urls.sort())