class MockFabric(object):
    '''
    mock fabric commands
    modified to view what shell commands
    would have run
    '''
    def __init__(self):
        self.env = {
            'use_ssh_config': True
        }
        self.run = self._record
        self.sudo = self._record

    def _record(self, *args, **kwargs):
        self.last_command = ''.join(args)
        self.last_kwargs = kwargs
