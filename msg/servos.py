from copy import deepcopy

from server import Accessor
from exceptions import ServoMissingFieldsException


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
        self.append = Accessor.append

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
        '''
        handle for the main servo routine
        '''
        raise NotImplementedError('servo requires a \'go\' routine')

    def nuke(self):
        '''
        handle for the routine that completely removes
        anything done by the servo
        '''
        raise NotImplementedError('servo requires a \'nuke\' routine')

    def validate(self):
        '''
        ensures all required items are in the config
        '''
        if not getattr(self, 'required', None):
            return self
        missing = [x for x in self.required if not self.config.get(x, None)]
        if len(missing) < 1:
            return self
        raise ServoMissingFieldsException(missing)


class HandShake(BaseServo):
    '''
    servo that echos a message through the host
    '''
    defaults = {
        'hello': 'Hellooooooo nurse',
        'goodbye': 'You ever see a podrace?'
    }

    def _run_message(self, message):
        self.run('echo "{message}"'.format(message=message))

    def go(self):
        self._run_message(self.config['hello'])

    def nuke(self):
        self._run_message(self.config['goodbye'])


class Installer(BaseServo):
    '''
    servo that installs a list of packages
    '''
    required = [
        'packages',
    ]
    defaults = {
        'command': 'apt-get install -y',
    }

    def go(self):
        self.sudo('{command} {packages}'.format(
            command=self.config['command'],
            packages=' '.join(self.config['packages'])
        ))


class Host(BaseServo):
    '''
    servo that manipulates the host file
    '''
    def __init__(self, data):
        super(Host, self).__init__(data)
        self.to_host = lambda x, y: '{0}     {1}'.format(x, y)
        self.short = not isinstance(self.config, dict)

    def validate(self):
        '''
        overrides base since there is a simple and complicated
        version of the config
        '''
        if self.short:
            if len(self.config) < 1:
                raise ServoMissingFieldsException(fields=['host'])
        else:
            raise NotImplementedError('only short mode available')
        return self

    def go(self):
        if self.short:
            self._short_go()

    def _short_go(self):
        self.append('/etc/hosts', self.to_host('127.0.0.1', self.config), True)


# key/class map
manifest = {
    'handshake': HandShake,
    'install': Installer,
    'host': Host
}
