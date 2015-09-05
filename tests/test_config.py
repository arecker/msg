from unittest import TestCase
import os

from msg.config import Kicker
from msg.exceptions import ServoConfigException
from utils import get_root


class TestKicker(TestCase):
    '''
    exercises the kicker object
    '''
    mock = '''
test: this is a test attribute
collection:
  - first
  - second
  - third
subitems:
  item1: 1
  item2: 2
  item3: true'''
    expected = {
        'test': 'this is a test attribute',
        'collection': [
            'first',
            'second',
            'third'
        ],
        'subitems': {
            'item1': 1,
            'item2': 2,
            'item3': True
        }
    }

    def test_parse_data(self):
        '''
        should return a data object from a yaml string
        '''
        self.assertEqual(Kicker(data=self.mock).data, self.expected)

    def test_parse_file(self):
        '''
        should return a data object from a yaml file
        '''
        try:
            target = os.path.join(get_root(), 'test_config.yml')
            with open(target, 'w+') as file:
                file.write(self.mock)

            actual = Kicker(path=target).data
            self.assertEqual(actual, self.expected)
        finally:
            try:
                os.remove(target)
            except OSError:
                pass

    def test_parse_nothing(self):
        '''
        should just return an empty dict if
        given nothing to parse
        '''
        with self.assertRaises(ServoConfigException):
            Kicker()
