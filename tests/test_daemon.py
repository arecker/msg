from mocks import MockFabricTestCase
from msg import daemon


class TestBaseDaemonController(MockFabricTestCase):
    def test_run_command_without_syntax(self):
        try:
            d = daemon.BaseDaemonController()
            d._run_command('restart', 'nginx')
            self.fail('able to run an incomplete controller')
        except NotImplementedError as e:
            self.assertEqual(e.message, 'Daemon requires \'syntax\'')


class DaemonControllerTestCase(MockFabricTestCase):
    def go(self):
        self.dc.restart('mysql')
        self.dc.reload('nginx')
        self.dc.stop('sshd')

        self.assertEqual(self.mock.history, [{
            'command': self.formatstring.format(
                command='restart', service='mysql'),
            'sudo': True
        }, {
            'command': self.formatstring.format(
                command='reload', service='nginx'),
            'sudo': True
        }, {
            'command': self.formatstring.format(
                command='stop', service='sshd'),
            'sudo': True
        }])


class SystemDControllerTestCase(DaemonControllerTestCase):
    def test(self):
        self.dc = daemon.SystemDController()
        self.formatstring = 'systemctl {command} {service}'
        self.go()


class UpstartControllerTestCase(DaemonControllerTestCase):
    def test(self):
        self.dc = daemon.UpstartController()
        self.formatstring = 'service {service} {command}'
        self.go()
