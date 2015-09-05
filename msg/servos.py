from copy import deepcopy

from server import Accessor


class BaseServo(object):
    '''
    base object for a servo
    constructed with a dictionary
    '''
    def __init__(self, data={}):
        # Save off config data
        self.config = self._build_config(data)

        # Pass through to accessor api
        self.run = Accessor.run
        self.sudo = Accessor.sudo

    def _build_config(self, data):
        '''
        combines the passed data with the servo
        defaults to make a config dict
        '''
        if not getattr(self, 'defaults', None):
            return data

        new = deepcopy(self.defaults)

        for k, v in data.iteritems():
            new[k] = v

        return new
