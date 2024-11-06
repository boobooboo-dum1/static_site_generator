import unittest

from generate import extract_title


class TestGenerate(unittest.TestCase):
    def test_extract_title(self):
        text = "# Valid header"
        expected = "Valid header"
        result = extract_title(text)

        self.assertEqual(result, expected)

    def test_extract_title_leading_space(self):
        text = "#  Valid header "
        expected = "Valid header"
        result = extract_title(text)

        self.assertEqual(result, expected)

    def test_extract_title_multiline(self):
        text = "# Valid header\n And some other line"
        expected = "Valid header"
        result = extract_title(text)

        self.assertEqual(result, expected)

    def test_extract_title_invalid(self):
        text = "## Inalid header"
        with self.assertRaises(ValueError):
            extract_title(text)
