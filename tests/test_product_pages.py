"""
Unit tests for dedicated product detail pages, suggested botanicals, brand footers, and Amazon links.
"""
import os
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestProductDetailPages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.products_dir = os.path.join(WORKSPACE_DIR, 'products')
        cls.index_path = os.path.join(WORKSPACE_DIR, 'index.html')
        with open(cls.index_path, 'r', encoding='utf-8') as f:
            cls.index_content = f.read()

        cls.product_files = {
            'amla': os.path.join(cls.products_dir, 'amla.html'),
            'reetha': os.path.join(cls.products_dir, 'reetha.html'),
            'hibiscus': os.path.join(cls.products_dir, 'hibiscus.html'),
            'shikakai': os.path.join(cls.products_dir, 'shikakai.html'),
            'bhringraj': os.path.join(cls.products_dir, 'bhringraj.html'),
            'combo': os.path.join(cls.products_dir, 'combo.html')
        }

        cls.product_contents = {}
        for name, path in cls.product_files.items():
            with open(path, 'r', encoding='utf-8') as f:
                cls.product_contents[name] = f.read()

    def test_all_product_pages_exist(self):
        """Ensure all 5 dedicated botanical product pages plus 5-in-1 combo page exist."""
        for name, path in self.product_files.items():
            self.assertTrue(os.path.exists(path), f"Product page {name}.html does not exist at {path}")

    def test_product_pages_have_identical_brand_footer_elements(self):
        """Ensure each product page footer matches index.html footer elements."""
        required_footer_snippets = [
            'class="site-footer"',
            'id="site-footer"',
            'footer-bg-svg-wrap',
            'footer-wave-divider',
            'Future Impact',
            '232/A KALIPUR EXTENTION ROAD, HARIDEVPUR, KOLKATA- 700082',
            '+91 91239 99907',
            'care@futureimpact.in',
            'Contact Us',
            '../contact.html',
            'https://www.facebook.com/profile.php?id=61590463904035',
            'https://www.instagram.com/futureimpact_official/?hl=en',
            '&copy; 2026 Future Impact. All Rights Reserved.'
        ]
        for name, content in self.product_contents.items():
            for snippet in required_footer_snippets:
                self.assertIn(
                    snippet, content,
                    f"Product page {name}.html missing footer element: {snippet}"
                )

    def test_amla_suggests_remaining_botanicals_below_usage(self):
        """Ensure amla.html suggests Bhringraj, Hibiscus, Reetha, and Shikakai below usage."""
        content = self.product_contents['amla']
        usage_pos = content.find('class="usage-box"')
        suggest_pos = content.find('class="suggested-products-section"')
        self.assertNotEqual(usage_pos, -1, "amla.html missing usage-box")
        self.assertNotEqual(suggest_pos, -1, "amla.html missing suggested-products-section")
        self.assertGreater(suggest_pos, usage_pos, "Suggested section must be below usage-box")

        suggested_block = content[suggest_pos:]
        self.assertIn('bhringraj.html', suggested_block)
        self.assertIn('Bhringraj Powder', suggested_block)
        self.assertIn('hibiscus.html', suggested_block)
        self.assertIn('Hibiscus Powder', suggested_block)
        self.assertIn('reetha.html', suggested_block)
        self.assertIn('Reetha Powder', suggested_block)
        self.assertIn('shikakai.html', suggested_block)
        self.assertIn('Shikakai Powder', suggested_block)

    def test_bhringraj_suggests_remaining_botanicals_below_usage(self):
        """Ensure bhringraj.html suggests Amla, Hibiscus, Reetha, and Shikakai below usage."""
        content = self.product_contents['bhringraj']
        usage_pos = content.find('class="usage-box"')
        suggest_pos = content.find('class="suggested-products-section"')
        self.assertGreater(suggest_pos, usage_pos)

        suggested_block = content[suggest_pos:]
        self.assertIn('amla.html', suggested_block)
        self.assertIn('Amla Fruit Powder', suggested_block)
        self.assertIn('hibiscus.html', suggested_block)
        self.assertIn('Hibiscus Powder', suggested_block)
        self.assertIn('reetha.html', suggested_block)
        self.assertIn('Reetha Powder', suggested_block)
        self.assertIn('shikakai.html', suggested_block)
        self.assertIn('Shikakai Powder', suggested_block)

    def test_hibiscus_suggests_remaining_botanicals_below_usage(self):
        """Ensure hibiscus.html suggests Amla, Bhringraj, Reetha, and Shikakai below usage."""
        content = self.product_contents['hibiscus']
        usage_pos = content.find('class="usage-box"')
        suggest_pos = content.find('class="suggested-products-section"')
        self.assertGreater(suggest_pos, usage_pos)

        suggested_block = content[suggest_pos:]
        self.assertIn('amla.html', suggested_block)
        self.assertIn('Amla Fruit Powder', suggested_block)
        self.assertIn('bhringraj.html', suggested_block)
        self.assertIn('Bhringraj Powder', suggested_block)
        self.assertIn('reetha.html', suggested_block)
        self.assertIn('Reetha Powder', suggested_block)
        self.assertIn('shikakai.html', suggested_block)
        self.assertIn('Shikakai Powder', suggested_block)

    def test_reetha_suggests_remaining_botanicals_below_usage(self):
        """Ensure reetha.html suggests Amla, Bhringraj, Hibiscus, and Shikakai below usage."""
        content = self.product_contents['reetha']
        usage_pos = content.find('class="usage-box"')
        suggest_pos = content.find('class="suggested-products-section"')
        self.assertGreater(suggest_pos, usage_pos)

        suggested_block = content[suggest_pos:]
        self.assertIn('amla.html', suggested_block)
        self.assertIn('Amla Fruit Powder', suggested_block)
        self.assertIn('bhringraj.html', suggested_block)
        self.assertIn('Bhringraj Powder', suggested_block)
        self.assertIn('hibiscus.html', suggested_block)
        self.assertIn('Hibiscus Powder', suggested_block)
        self.assertIn('shikakai.html', suggested_block)
        self.assertIn('Shikakai Powder', suggested_block)

    def test_shikakai_suggests_remaining_botanicals_below_usage(self):
        """Ensure shikakai.html suggests Amla, Bhringraj, Hibiscus, and Reetha below usage."""
        content = self.product_contents['shikakai']
        usage_pos = content.find('class="usage-box"')
        suggest_pos = content.find('class="suggested-products-section"')
        self.assertGreater(suggest_pos, usage_pos)

        suggested_block = content[suggest_pos:]
        self.assertIn('amla.html', suggested_block)
        self.assertIn('Amla Fruit Powder', suggested_block)
        self.assertIn('bhringraj.html', suggested_block)
        self.assertIn('Bhringraj Powder', suggested_block)
        self.assertIn('hibiscus.html', suggested_block)
        self.assertIn('Hibiscus Powder', suggested_block)
        self.assertIn('reetha.html', suggested_block)
        self.assertIn('Reetha Powder', suggested_block)

    def test_combo_suggests_all_individual_botanicals_below_usage(self):
        """Ensure combo.html suggests all 5 individual botanicals below usage in a single row."""
        content = self.product_contents['combo']
        usage_pos = content.find('class="usage-box"')
        suggest_pos = content.find('class="suggested-products-section"')
        self.assertGreater(suggest_pos, usage_pos)

        suggested_block = content[suggest_pos:]
        self.assertIn('combo-5-grid', suggested_block)
        self.assertIn('amla.html', suggested_block)
        self.assertIn('bhringraj.html', suggested_block)
        self.assertIn('hibiscus.html', suggested_block)
        self.assertIn('reetha.html', suggested_block)
        self.assertIn('shikakai.html', suggested_block)

    def test_stylesheet_links_in_product_pages(self):
        """Ensure product pages link both suggested-products.css and footer.css."""
        for name, content in self.product_contents.items():
            self.assertIn('css/suggested-products.css', content, f"{name}.html missing suggested-products.css")
            self.assertIn('css/footer.css', content, f"{name}.html missing footer.css")

    def test_index_page_view_product_links(self):
        """Ensure index.html contains View Product links to all featured cards."""
        expected_links = [
            'products/combo.html',
            'products/reetha.html',
            'products/bhringraj.html',
            'products/amla.html',
            'products/hibiscus.html',
            'products/shikakai.html'
        ]
        for link in expected_links:
            self.assertIn(link, self.index_content, f"Index page missing link to {link}")

    def test_index_page_buy_amazon_links(self):
        """Ensure index.html contains Buy buttons with corresponding Amazon shortlinks."""
        expected_amazon_links = [
            'https://amzn.in/d/0idDxXD1',
            'https://amzn.in/d/00Bro9dT',
            'https://amzn.in/d/09oEJZaX',
            'https://amzn.in/d/06UqzjGl',
            'https://amzn.in/d/08tYjIGo',
            'https://amzn.in/d/0fsECK77'
        ]
        for url in expected_amazon_links:
            self.assertIn(url, self.index_content, f"Index page missing Amazon link {url}")

    def test_file_line_counts_strictly_under_500(self):
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


if __name__ == '__main__':
    unittest.main()
