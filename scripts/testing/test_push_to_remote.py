"""Unittests for push_to_remote.py. Python unittests should not be run directly! Run them using run_test.py."""

import push_to_remote
import run_test
import utilities
import unittest
from unittest import mock

@mock.patch('builtins.print', mock.Mock(auto_spec=True))
@mock.patch('push_to_remote.LOGGER', mock.Mock(auto_spec=True))
class TestMain(unittest.TestCase):
    """Test cases for main()."""

    def setUp(self) -> None:
        """Setup, gets run before each test. Use to configure test environment."""
        self._get_modified_files = utilities.get_modified_files
        utilities.get_modified_files = mock.Mock(auto_spec=True, return_value=[])

        self._get_untracked_files = utilities.get_untracked_files
        utilities.get_untracked_files = mock.Mock(auto_spec=True, return_value=[])

        self._get_staged_files = utilities.get_staged_files
        utilities.get_staged_files = mock.Mock(auto_spec=True, return_value=[])

        self._get_current_branch = utilities.get_current_branch
        utilities.get_current_branch = mock.Mock(auto_spec=True)

        self._run_command= utilities.run_command
        utilities.run_command = mock.Mock(auto_spec=True)

        self._run_test = run_test.main
        run_test.main = mock.Mock(auto_spec=True)

        self.args = mock.Mock(auto_spec=True)
        self.args.branch = 'some_branch'
        self.args.dry_run = False

        self._process_args = push_to_remote._process_args
        push_to_remote._process_args = mock.Mock(auto_spec=True, return_value=self.args)


    def tearDown(self) -> None:
        """Teardown, run after each test. Use to reset test environment."""
        utilities.get_current_branch = self._get_current_branch
        utilities.get_staged_files = self._get_staged_files
        utilities.get_untracked_files = self._get_untracked_files
        utilities.get_modified_files = self._get_modified_files
        utilities.run_command = self._run_command
        run_test.main = self._run_test

        push_to_remote._process_args = self._process_args
        self.args.reset_mock()
    

    def test_dry_run(self) -> None:
        """Test for main() dry run."""
        self.args.dry_run = True
        push_to_remote.main(self.args)
        utilities.run_command.assert_not_called()
        run_test.main.assert_not_called()

    
    def test_main_clean(self) -> None:
        """Test for main() with clean worktree."""
        push_to_remote.main(self.args)
        utilities.run_command.assert_called_once()


    def test_with_branch_name_main(self) -> None:
        """Test for main() with branch name == 'main'."""
        self.args.branch = 'main'
        push_to_remote.main(self.args)
        utilities.run_command.assert_not_called()


    @mock.patch('utilities.get_modified_files', mock.Mock(auto_spec=True, return_value=['some/file.py']))
    def test_main_dirty(self) -> None:
        """Test for main() with dirty worktree."""
        with self.assertRaises(push_to_remote.DirtyWorktreeError):
            push_to_remote.main(self.args)
        utilities.run_command.assert_not_called()


