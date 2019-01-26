from unittest import TestLoader, TextTestRunner, TestSuite
from prender_test import PrerenderTestCase
from scraper_test import ScraperTestCase
if __name__ == '__main__':
    TEST_CLASSES_TO_RUN = [
        PrerenderTestCase,
        ScraperTestCase
    ]

    LOADER = TestLoader()
    SUITES_LIST = [LOADER.loadTestsFromTestCase(
        test_class) for test_class in TEST_CLASSES_TO_RUN]
    BIG_SUITE = TestSuite(SUITES_LIST)
    exit(TextTestRunner(verbosity=2).run(BIG_SUITE).wasSuccessful())
