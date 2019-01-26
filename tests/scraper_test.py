from unittest import TestCase
from unittest.mock import patch
from scraper.scraper import block_request

class ScraperTestCase(TestCase):

    @patch.dict('os.environ', {'ALLOWED_DOMAINS': "example.com"})
    def test_block_domain(self):
        request = block_request("subdomain.rejectme.com")
        self.assertTrue(request)
    
    @patch.dict('os.environ', {'ALLOWED_DOMAINS': "example.com"})
    def test_allow_domain(self):
        self.assertFalse(block_request("subdomain.example.com"))

    def test_allow_domain_if_unset(self):
        self.assertFalse(block_request("subdomain.example.com"))