from unittest import TestCase
from types import ModuleType


class TestSanity(TestCase):
    def test_import(self):
        import msg
        self.assertIsInstance(msg, ModuleType)
