"""
Unit tests for 'The futureimpact Promise' section, icons, typography, and constraints.
"""
import os
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PromiseSectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_promise_section = False
        self.section_found = False
        self.main_title = ""
        self.cards = []
        self.current_card = None
        self.current_tag = None
        self.capture_title = False
        self.capture_heading = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.current_tag = tag

        if tag == 'section' and attr_dict.get('id') == 'brand-promise':
            self.in_promise_section = True
            self.section_found = True

        if self.in_promise_section:
            if tag == 'h2' and 'promise-main-title' in attr_dict.get('class', ''):
                self.capture_title = True

            if tag == 'article' and 'promise-card' in attr_dict.get('class', ''):
                self.current_card = {
                    'heading': '',
                    'has_svg': False,
                    'desc': ''
                }
                self.cards.append(self.current_card)

            if self.current_card is not None and tag == 'svg' and 'promise-icon-svg' in attr_dict.get('class', ''):
                self.current_card['has_svg'] = True

            if self.current_card is not None and tag == 'h3' and 'promise-heading' in attr_dict.get('class', ''):
                self.capture_heading = True

    def handle_endtag(self, tag):
        if tag == 'h2' and self.capture_title:
            self.capture_title = False
        if tag == 'h3' and self.capture_heading:
            self.capture_heading = False
        if tag == 'section' and self.in_promise_section:
            self.in_promise_section = False
        self.current_tag = None

    def handle_data(self, data):
        cleaned = data.strip()
        if not cleaned:
            return

        if self.capture_title:
            self.main_title += (" " + cleaned) if self.main_title else cleaned

        if self.capture_heading and self.current_card is not None:
            self.current_card['heading'] += cleaned


class TestPromiseSection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.join(WORKSPACE_DIR, 'index.html')
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

        parser = PromiseSectionParser()
        parser.feed(cls.html_content)
        cls.parser = parser

    def test_file_line_counts_less_than_500(self):
        """Rule check: Make sure each file must not be more than 500 lines of code."""
        extensions = ('.js', '.css', '.html', '.py')
        for root, _, files in os.walk(WORKSPACE_DIR):
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                    self.assertLessEqual(
                        lines, 500,
                        f"File {file} exceeds 500 lines ({lines} lines)"
                    )

    def test_promise_section_exists(self):
        """The Future Impact Promise section must be present in index.html."""
        self.assertTrue(self.parser.section_found, "Brand promise section with id='brand-promise' not found.")
        self.assertTrue(
            "The Future Impact Promise" in self.parser.main_title or "The futureimpact Promise" in self.parser.main_title
        )

    def test_promise_card_count(self):
        """Must contain 10 promise cards (4 original + 6 clean formulation)."""
        self.assertEqual(len(self.parser.cards), 10, f"Expected 10 promise cards, found {len(self.parser.cards)}")

    def test_promise_card_headings(self):
        """Must contain all 10 requested headings."""
        headings = [card['heading'].replace('&amp;', '&').strip() for card in self.parser.cards]
        expected_headings = [
            'Ethically Sourced',
            '100% Pure & Natural',
            'Premium Quality',
            'Sustainable Packaging',
            'Preservative Free',
            'Ammonia Free',
            'Chemical Free',
            'Metalic Salts Free',
            'Pesticides Free',
            'PPD Free'
        ]
        for expected in expected_headings:
            self.assertIn(expected, headings, f"Missing promise heading: {expected}")

    def test_promise_cards_have_icons(self):
        """Every card must have a suitable SVG icon."""
        for card in self.parser.cards:
            self.assertTrue(card['has_svg'], f"Card '{card['heading']}' is missing an SVG icon.")

    def test_css_and_js_integration(self):
        """Check that promise.css and promiseSection.js are integrated."""
        self.assertIn('css/promise.css', self.html_content)
        main_js_path = os.path.join(WORKSPACE_DIR, 'js', 'main.js')
        with open(main_js_path, 'r', encoding='utf-8') as f:
            main_js_content = f.read()
        self.assertIn('PromiseSectionManager', main_js_content)

    def test_single_row_marquee_auto_scroll(self):
        """Verify single-row marquee container structure and CSS auto-scroll rules."""
        self.assertIn('promise-marquee-container', self.html_content)
        self.assertIn('promise-track', self.html_content)
        css_path = os.path.join(WORKSPACE_DIR, 'css', 'promise.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        self.assertIn('promiseAutoScroll', css_content)
        self.assertIn('animation-play-state: paused', css_content)
        self.assertIn('flex-wrap: nowrap', css_content)


if __name__ == '__main__':
    unittest.main()
