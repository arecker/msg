class MockFabric(object):
    '''
    mock fabric commands
    modified to view what shell commands
    would have run
    '''
    def __init__(self):
        self.history = []
        self.last = {}
        self.env = {}

    def sudo(self, cmd):
        self._shell_command(cmd, True)

    def run(self, cmd):
        self._shell_command(cmd, False)

    def _shell_command(self, cmd, sudo):
        self.last = {
            'command': cmd,
            'sudo': sudo
        }
        self.history.append(self.last)
