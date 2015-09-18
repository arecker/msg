from msg.config import Kicker
from msg import exceptions
from mocks import MockFabricTestCase


class TestKicker(MockFabricTestCase):
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
        self.assertEqual(Kicker(data=self.mock_data).data, self.expected)

    def test_parse_nothing(self):
        with self.assertRaises(exceptions.MSGConfigParseException):
            Kicker()
