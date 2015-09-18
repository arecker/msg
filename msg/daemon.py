from server import Accessor


class BaseDaemonController(object):
    def __init__(self):
        self.sudo = Accessor.sudo

    def _run_command(self, command, service):
        if not getattr(self, 'syntax', None):
            raise NotImplementedError('Daemon requires \'syntax\'')

        self.sudo(self.syntax.format(command=command, service=service))
        return self

    def restart(self, service):
        return self._run_command('restart', service)

    def reload(self, service):
        return self._run_command('reload', service)

    def stop(self, service):
        return self._run_command('stop', service)


class SystemDController(BaseDaemonController):
    syntax = 'systemctl {command} {service}'


class UpstartController(BaseDaemonController):
    syntax = 'service {service} {command}'
