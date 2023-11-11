"""Unittests for setup.py. Python unittests should not be run directly! Run them using run_test.py."""

import setup
import unittest
from unittest import mock

class TestMain(unittest.TestCase):
    """Test cases for main()."""

    def setUp(self) -> None:
        """Setup, gets run before each test. Use to configure test environment."""
        self._logger = setup.LOGGER
        setup.LOGGER = mock.Mock(auto_spec=True)
        self.args = mock.Mock(auto_spec=True)

    def tearDown(self) -> None:
        """Teardown, run after each test. Use to reset test environment."""
        setup.LOGGER = self._logger
        self.args.reset_mock()
    
    @mock.patch('setup._validate_python_packages', mock.Mock(auto_spec=True))
    @mock.patch('setup._process_args', mock.Mock(auto_spec=True))
    def test_main(self) -> None:
        """Test for main()."""
        setup.main(self.args)
        setup._process_args.assert_called_once()
        setup._validate_python_packages.assert_called_once()

