from unittest import TestCase
import os

from msg import server
from msg.server import api
from msg.config import Kicker
from mocks import MockFabric
from utils import get_root


class MockMSGTestCase(TestCase):
    '''
    writes out config file and removes it
    '''
    def setUp(self):
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
  prod: 'prod-server'
  stage: 'stage-server'

servos:
  - handshake
  - install:
      packages:
        - python
        - python-pip
'''

    def test_it(self):
        Kicker(path=self.config).validate('prod').go()

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
        Kicker(path=self.config).validate('prod').go()

        self.assertEqual(self.mock.command_history, [
            'echo "I am overriding the default message"',
            'sudo pacman -S python python-pip mysql'
        ])
