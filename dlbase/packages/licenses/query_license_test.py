import unittest

from packages.licenses.query_license import get_license_url_for_packages

#TODO: add this unit test to the Kokoro CI
class MyTestCase(unittest.TestCase):
    def test_query_license(self):
        package_name1 = 'arrow'
        expected_url1 = 'https://raw.githubusercontent.com/apache/arrow/master/LICENSE.txt'
        self.assertEqual(get_license_url_for_packages(package_name1), expected_url1)

        package_name3 = 'conda_build'
        package_name4 = 'conda-build'
        expected_url2 = 'https://raw.githubusercontent.com/conda/conda-build/master/LICENSE.txt'
        self.assertEqual(get_license_url_for_packages(package_name3), expected_url2)
        self.assertEqual(get_license_url_for_packages(package_name4), expected_url2)


if __name__ == '__main__':
    unittest.main()

