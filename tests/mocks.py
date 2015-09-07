from unittest import TestCase
import os

from click.testing import CliRunner

from msg import server
from msg.cli import main
from msg.server import api


class MockFiles(object):
    '''
    mock fabric files object
    has to be seperate because it is in
    a different module
    '''
    def __init__(self, callback):
        self.callback = callback

    def append(self, filename, text, sudo):
        self.callback({
            'file': filename,
            'append': text,
            'sudo': sudo
        })


class MockFabric(object):
    '''
    mock fabric commands
    modified to view what shell commands
    would have run
    '''
    def __init__(self):
        self.history = []
        self.last = {}
        self.env = {}
        self._files = MockFiles(self._files_command)

    def sudo(self, cmd):
        self._shell_command(cmd, True)

    def run(self, cmd):
        self._shell_command(cmd, False)

    def _files_command(self, obj):
        self.history.append(obj)
        self.last = obj

    def _shell_command(self, cmd, sudo):
        self.last = {
            'command': cmd,
            'sudo': sudo
        }
        self.history.append(self.last)


class MockFabricTestCase(TestCase):
    '''
    Custom test case suite that mocks
    out fabric, creates configs, and supplies test click
    cli runners
    '''
    def setUp(self):
        self.cli = CliRunner()
        server.api = self.mock = MockFabric()
        server.files = self.mock._files
        if getattr(self, 'config_data', None):
            self._write_config()

    def tearDown(self):
        server.api = api
        if getattr(self, 'config', None):
            self._destroy_config()

    def _write_config(self):
        root = os.path.dirname(os.path.realpath(__file__))
        self.config = os.path.join(root, 'test_config.yml')
        with open(self.config, 'w+') as file:
            file.write(self.config_data)

    def _destroy_config(self):
        try:
            os.remove(self.config)
        except OSError:
            pass

    def cli_prod(self):
        self._invoke_and_compare('prod')

    def cli_stage(self):
        self._invoke_and_compare('stage')

    def _invoke_and_compare(self, env):
        self.cli.invoke(main, [env, self.config])
        self.assertEqual(self.mock.history, self.expected)
