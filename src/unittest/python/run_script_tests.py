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
