import os
import shutil
import tempfile
import unittest

from file_funcs import static_to_public, generate_page


class TestStaticToPublic(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_static_to_public_raises_exception_when_static_not_exists(self):
        with self.assertRaises(Exception) as context:
            static_to_public()
        self.assertEqual(str(context.exception), "Static directory does not exist")

    def test_static_to_public_copies_files(self):
        os.makedirs("static", exist_ok=True)
        with open("static/test.txt", "w") as f:
            f.write("test content")

        static_to_public()

        self.assertTrue(os.path.exists("public"))
        self.assertTrue(os.path.exists("public/test.txt"))
        with open("public/test.txt", "r") as f:
            self.assertEqual(f.read(), "test content")

    def test_static_to_public_removes_existing_public(self):
        os.makedirs("static", exist_ok=True)
        with open("static/new.txt", "w") as f:
            f.write("new content")

        os.makedirs("public", exist_ok=True)
        with open("public/old.txt", "w") as f:
            f.write("old content")

        static_to_public()

        self.assertTrue(os.path.exists("public"))
        self.assertFalse(os.path.exists("public/old.txt"))
        self.assertTrue(os.path.exists("public/new.txt"))

    def test_static_to_public_copies_nested_directories(self):
        os.makedirs("static/nested/dir", exist_ok=True)
        with open("static/nested/dir/file.txt", "w") as f:
            f.write("nested content")

        static_to_public()

        self.assertTrue(os.path.exists("public/nested/dir/file.txt"))


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_generate_page_creates_html_file(self):
        os.makedirs("content", exist_ok=True)
        os.makedirs("template", exist_ok=True)

        with open("content/test.md", "w") as f:
            f.write("# Test Title\n\nThis is a paragraph.")

        with open("template/page.html", "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

        generate_page("content/test.md", "template/page.html", "public/test.html")

        self.assertTrue(os.path.exists("public/test.html"))
        with open("public/test.html", "r") as f:
            content = f.read()
        self.assertIn("<title>Test Title</title>", content)
        self.assertIn("<p>", content)

    def test_generate_page_creates_nested_directories(self):
        os.makedirs("content", exist_ok=True)
        os.makedirs("template", exist_ok=True)

        with open("content/test.md", "w") as f:
            f.write("# Nested Page\n\nContent here.")

        with open("template/page.html", "w") as f:
            f.write("<html><body>{{ Title }} - {{ Content }}</body></html>")

        generate_page("content/test.md", "template/page.html", "public/nested/deep/test.html")

        self.assertTrue(os.path.exists("public/nested/deep/test.html"))

    def test_generate_page_with_bold_and_italic(self):
        os.makedirs("content", exist_ok=True)
        os.makedirs("template", exist_ok=True)

        with open("content/test.md", "w") as f:
            f.write("# Title\n\nThis has **bold** and _italic_ text.")

        with open("template/page.html", "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

        generate_page("content/test.md", "template/page.html", "public/test.html")

        with open("public/test.html", "r") as f:
            content = f.read()
        self.assertIn("<b>bold</b>", content)
        self.assertIn("<i>italic</i>", content)

    def test_generate_page_with_list(self):
        os.makedirs("content", exist_ok=True)
        os.makedirs("template", exist_ok=True)

        with open("content/test.md", "w") as f:
            f.write("# Title\n\n- Item 1\n- Item 2\n- Item 3")

        with open("template/page.html", "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

        generate_page("content/test.md", "template/page.html", "public/test.html")

        with open("public/test.html", "r") as f:
            content = f.read()
        self.assertIn("<ul>", content)
        self.assertIn("<li>Item 1</li>", content)


if __name__ == "__main__":
    unittest.main()
