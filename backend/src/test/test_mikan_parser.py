
import unittest
from unittest.mock import MagicMock, patch
from module.parser.analyser.mikan_parser import mikan_parser

class TestMikanCrash(unittest.TestCase):
    @patch("module.parser.analyser.mikan_parser.RequestContent")
    def test_get_content_returns_none(self, MockRequestContent):
        # Setup mock
        mock_req = MockRequestContent.return_value.__enter__.return_value
        
        # Mock HTML with poster
        html_content = """
        <html>
            <div class="bangumi-poster" style="background-image: url('/images/poster.jpg');"></div>
            <p class="bangumi-title"><a href="/Home/Bangumi/123">Test Anime</a></p>
        </html>
        """
        mock_req.get_html.return_value = html_content
        
        # Mock get_content returning None (image download failure)
        mock_req.get_content.return_value = None
        
        # This should NO LONGER crash, but return empty poster path
        poster_link, official_title = mikan_parser("https://mikanani.me/Home/Episode/123")
        
        self.assertEqual(poster_link, "")
        self.assertEqual(official_title, "Test Anime")

if __name__ == "__main__":
    unittest.main()
