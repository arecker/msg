class MockFiles(object):
    '''
    mock fabric files object
    has to be seperate because it is in
    a different module
    '''
    def __init__(self, callback):
        self.callback = callback

    def append(self, filename, text, sudo):
        self.callback({
            'file': filename,
            'append': text,
            'sudo': sudo
        })


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
        self._files = MockFiles(self._files_command)

    def sudo(self, cmd):
        self._shell_command(cmd, True)

    def run(self, cmd):
        self._shell_command(cmd, False)

    def _files_command(self, obj):
        self.history.append(obj)
        self.last = obj

    def _shell_command(self, cmd, sudo):
        self.last = {
            'command': cmd,
            'sudo': sudo
        }
        self.history.append(self.last)
