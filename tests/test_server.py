from unittest import TestCase

from fabric import api

from msg import server
from msg.server import Accessor


class MockFabric(object):
    def __init__(self):
        self.env = {
            'use_ssh_config': True
        }
        self.run = self._record
        self.sudo = self._record

    def _record(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs


class TestAccessorEnvironment(TestCase):
    '''
    tests persistance of the server
    accessor in setting the fabric
    environment
    '''
    def test_ssh_config(self):
        '''
        should set fabric to use
        ssh config
        '''
        self.assertEqual(api.env['use_ssh_config'], True)

    def test_set_host(self):
        '''
        should set fabric host
        '''
        test_host_name = 'my_test_host'
        Accessor.host(test_host_name)
        self.assertEqual(api.env['host_string'], test_host_name)

    def test_set_password(self):
        '''
        should set fabric password
        '''
        test_pass = 'monkey_balls'
        Accessor.password(test_pass)
        self.assertEqual(api.env['password'], test_pass)

    def test_password_host_chainable(self):
        '''
        should be chainable
        '''
        expected = {
            'pass': 'monkey_nuts',
            'host': 'your-mothers-house'
        }

        Accessor.password(expected['pass']) \
                .host(expected['host'])

        self.assertEqual(api.env['host_string'], expected['host'])
        self.assertEqual(api.env['password'], expected['pass'])


class TestAccessorCommands(TestCase):
    '''
    exercises command pass through to
    fabric using mock fabric api
    '''
    def setUp(self):
        server.api = self.mock = MockFabric()

    def tearDown(self):
        server.api = api

    def test_run(self):
        Accessor.host('localhost')
        Accessor.run('echo hello', timeout=5)
        self.assertEqual(''.join(self.mock._args), ''.join(self.mock._args))
        self.assertEqual(len(set(dict(timeout=5)) ^ set(self.mock._kwargs)), 0)

    def test_sudo(self):
        Accessor.host('test-host').password('testpass')
        Accessor.sudo('echo boo')
        self.assertEqual(''.join(self.mock._args), ''.join(self.mock._args))
        self.assertEqual(len(set(dict(
            use_ssh_config=True,
            password='testpass',
            host_string='test-host'
        )) ^ set(self.mock.env)), 0)
