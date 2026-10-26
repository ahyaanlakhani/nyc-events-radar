"""The NYC agent keeps only in-person events in New York City."""
import unittest
from datetime import datetime, timezone

from agent.radar import NYC_HINTS, normalize_event

NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


def raw(**overrides):
    value = dict(title='Agents meetup', start='2026-10-10T18:00:00-04:00', end=None,
                 venue='Brooklyn, New York', format='in-person', organizer='NYC Builders',
                 description='A talk about agents', is_free=True, cost='Free',
                 student_only=False, source_url='https://example.com/event', extraction='jsonld')
    value.update(overrides)
    return value


class NycScopeTests(unittest.TestCase):
    def test_in_person_event_in_new_york_is_kept(self):
        self.assertIsNotNone(normalize_event(raw(), NOW))

    def test_every_borough_hint_is_accepted(self):
        for venue in ('Queens, NY', 'The Bronx', 'Staten Island', 'Midtown Manhattan', 'NYC'):
            with self.subTest(venue=venue):
                self.assertIsNotNone(normalize_event(raw(venue=venue), NOW))

    def test_in_person_event_outside_nyc_is_rejected(self):
        self.assertIsNone(normalize_event(raw(venue='San Francisco, CA'), NOW))

    def test_hybrid_and_online_events_are_rejected(self):
        self.assertIsNone(normalize_event(raw(format='hybrid'), NOW))
        self.assertIsNone(normalize_event(raw(format='online', venue='New York (Zoom)'), NOW))

    def test_hint_list_is_lowercase_for_matching(self):
        self.assertTrue(all(hint == hint.lower() for hint in NYC_HINTS))


if __name__ == '__main__':
    unittest.main()
