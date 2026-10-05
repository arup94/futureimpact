"""
Unit tests for the Brand Footer section (#1b301e), addresses, products, queries, socials, and rules.
"""
import os
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FooterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_footer = False
        self.footer_found = False
        self.footer_text = ""
        self.links = []
        self.images = []
        self.svg_count = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'footer' and ('site-footer' in attr_dict.get('class', '') or attr_dict.get('id') == 'site-footer'):
            self.in_footer = True
            self.footer_found = True

        if self.in_footer:
            if tag == 'a' and 'href' in attr_dict:
                self.links.append({
                    'href': attr_dict['href'],
                    'class': attr_dict.get('class', ''),
                    'aria_label': attr_dict.get('aria-label', '')
                })
            if tag == 'img' and 'src' in attr_dict:
                self.images.append(attr_dict['src'])
            if tag == 'svg':
                self.svg_count += 1

    def handle_endtag(self, tag):
        if tag == 'footer' and self.in_footer:
            self.in_footer = False

    def handle_data(self, data):
        if self.in_footer:
            self.footer_text += " " + data.strip()


class TestBrandFooter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.join(WORKSPACE_DIR, 'index.html')
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

        cls.css_path = os.path.join(WORKSPACE_DIR, 'css', 'footer.css')
        with open(cls.css_path, 'r', encoding='utf-8') as f:
            cls.css_content = f.read()

        parser = FooterParser()
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

    def test_footer_exists(self):
        """Footer with class site-footer and id site-footer must exist."""
        self.assertTrue(self.parser.footer_found)

    def test_footer_background_color_code(self):
        """Footer CSS must explicitly use color code #1b301e."""
        self.assertIn('#1b301e', self.css_content)

    def test_company_name_and_logo(self):
        """Footer must include company logo and name Future Impact."""
        self.assertIn('Future Impact', self.parser.footer_text)
        self.assertTrue(any('Logo1.png' in img or 'LOGO.png' in img for img in self.parser.images))

    def test_company_address_and_contacts(self):
        """Address, phone and email must be present in footer text."""
        normalized_text = ' '.join(self.parser.footer_text.split())
        self.assertIn('232/A KALIPUR EXTENTION ROAD, HARIDEVPUR, KOLKATA- 700082', normalized_text)
        self.assertIn('+91 91239 99907', normalized_text)
        self.assertIn('care@futureimpact.in', normalized_text)

        # Contact click links
        hrefs = [l['href'] for l in self.parser.links]
        self.assertTrue(any('tel:+919123999907' in h for h in hrefs))
        self.assertTrue(any('mailto:care@futureimpact.in' in h for h in hrefs))

    def test_five_products_in_middle_column(self):
        """Must show company's five product names."""
        products = [
            'Hibiscus Powder',
            'Reetha Powder',
            'Bhringraj Powder',
            'Amla Fruit Powder',
            'Shikakai Powder'
        ]
        for prod in products:
            self.assertIn(prod, self.parser.footer_text)

    def test_formal_query_form_link(self):
        """Must show Contact Us link to contact.html."""
        self.assertIn('Contact Us', self.parser.footer_text)
        hrefs = [l['href'] for l in self.parser.links]
        self.assertTrue(any('contact.html' in h for h in hrefs))

    def test_social_media_links(self):
        """Must show Facebook and Instagram links with proper labels."""
        labels = [l['aria_label'] for l in self.parser.links]
        hrefs = [l['href'] for l in self.parser.links]
        self.assertTrue(any('Facebook' in lbl for lbl in labels))
        self.assertTrue(any('Instagram' in lbl for lbl in labels))
        self.assertTrue(any('facebook.com' in h for h in hrefs))
        self.assertTrue(any('instagram.com' in h for h in hrefs))

    def test_footer_background_svg(self):
        """Verify the dynamic ambient SVG background is rendered and styled in footer."""
        self.assertIn('footer-bg-svg-wrap', self.html_content)
        self.assertIn('.footer-bg-svg-wrap', self.css_content)
        self.assertIn('footer-gradient', self.html_content)

    def test_svg_icons_present(self):
        """Address, phone, email, query arrow, and socials must all have SVG icons."""
        self.assertGreaterEqual(self.parser.svg_count, 5)


if __name__ == '__main__':
    unittest.main()
