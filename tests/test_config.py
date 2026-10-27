"""The shipped config points the agent at New York City, in Eastern Time."""
import json
import unittest
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / 'agent' / 'config.json'


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(CONFIG.read_text(encoding='utf-8'))

    def test_timezone_is_eastern(self):
        self.assertEqual(self.cfg['timezone'], 'America/New_York')

    def test_listing_urls_are_new_york_and_in_person(self):
        self.assertTrue(self.cfg['listing_urls'])
        for url in self.cfg['listing_urls']:
            with self.subTest(url=url):
                self.assertIn('new-york', url)
                self.assertNotIn('online', url)

    def test_searches_mention_new_york_and_no_other_city(self):
        for query in self.cfg['queries'] + self.cfg['free_queries']:
            with self.subTest(query=query):
                lowered = query.lower()
                self.assertTrue(any(word in lowered for word in ('new york', 'nyc', 'nyu', 'columbia', 'cornell')))
                self.assertNotIn('karachi', lowered)


if __name__ == '__main__':
    unittest.main()
