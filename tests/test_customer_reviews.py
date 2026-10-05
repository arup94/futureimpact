"""
Unit tests for the Customer Review section (Amazon customer review and 5-star rating).
"""
import os
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReviewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_review = False
        self.review_found = False
        self.review_text = ""
        self.star_count = 0
        self.section_classes = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'section' and (attr_dict.get('id') == 'customer-reviews' or 'customer-review-section' in attr_dict.get('class', '')):
            self.in_review = True
            self.review_found = True
            self.section_classes = attr_dict.get('class', '')

        if self.in_review:
            if tag == 'svg' and 'star-icon' in attr_dict.get('class', ''):
                self.star_count += 1

    def handle_endtag(self, tag):
        if tag == 'section' and self.in_review:
            self.in_review = False

    def handle_data(self, data):
        if self.in_review:
            self.review_text += " " + data.strip()


class TestCustomerReviews(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.join(WORKSPACE_DIR, 'index.html')
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

        cls.css_path = os.path.join(WORKSPACE_DIR, 'css', 'reviews.css')
        with open(cls.css_path, 'r', encoding='utf-8') as f:
            cls.css_content = f.read()

        parser = ReviewParser()
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

    def test_customer_review_section_exists_and_positioned_properly(self):
        """Ensure customer-reviews section exists below promise section and above footer."""
        self.assertTrue(self.parser.review_found, "Customer review section was not found")
        self.assertIn("customer-reviews", self.html_content)
        promise_pos = self.html_content.find('id="brand-promise"')
        review_pos = self.html_content.find('id="customer-reviews"')
        footer_pos = self.html_content.find('id="site-footer"')
        self.assertNotEqual(promise_pos, -1, "Promise section not found")
        self.assertNotEqual(review_pos, -1, "Customer reviews section not found")
        self.assertNotEqual(footer_pos, -1, "Footer section not found")
        self.assertLess(promise_pos, review_pos, "Customer review section must be below the promise section")
        self.assertLess(review_pos, footer_pos, "Customer review section must be above the footer section")

    def test_exact_customer_review_quote_present(self):
        """Ensure the exact customer review quote provided by the user is present."""
        expected_quote = (
            "Great product. It genuinely helped me. Far better from the cosmetics and chemicals. "
            "As per advice i have used it and my hair and scalp looks healthier."
        )
        self.assertIn(expected_quote, self.html_content, "Exact customer review quote is missing in HTML")

    def test_five_star_rating_present(self):
        """Verify five star rating is present and accurately counted."""
        self.assertEqual(self.parser.star_count, 5, f"Expected 5 star icons, found {self.parser.star_count}")
        self.assertIn("5.0 / 5.0", self.html_content)

    def test_amazon_customer_attribution(self):
        """Verify Amazon buyer attribution and verified badge are present."""
        self.assertIn("Amazon Customer", self.html_content)
        self.assertIn("Amazon Verified Purchase", self.html_content)

    def test_reviews_css_linked_and_styled(self):
        """Verify reviews.css is linked in index.html and contains appropriate styling."""
        self.assertIn('href="css/reviews.css"', self.html_content)
        self.assertIn('.customer-review-section', self.css_content)
        self.assertIn('.star-icon', self.css_content)
        self.assertIn('.review-card', self.css_content)


if __name__ == '__main__':
    unittest.main()
