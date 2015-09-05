from unittest import TestCase

from fabric.api import env
from fabric.exceptions import NetworkError

from msg.server import Accessor


class TestAccessor(TestCase):
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
        self.assertEqual(env['use_ssh_config'], True)

    def test_set_host(self):
        '''
        should set fabric host
        '''
        test_host_name = 'my_test_host'
        Accessor.host(test_host_name)
        self.assertEqual(env['host_string'], test_host_name)

    def test_set_password(self):
        '''
        should set fabric password
        '''
        test_pass = 'monkey_balls'
        Accessor.password(test_pass)
        self.assertEqual(env['password'], test_pass)

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

        self.assertEqual(env['host_string'], expected['host'])
        self.assertEqual(env['password'], expected['pass'])

    def test_run(self):
        try:
            passed = True
            Accessor.host('localhost')
            Accessor.run('echo hello', timeout=5)
        except NetworkError:
            pass
        except:
            passed = False
        self.assertTrue(passed)

    def test_sudo(self):
        try:
            passed = True
            Accessor.host('localhost')
            Accessor.sudo('echo hello', timeout=5)
        except NetworkError:
            pass
        except:
            passed = False
        self.assertTrue(passed)
