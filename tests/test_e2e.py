from unittest import TestCase
import os

from click.testing import CliRunner

from msg.cli import main
from msg import server
from msg.server import api
from msg import exceptions
from mocks import MockFabric
from utils import get_root


class MockMSGTestCase(TestCase):
    '''
    writes out config file and removes it
    '''
    def setUp(self):
        self.cli = CliRunner()
        server.api = self.mock = MockFabric()
        self.config = os.path.join(get_root(), 'test_config.yml')
        with open(self.config, 'w+') as file:
            file.write(self.config_data)

    def tearDown(self):
        server.api = api
        try:
            os.remove(self.config)
        except OSError:
            pass


class TestHandShakeInstallerConfig(MockMSGTestCase):
    config_data = '''
host:
  prod: 'prod-host'
  stage: 'stage-host'

servos:
  - handshake
  - install:
      packages:
        - python
        - python-pip
'''

    def test_it(self):
        self.cli.invoke(main, ['prod', self.config])
        self.assertEqual(self.mock.command_history, [
            'echo "Hellooooooo nurse"',
            'sudo apt-get install -y python python-pip'
        ])


class TestHandShakeInstallerConfigOverrides(MockMSGTestCase):
    config_data = '''
host:
  prod: 'test-server'
  stage: 'stage-server'

servos:
  - handshake:
      hello: 'I am overriding the default message'
  - install:
      command: sudo pacman -S
      packages:
        - python
        - python-pip
        - mysql
'''

    def test_it(self):
        self.cli.invoke(main, ['stage', self.config])
        self.assertEqual(self.mock.command_history, [
            'echo "I am overriding the default message"',
            'sudo pacman -S python python-pip mysql'
        ])


class TestInstallerMissingReqs(MockMSGTestCase):
    config_data = '''
host:
  prod: 'prod-host'
  stage: 'stage-host'

servos:
  - handshake
  - install
'''

    def test_it(self):
        try:
            self.cli.invoke(main, ['stage', self.config])
        except exceptions.MSGException as e:
            self.assertEqual(len(e.errors), 1)
            self.assertEqual(e.errors[0].fields, ['packages'])
