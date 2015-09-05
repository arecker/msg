from copy import deepcopy

from server import Accessor
from exceptions import ServoConfigException


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

    def go(self):
        raise NotImplementedError('servo requires a \'go\' routine')

    def validate(self):
        '''
        ensures all required items are in the config
        '''
        if not getattr(self, 'required', None):
            return self
        missing = [x for x in self.required if not self.config.get(x, None)]
        if not missing:
            return self
        raise ServoConfigException(
            message='missing config items', missing=missing)


class HandShake(BaseServo):
    '''
    servo that echos a message through the host
    '''
    defaults = {
        'message': 'Hellooooooo nurse'
    }

    def go(self):
        self.run('echo "{message}"'.format(message=self.config['message']))
