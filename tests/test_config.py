from msg.config import Kicker
from msg import exceptions
from mocks import MockFabricTestCase


class TestKicker(MockFabricTestCase):
    '''
    exercises the kicker object
    '''
    mock_data = '''
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
        self.assertEqual(Kicker(data=self.mock_data).data, self.expected)

    def test_parse_nothing(self):
        '''
        should thrown an exception if
        given nothing to parse
        '''
        with self.assertRaises(exceptions.MSGConfigParseException):
            Kicker()
