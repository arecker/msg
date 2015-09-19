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

    def upload_template(self, template, destination, **kwargs):
        self.callback({
            'template': template,
            'destination': destination,
            'data': kwargs['context'],
            'sudo': kwargs['use_sudo']
        })


class MockOperations(object):
    '''
    mock fabric.opterations
    '''
    def __init__(self, callback):
        self.callback = callback

    def put(self, source, destination, sudo):
        self.callback({
            'put': source,
            'destination': destination,
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
        self._files = MockFiles(self._callback)
        self._operations = MockOperations(self._callback)

    def sudo(self, cmd, user=None):
        self._shell_command(cmd, True, user=user)

    def run(self, cmd):
        self._shell_command(cmd, False)

    def _callback(self, obj):
        self.history.append(obj)
        self.last = obj

    def _shell_command(self, cmd, sudo, user=None):
        self.last = {
            'command': cmd,
            'sudo': sudo
        }
        if user:
            self.last['user'] = user
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
        server.operations = self.mock._operations
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

    def prod(self):
        return self._invoke('prod')

    def stage(self):
        return self._invoke('stage')

    def _invoke(self, env):
        return self.cli.invoke(main, [env, self.config])

    def compare(self):
        self.assertEqual(self.mock.history, self.expected)
