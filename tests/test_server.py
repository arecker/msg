from unittest import TestCase

from fabric import api

from mocks import MockFabricTestCase
from msg.server import Accessor


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


class TestAccessorCommands(MockFabricTestCase):
    '''
    exercises command pass through to
    fabric using mock fabric api
    '''
    def test_run(self):
        Accessor.run('echo hello')
        self.assertEqual(self.mock.last, {
            'command': 'echo hello',
            'sudo': False
        })

    def test_sudo(self):
        Accessor.sudo('echo boo')
        self.assertEqual(self.mock.last, {
            'command': 'echo boo',
            'sudo': True
        })

    def test_append(self):
        Accessor.append('test.txt', 'hello there', False)
        self.assertEqual(self.mock.last, {
            'file': 'test.txt',
            'append': 'hello there',
            'sudo': False
        })

    def test_put(self):
        Accessor.put('source file', 'destination file', False)
        self.assertEqual(self.mock.last, {
            'put': 'source file',
            'destination': 'destination file',
            'sudo': False
        })
