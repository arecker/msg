from server import Accessor


class BaseDatabaseController(object):
    def __init__(self):
        self.sudo = Accessor.sudo

    def _run_command(self, cmd):
        if not getattr(self, 'user', None):
            raise NotImplementedError('\'user\' required')
        return self.sudo(cmd, user=self.user)


class PostgresController(BaseDatabaseController):
    pass


class MysqlController(BaseDatabaseController):
    pass
