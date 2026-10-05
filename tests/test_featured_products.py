"""
Unit tests for the Featured Products section, assets, and modular components.
"""
import os
import unittest
import urllib.parse
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProductCardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_featured_section = False
        self.cards = []
        self.current_card = None
        self.current_tag = None
        self.text_buffer = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.current_tag = tag

        if tag == 'section' and attr_dict.get('id') == 'featured-products':
            self.in_featured_section = True

        if self.in_featured_section and tag == 'article' and 'bento-card' in attr_dict.get('class', ''):
            self.current_card = {
                'class': attr_dict.get('class', ''),
                'title': '',
                'desc': '',
                'images': [],
                'links': []
            }
            self.cards.append(self.current_card)

        if self.in_featured_section and self.current_card is not None:
            if tag == 'img' and 'src' in attr_dict:
                self.current_card['images'].append(attr_dict['src'])
            if tag == 'a' and 'href' in attr_dict:
                self.current_card['links'].append({
                    'href': attr_dict['href'],
                    'class': attr_dict.get('class', '')
                })

    def handle_endtag(self, tag):
        if tag == 'section' and self.in_featured_section:
            self.in_featured_section = False
        self.current_tag = None

    def handle_data(self, data):
        cleaned = data.strip()
        if not cleaned or not self.in_featured_section or self.current_card is None:
            return

        # Check for title or desc elements
        if any(keyword in self.current_card['class'] for keyword in ['card-hibiscus', 'card-reetha', 'card-bhringraj', 'card-amla', 'card-hibiscus-powder', 'card-shikakai']):
            if cleaned in ['Reetha', 'Bhringraj', 'Amla', 'Hibiscus', 'Shikakai'] or 'Amla, Reetha, Shikakai, Bhringraj & Hibiscus' in cleaned:
                self.current_card['title'] = cleaned


class TestFeaturedProducts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.join(WORKSPACE_DIR, 'index.html')
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

        parser = ProductCardParser()
        parser.feed(cls.html_content)
        cls.cards = parser.cards

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

    def test_featured_products_count(self):
        """Should have 6 product cards in the featured products bento grid (Combo + 5 botanical cards)."""
        self.assertEqual(len(self.cards), 6, f"Expected 6 featured product cards, found {len(self.cards)}")

    def test_featured_product_names(self):
        """Should contain 5-in-1 Combo (Amla, Reetha, Shikakai, Bhringraj & Hibiscus), Reetha, Bhringraj, Amla, Hibiscus, Shikakai."""
        titles = " ".join([card['title'] for card in self.cards])
        expected_titles = ['Amla', 'Reetha', 'Bhringraj', 'Shikakai', 'Hibiscus']
        for expected in expected_titles:
            self.assertIn(expected, titles, f"Missing product mention: {expected}")

    def test_featured_product_image_paths_exist(self):
        """All images referenced in the 5 product cards must exist on the local file system."""
        for card in self.cards:
            self.assertGreater(len(card['images']), 0, f"Card {card['title']} has no images")
            for img_src in card['images']:
                decoded_src = urllib.parse.unquote(img_src)
                full_path = os.path.join(WORKSPACE_DIR, decoded_src.replace('/', os.sep))
                self.assertTrue(
                    os.path.exists(full_path),
                    f"Image path does not exist: {full_path} (from src '{img_src}')"
                )

    def test_featured_products_background_and_leaves(self):
        """Verify #F7F7ED background color and the 4 botanical decorative leaf images."""
        css_path = os.path.join(WORKSPACE_DIR, 'css', 'featured-products.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('#F7F7ED', css)
        self.assertIn('.featured-bg-leaf', css)

        expected_leaves = [
            'product_lefttop.png',
            'product_leftbuttom.png',
            'product_righttop.png',
            'product_rightbuttom.png'
        ]
        for leaf in expected_leaves:
            self.assertIn(leaf, self.html_content)
            full_path = os.path.join(WORKSPACE_DIR, leaf)
            self.assertTrue(os.path.exists(full_path), f"Leaf asset missing: {full_path}")

    def test_css_and_js_integration(self):
        """Check that featured-products.css and featuredProducts.js are linked."""
        self.assertIn('css/featured-products.css', self.html_content)
        main_js_path = os.path.join(WORKSPACE_DIR, 'js', 'main.js')
        with open(main_js_path, 'r', encoding='utf-8') as f:
            main_js_content = f.read()
        self.assertIn('FeaturedProductsManager', main_js_content)


if __name__ == '__main__':
    unittest.main()
