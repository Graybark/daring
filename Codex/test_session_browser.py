"""Integrity checks for the private, offline session browser."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

import build_session_browser as browser


class SessionBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = browser.OUTPUT.read_text(encoding='utf-8')
        match = re.search(r'<script id="session-data" type="application/json">(.*?)</script>', cls.page, re.S)
        if match is None:
            raise AssertionError('Embedded archive data missing')
        cls.archive = json.loads(match.group(1))

    def test_generated_sessions_match_every_markdown_source(self) -> None:
        self.assertEqual(self.archive['sessions'], browser.build_data())
        numbers = [item['number'] for item in self.archive['sessions']]
        self.assertEqual(numbers, list(range(max(numbers), 0, -1)))
        self.assertGreaterEqual(len(numbers), 133)

    def test_reference_categories_and_source_links_preserved(self) -> None:
        expected = {'Characters', 'Encounters', 'Mythology', 'Factions', 'Culture and History', 'Locations'}
        self.assertEqual({item['category'] for item in self.archive['lore']}, expected)
        self.assertGreater(len(self.archive['lore']), 0)
        for item in self.archive['sessions']:
            self.assertTrue((browser.SESSION_DIR / item['file']).is_file(), item['file'])
        for item in self.archive['lore']:
            path = unquote(item['source'].split('#', 1)[0])
            self.assertTrue((browser.SESSION_DIR / path).is_file(), path)

    def test_default_and_count_are_dynamic(self) -> None:
        count = len(self.archive['sessions'])
        self.assertIn(f'{count} sessions', self.page)
        self.assertNotIn('byNumber.get(132)', self.page)
        self.assertIn('byNumber.get(number) || sessions[0]', self.page)
        self.assertNotIn('__SESSION_COUNT__', self.page)
        self.assertIn('Private GM archive', self.page)
        self.assertNotRegex(self.page, r'<script\b[^>]*\bsrc=["\']https?://')

    def test_session_133_does_not_include_unrevealed_preparation(self) -> None:
        item = next(item for item in self.archive['sessions'] if item['number'] == 133)
        self.assertIn('Into Death Heart', item['title'])
        self.assertIn('Yalda', item['text'])
        self.assertIn('Listener', item['text'])
        # The private GM record is intentionally not a browser session source.
        for secret in ('Morthakar', 'Quiet Tower', 'conduit ritual', 'vampiric minotaur'):
            self.assertNotIn(secret, item['text'])
        self.assertTrue((browser.ROOT / 'sessions/gm/session-133.md').is_file())

    def test_future_sessions_and_invalid_sequences(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for number in range(1, 135):
                (folder / f'DaringDozen{number:03d}.md').write_text(
                    f'# Session {number}\n\n**In-game date:** To confirm\n\n## Session notes\n\nTest record.\n\n---\n\n**Date played:** To confirm\n', encoding='utf-8')
            with patch.object(browser, 'SESSION_DIR', folder):
                self.assertEqual(browser.build_data()[0]['number'], 134)
                duplicate = folder / 'DaringDozen134_duplicate.md'
                duplicate.write_text('# Duplicate\n', encoding='utf-8')
                with self.assertRaises(ValueError):
                    browser.build_data()
                duplicate.unlink()
                (folder / 'DaringDozen024.md').unlink()
                with self.assertRaises(ValueError):
                    browser.build_data()


if __name__ == '__main__':
    unittest.main(verbosity=2)
