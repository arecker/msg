from unittest import TestCase

from msg.server import Accessor
from msg.servos import BaseServo


class TestBaseServo(TestCase):
    '''
    exercises base servo class
    '''
    def test_init_accessor_passes(self):
        '''
        should pass through to accessor api
        '''
        obj = BaseServo()
        self.assertEqual(obj.run, Accessor.run)
        self.assertEqual(obj.sudo, Accessor.sudo)

    def test_init_data_dict(self):
        '''
        should save off data, or default to an empty
        dict if none given
        '''
        obj = BaseServo()
        self.assertEqual(obj.config, {})
        expected = {
            'one': 1,
            'two': True,
            'three': 'hello'
        }
        obj = BaseServo(expected)
        self.assertEqual(obj.config, expected)

    def test_defaults_loaded_in_config(self):
        '''
        should load the config object with
        specified defaults
        '''
        class MockServo(BaseServo):
            defaults = {
                'one': 1,
                'two': 2,
                'three': 3
            }

        mock = {
            'one': 'ONE',
            'three': 3,
            'extra': 'wooh!'
        }

        expected = {
            'one': 'ONE',
            'two': 2,
            'three': 3,
            'extra': 'wooh!'
        }

        obj = MockServo(mock)
        self.assertEqual(obj.config, expected)
