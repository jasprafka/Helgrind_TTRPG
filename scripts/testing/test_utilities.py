"""Unittests for utilities.py. Python unittests should not be run directly! Run them using run_test.py."""

import unittest
import subprocess
from unittest import mock
import utilities

@mock.patch('builtins.print', mock.Mock(auto_spec=True))
class TestRunCommand(unittest.TestCase):
    """Test cases for run_command()."""

    def setUp(self) -> None:
        """Setup, gets run before each test. Use to configure test environment."""
        self._check_call = subprocess.check_call
        subprocess.check_call = mock.Mock(auto_spec=True)

    def tearDown(self) -> None:
        """Teardown, run after each test. Use to reset test environment."""
        subprocess.check_call = self._check_call
    
    def test_run_command(self) -> None:
        """Test for run_command()."""
        utilities.run_command('test')
        subprocess.check_call.assert_called_once()
