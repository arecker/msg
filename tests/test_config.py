from unittest import TestCase
import os

from msg.config import parse
from utils import get_root


class TestConfig(TestCase):
    '''
    exercises functions in the config module
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
        self.assertEqual(parse(data=self.mock), self.expected)

    def test_parse_file(self):
        '''
        should return a data object from a yaml file
        '''
        try:
            target = os.path.join(get_root(), 'test_config.yml')
            with open(target, 'w+') as file:
                file.write(self.mock)

            actual = parse(path=target)
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
        self.assertEqual(parse(), {})
