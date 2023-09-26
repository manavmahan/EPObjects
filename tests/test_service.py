"""Tests the service by running it on Tausendpfund project."""
import unittest

from service.service import run_service


class TestService(unittest.TestCase):
    """Integration testing."""

    @classmethod
    def setUpClass(cls):
        """Run once before the entire test suite."""

    @classmethod
    def tearDownClass(cls):
        """Run once after the entire test suite."""

    def setUp(self):
        """Run before each test."""

    def tearDown(self):
        """Run after each test."""

    def test_tausendpfund(self):
        """Test on Tausendpfund."""
        run_service('tum-gni', 'tausendpfund-in')


if __name__ == "__main__":
    unittest.main()
