from unittest import TestCase
from runpy import run_module

from click.testing import CliRunner

from msg.cli import main, prod, stage
from mocks import MockFabricTestCase


class TestCliSanity(TestCase):
    '''
    tests basic app cli interaction
    '''
    def setUp(self):
        self.runner = CliRunner()

    def test_main(self):
        result = self.runner.invoke(main)
        self.assertEqual(result.exit_code, 0)

    def test_prod(self):
        result = self.runner.invoke(prod)
        self.assertEqual(result.exit_code, 2)

    def test_stage(self):
        result = self.runner.invoke(stage)
        self.assertEqual(result.exit_code, 2)

    def test_module(self):
        result = run_module('msg.cli')
        self.assertIsInstance(result, dict)


class TestMissingHost(MockFabricTestCase):
    config_data = '''
host:
  stage: hello
'''

    def test(self):
        result = self.prod()
        self.assertEqual(result.exit_code, 1)


class TestInvalidYaml(MockFabricTestCase):
    config_data = '''
    This is definitely not yaml.
At least hopefully not.
Let me add some garbage text to make sure.

lkajsdflkjasdf08as0d9f8a09sdf0a9423*)(S*)(ADF
- asdfa4r: faw09rsdf : w9i4
 '''

    def test(self):
        result = self.prod()
        self.assertEqual(result.exit_code, 1)


class TestNoServos1(MockFabricTestCase):
    config_data = '''
host:
  stage: hello
  prod: woop
'''

    def test(self):
        result = self.prod()
        self.assertEqual(result.exit_code, 1)


class TestNoServos2(MockFabricTestCase):
    config_data = '''
host:
  stage: hello
  prod: woop

servos:
'''

    def test(self):
        result = self.prod()
        self.assertEqual(result.exit_code, 1)
