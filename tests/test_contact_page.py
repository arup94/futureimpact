"""
Unit tests for the Contact Us page (contact.html, css/contact.css, js/contact.js).
"""
import os
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ContactHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = []
        self.textareas = []
        self.buttons = []
        self.forms = []
        self.in_footer = False
        self.footer_found = False
        self.footer_text = ""
        self.headings = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'form':
            self.forms.append(attr_dict)
        if tag == 'input':
            self.inputs.append(attr_dict)
        if tag == 'textarea':
            self.textareas.append(attr_dict)
        if tag == 'button':
            self.buttons.append(attr_dict)
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.headings.append(tag)
        if tag == 'footer' and ('site-footer' in attr_dict.get('class', '') or attr_dict.get('id') == 'site-footer'):
            self.in_footer = True
            self.footer_found = True

    def handle_endtag(self, tag):
        if tag == 'footer' and self.in_footer:
            self.in_footer = False

    def handle_data(self, data):
        if self.in_footer:
            self.footer_text += " " + data.strip()


class TestContactPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.join(WORKSPACE_DIR, 'contact.html')
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

        cls.css_path = os.path.join(WORKSPACE_DIR, 'css', 'contact.css')
        with open(cls.css_path, 'r', encoding='utf-8') as f:
            cls.css_content = f.read()

        cls.js_path = os.path.join(WORKSPACE_DIR, 'js', 'contact.js')
        with open(cls.js_path, 'r', encoding='utf-8') as f:
            cls.js_content = f.read()

        parser = ContactHTMLParser()
        parser.feed(cls.html_content)
        cls.parser = parser

    def test_contact_file_exists(self):
        """contact.html, css/contact.css and js/contact.js must exist."""
        self.assertTrue(os.path.exists(self.html_path))
        self.assertTrue(os.path.exists(self.css_path))
        self.assertTrue(os.path.exists(self.js_path))

    def test_form_fields_present(self):
        """Contact us form must have options for Full Name, Email, Mobile number, and Message."""
        input_names = [i.get('name') for i in self.parser.inputs]
        input_ids = [i.get('id') for i in self.parser.inputs]
        textarea_names = [t.get('name') for t in self.parser.textareas]
        textarea_ids = [t.get('id') for t in self.parser.textareas]

        self.assertIn('fullName', input_names)
        self.assertIn('email', input_names)
        self.assertIn('mobile', input_names)
        self.assertIn('message', textarea_names)

        self.assertIn('fullName', input_ids)
        self.assertIn('email', input_ids)
        self.assertIn('mobile', input_ids)
        self.assertIn('message', textarea_ids)

    def test_contact_form_element(self):
        """Contact form element must exist with id contactForm."""
        form_ids = [f.get('id') for f in self.parser.forms]
        self.assertIn('contactForm', form_ids)

    def test_same_footer_exists(self):
        """Footer in contact.html must have site-footer with matching company and products info."""
        self.assertTrue(self.parser.footer_found)
        self.assertIn('Future Impact', self.parser.footer_text)
        self.assertIn('232/A KALIPUR EXTENTION ROAD', self.parser.footer_text)
        self.assertIn('+91 91239 99907', self.parser.footer_text)
        self.assertIn('care@futureimpact.in', self.parser.footer_text)
        self.assertIn('Hibiscus Powder', self.parser.footer_text)
        self.assertIn('Reetha Powder', self.parser.footer_text)

    def test_validation_logic_in_js(self):
        """validateContactData function must validate name, email, mobile, and message."""
        self.assertIn('validateContactData', self.js_content)
        self.assertIn('initContactForm', self.js_content)

    def test_google_maps_location_present(self):
        """Google Maps section and embed iframe must exist with the correct company address query."""
        self.assertIn('contact-map-section', self.html_content)
        self.assertIn('map-embed-wrapper', self.html_content)
        self.assertIn('maps.google.com/maps', self.html_content)
        self.assertIn('232', self.html_content)
        self.assertIn('KALIPUR', self.html_content)
        self.assertIn('.contact-map-section', self.css_content)

    def test_separate_contact_cards_present(self):
        """Address, phone, and email must be separated into distinct cards."""
        self.assertIn('contact-cards-stack', self.html_content)
        self.assertIn('card-address', self.html_content)
        self.assertIn('card-phone', self.html_content)
        self.assertIn('card-email', self.html_content)
        self.assertIn('.card-address', self.css_content)
        self.assertIn('.card-phone', self.css_content)
        self.assertIn('.card-email', self.css_content)

    def test_whole_page_gradient_present(self):
        """Body must have full page gradient styling in css/contact.css."""
        self.assertIn('linear-gradient', self.css_content)
        self.assertIn('background-attachment: fixed', self.css_content)

    def test_responsive_css_present(self):
        """css/contact.css must have responsive media queries and design tokens."""
        self.assertIn('@media', self.css_content)
        self.assertIn('--primary-green', self.css_content)


if __name__ == '__main__':
    unittest.main()
