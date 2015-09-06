from unittest import TestCase
from runpy import run_module

from click.testing import CliRunner

from msg.cli import main, prod, stage


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
