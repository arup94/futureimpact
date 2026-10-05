"""
Unit tests for Our Specialized Product section, including authentic SVG icons from futureimpact.in.
"""
import os
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SpecializedProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_section = False
        self.cards = []
        self.current_card = None
        self.current_icon_svg = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'section' and attr_dict.get('id') == 'specialized-products':
            self.in_section = True

        if self.in_section:
            if tag == 'article' and 'product-card' in attr_dict.get('class', ''):
                self.current_card = {'headings': [], 'subheadings': [], 'svg_viewbox': None, 'svg_count': 0}
            if self.current_card is not None and tag == 'svg':
                self.current_card['svg_count'] += 1
                if 'viewbox' in attr_dict:
                    self.current_card['svg_viewbox'] = attr_dict['viewbox']

    def handle_endtag(self, tag):
        if tag == 'article' and self.current_card is not None:
            self.cards.append(self.current_card)
            self.current_card = None
        if tag == 'section' and self.in_section:
            self.in_section = False

    def handle_data(self, data):
        text = data.strip()
        if not text or self.current_card is None:
            return
        if text in ['Hair Care', 'Skin Care', 'Lip Care', 'Natural Willing']:
            self.current_card['headings'].append(text)
        elif text in ['Always the best', 'Expect more by default', "We're here to help", 'Ready to impress']:
            self.current_card['subheadings'].append(text)


class TestSpecializedProductIcons(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.join(WORKSPACE_DIR, 'index.html')
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

        parser = SpecializedProductParser()
        parser.feed(cls.html_content)
        cls.parser = parser

    def test_specialized_products_count(self):
        """Ensure all 4 specialized product cards are present."""
        self.assertEqual(len(self.parser.cards), 4, "Expected 4 specialized product cards")

    def test_hair_care_card_image_and_background(self):
        """Verify Hair Care uses Hair.png photo and custom card background #F3F8E6."""
        hair_card = self.parser.cards[0]
        self.assertIn('Hair Care', hair_card['headings'])
        self.assertIn('Always the best', hair_card['subheadings'])
        self.assertIn('Hair.png', self.html_content)
        self.assertIn('Nourish your hair naturally with time-tested herbs', self.html_content)
        self.assertTrue(os.path.exists(os.path.join(WORKSPACE_DIR, 'Hair.png')))

        css_path = os.path.join(WORKSPACE_DIR, 'css', 'components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.card-hair-care', css)
        self.assertIn('#F3F8E6', css)

    def test_skin_care_card_image_and_background(self):
        """Verify Skin Care uses Skin.png photo and custom card background #FBF3F1."""
        skin_card = self.parser.cards[1]
        self.assertIn('Skin Care', skin_card['headings'])
        self.assertIn('Expect more by default', skin_card['subheadings'])
        self.assertIn('Skin.png', self.html_content)
        self.assertIn('Reveal natural radiance with pure botanical care', self.html_content)
        self.assertTrue(os.path.exists(os.path.join(WORKSPACE_DIR, 'Skin.png')))

        css_path = os.path.join(WORKSPACE_DIR, 'css', 'components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.card-skin-care', css)
        self.assertIn('#FBF3F1', css)

    def test_lip_care_card_image_and_background(self):
        """Verify Lip Care uses Lip.png photo and custom card background #FBF5EE."""
        lip_card = self.parser.cards[2]
        self.assertIn('Lip Care', lip_card['headings'])
        self.assertIn("We're here to help", lip_card['subheadings'])
        self.assertIn('Lip.png', self.html_content)
        self.assertIn('Keep your lips naturally soft, smooth and nourished', self.html_content)
        self.assertTrue(os.path.exists(os.path.join(WORKSPACE_DIR, 'Lip.png')))

        css_path = os.path.join(WORKSPACE_DIR, 'css', 'components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.card-lip-care', css)
        self.assertIn('#FBF5EE', css)

    def test_natural_willing_card_image_and_background(self):
        """Verify Natural Willing uses NaturalWilling.png photo and custom card background #F1F7E9."""
        natural_card = self.parser.cards[3]
        self.assertIn('Natural Willing', natural_card['headings'])
        self.assertIn('Ready to impress', natural_card['subheadings'])
        self.assertIn('NaturalWilling.png', self.html_content)
        self.assertIn('Pure. Natural. Effective. Made from the finest herbs', self.html_content)
        self.assertTrue(os.path.exists(os.path.join(WORKSPACE_DIR, 'NaturalWilling.png')))

        css_path = os.path.join(WORKSPACE_DIR, 'css', 'components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.card-natural-willing', css)
        self.assertIn('#F1F7E9', css)

    def test_specialized_title_accent_color(self):
        """Ensure 'Specialized' has accent highlight span with #3B650A in CSS."""
        self.assertIn('<span class="text-accent-highlight">Specialized</span>', self.html_content)
        css_path = os.path.join(WORKSPACE_DIR, 'css', 'components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.text-accent-highlight', css)
        self.assertIn('#3B650A', css)

    def test_specialized_products_background_leaves(self):
        """Ensure top_left.png, bottom_left.png, and bottom_right.png are referenced and exist."""
        expected_leaves = ['top_left.png', 'bottom_left.png', 'bottom_right.png']
        for leaf in expected_leaves:
            self.assertIn(leaf, self.html_content, f"Missing background leaf reference: {leaf}")
            full_path = os.path.join(WORKSPACE_DIR, leaf)
            self.assertTrue(os.path.exists(full_path), f"Background leaf file not found: {full_path}")

        css_path = os.path.join(WORKSPACE_DIR, 'css', 'components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.specialized-bg-leaf', css)
        self.assertIn('.leaf-top-left', css)
        self.assertIn('.leaf-bottom-left', css)
        self.assertIn('.leaf-bottom-right', css)

    def test_file_line_counts_strictly_under_500(self):
        """Ensure all project files remain strictly <= 500 lines."""
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


if __name__ == '__main__':
    unittest.main()

