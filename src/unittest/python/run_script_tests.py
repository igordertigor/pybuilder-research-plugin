import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import os


import pybuilder_research_plugin as plugin


class TestCopyEnv(unittest.TestCase):

    def setUp(self):
        self.original_env = {'SOME_VAR': 'value'}

    def test_should_create_copy(self):
        with mock.patch('os.environ', self.original_env):
            modified_env = plugin.copy_env('ANY_DIRECTORY')
        modified_env['SOME_VAR'] = 'other value'
        self.assertEqual(self.original_env['SOME_VAR'], 'value')

    def test_should_add_pythonpath(self):
        with mock.patch('os.environ', self.original_env):
            modified_env = plugin.copy_env('ANY_DIRECTORY')

        self.assertDictEqual(modified_env,
                             {'SOME_VAR': 'value',
                              'PYTHONPATH': 'ANY_DIRECTORY'})

    def test_should_extend_pythonpath_if_set(self):
        self.original_env['PYTHONPATH'] = 'SOME_DIRECTORY'
        with mock.patch('os.environ', self.original_env):
            modified_env = plugin.copy_env('ANY_DIRECTORY')

        expected_pythonpath = ('SOME_DIRECTORY{}ANY_DIRECTORY'
                               .format(os.pathsep))
        self.assertDictEqual(modified_env,
                             {'SOME_VAR': 'value',
                              'PYTHONPATH': expected_pythonpath})


class TestRunScript(unittest.TestCase):

    def setUp(self):
        self.project = mock.Mock()
        self.project.get_property.return_value = 'ANY_SCRIPTS_DIR'
        self.project.expand_path.return_value = 'ANY_PACKAGE_DIR'
        self.logger = mock.Mock()

        self.patch_executable = mock.patch('sys.executable',
                                           'ANY_PYTHON_EXECUTABLE')
        self.patch_getenv = mock.patch('os.getenv')
        self.patches_plugin = mock.patch.multiple(
            'pybuilder_research_plugin',
            copy_env=mock.DEFAULT,
            execute_command=mock.DEFAULT)

        self.patch_executable.start()
        self.mock_getenv = self.patch_getenv.start()
        mock_plugin = self.patches_plugin.start()
        self.mock_copy_env = mock_plugin['copy_env']
        self.mock_exec_command = mock_plugin['execute_command']

    def tearDown(self):
        mock.patch.stopall()

    def test_should_execute_command_in_correct_env(self):
        self.mock_copy_env.return_value = 'ANY_ENVIRONMENT'
        self.mock_getenv.return_value = 'ANY_SCRIPT'
        self.mock_exec_command.return_value = 0
        plugin.run_script(self.project, self.logger)

        self.mock_exec_command.assert_called_once_with(
            'ANY_PYTHON_EXECUTABLE ANY_PACKAGE_DIR/ANY_SCRIPTS_DIR/ANY_SCRIPT',
            env='ANY_ENVIRONMENT',
            shell=True)

    def test_should_raise_if_script_fails(self):
        self.mock_copy_env.return_value = 'ANY_ENVIRONMENT'
        self.mock_getenv.return_value = 'ANY_SCRIPT'
        self.mock_exec_command.return_value = 1
        with self.assertRaises(plugin.PybResearchException):
            plugin.run_script(self.project, self.logger)

        self.mock_exec_command.assert_called_once_with(
            'ANY_PYTHON_EXECUTABLE ANY_PACKAGE_DIR/ANY_SCRIPTS_DIR/ANY_SCRIPT',
            env='ANY_ENVIRONMENT',
            shell=True)

    def test_should_raise_if_no_script_set(self):
        self.mock_copy_env.return_value = 'ANY_ENVIRONMENT'
        self.mock_getenv.return_value = ''
        with self.assertRaises(plugin.PybResearchException):
            plugin.run_script(self.project, self.logger)

        self.mock_exec_command.assert_not_called()
