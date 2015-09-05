from unittest import TestCase
from types import ModuleType


class TestSanity(TestCase):
    def test_import(self):
        '''
        should import package
        '''
        import msg
        self.assertIsInstance(msg, ModuleType)
