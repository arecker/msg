from mocks import MockFabricTestCase
from msg import db


class TestBaseDatabaseController(MockFabricTestCase):
    def test_run_command_without_user(self):
        try:
            d = db.BaseDatabaseController()
            d._run_command('select * from something')
            self.fail('able to run an incomplete controller')
        except NotImplementedError as e:
            self.assertEqual(e.message, '\'user\' required')


class PostgresDatabaseController(MockFabricTestCase):
    def test_run_command_without_user(self):
        d = db.PostgresController()
        d._run_command('drop everything')
        self.assertEqual(self.mock.last, {
            'command': 'drop everything',
            'sudo': True,
            'user': 'postgres'
        })
