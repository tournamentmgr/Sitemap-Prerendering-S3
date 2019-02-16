# pylint: disable=C0111,E1101,W0212
from unittest import TestCase
from unittest.mock import patch, Mock

# External
import responses

# Internal
from prerender.prerender import Prerender


@patch.object(Prerender, '_check_valid_xml', new=Mock())
class PrerenderTestCase(TestCase):

    @staticmethod
    def get_test_xml(urls) -> str:
        xml_string = "<urlset>"
        for item in urls:
            xml_string += f"<url><loc>{item}</loc></url>"
        xml_string += "</urlset>"
        return xml_string

    def test_request_local(self):
        prerender = Prerender(
            robots_url="https://example.com",
            s3_bucket="some-bucket",
        )
        self.assertEqual(prerender.bucket, "some-bucket")

    def test_domain_with_subdomain(self):
        prerender = Prerender(
            robots_url="https://subdomain.example.com/robots.txt",
            s3_bucket="some-bucket",
        )
        self.assertEqual(prerender.domain, "subdomain.example.com")

    @patch('botocore.client.BaseClient._make_api_call')
    def test_upload_to_s3(self, boto_mock):
        boto_mock.side_effect = [{"VersionId": 1,
                                  "ResponseMetadata": {"HTTPStatusCode": 200}}]
        response = Prerender(
            robots_url="https://subdomain.example.com/robots.txt",
            s3_bucket="some-bucket",
        )._archive_content(
            file_name="test", response="some text"
        )
        self.assertEqual(response['VersionId'], 1)

    @responses.activate
    @patch.object(Prerender, 'capture_page_and_upload')
    def test_capture_calls(self, prerender):
        responses.add(responses.GET, 'https://subdomain.example.com/robots.txt',
                      body="Sitemap: https://example.com/sitemap.xml", status=200)
        responses.add(responses.GET, 'https://example.com/sitemap.xml',
                      body=self.get_test_xml(["https://example.com", "https://example.com/page1"]),
                      status=200)

        # .json.return_value = {}
        prerender.return_value = None
        Prerender(
            robots_url="https://subdomain.example.com/robots.txt",
            s3_bucket="some-bucket",
        ).capture()
        self.assertEqual(len(responses.calls), 2)


    @patch.object(Prerender, '_archive_content')
    @patch('scraper.scraper.query_url')
    def test_html_query_local(self, query, archive):
        query.return_value = "test"
        archive.return_value = ""
        Prerender(
            robots_url="https://example.com/sitemap.xml",
            s3_bucket="some-bucket",
        ).capture_page_and_upload("https:/example.com/home/test/")
        _, kwargs = archive.call_args_list[0]
        self.assertEqual(kwargs['file_name'], "home/test")
        self.assertEqual(kwargs['response'], "test")

    @patch.dict('os.environ', {})
    @patch.object(Prerender, 'capture_page_and_upload')
    def test_analyze_site_to_get_urls(self, capture):
        urls = ["https://example.com/page1", "http://example.com/page2"]
        capture.return_value = None
        Prerender(
            robots_url="https://example.com/robots.txt",
            s3_bucket="some-bucket",
        )._analyze_site_map(self.get_test_xml(urls), "https://example.com/sitemap.xml")
        results = [result[0][0] for result in capture.call_args_list]
        self.assertEqual(results.sort(), urls.sort())

    @patch.object(Prerender, '_archive_content')
    @patch('scraper.scraper.query_url')
    def test_auth_passed(self, query, archive):
        query.return_value = "test"
        archive.return_value = ""
        Prerender(
            robots_url="https://example.com/sitemap.xml",
            s3_bucket="some-bucket",
            auth=('test', 'pass')
        ).capture_page_and_upload("https:/example.com/home/test/")
        _, kwargs = query.call_args_list[0]
        self.assertEqual(kwargs['username'], "test")
        self.assertEqual(kwargs['password'], "pass")
