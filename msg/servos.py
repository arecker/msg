from copy import deepcopy
import os
import ntpath

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
        self.put = Accessor.put
        self.template = Accessor.template

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
    required = ['packages']
    defaults = {'command': 'apt-get install -y'}

    def __init__(self, data):
        if not isinstance(data, dict):
            data = {'command': self.defaults['command'],
                    'packages': [data]}
        super(Installer, self).__init__(data)

    def go(self):
        packages = ' '.join(self.config['packages'])
        command = self.config['command']
        self.sudo('{0} {1}'.format(command, packages))


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
        return self

    def go(self):
        self.append('/etc/hosts', self.to_host('127.0.0.1', self.config), True)


class Put(BaseServo):
    '''
    servo that puts a payload on the server
    '''
    required = ['source', 'destination']

    def go(self):
        self.put(self.config['source'], self.config['destination'], False)


class Clone(BaseServo):
    '''
    servo that clones a git repo
    '''
    required = ['url', 'target']

    def go(self):
        url = self.config['url']
        target = self.config['target']
        self.run('git clone {0} {1}'.format(url, target))


class Untar(BaseServo):
    '''
    servo that untars a file to a location
    '''
    required = ['source', 'destination']

    def go(self):
        source = self.config['source']
        dest = self.config['destination']
        self.run('tar xvf {0} -C {1}'.format(source, dest))


class Unzip(BaseServo):
    '''
    servo that unzips a ZIP
    '''
    required = ['source', 'destination']

    def go(self):
        source = self.config['source']
        dest = self.config['destination']
        self.run('unzip {0} -d {1}'.format(source, dest))


class Remove(BaseServo):
    '''
    servo that deletes a file
    '''
    required = ['target']

    def go(self):
        self.run('rm {0}'.format(self.config['target']))


class Symlink(BaseServo):
    '''
    servo that creates a symlink
    '''
    required = ['source', 'destination']
    defaults = {
        'soft': True,
        'sudo': False
    }

    def go(self):
        source = self.config['source']
        dest = self.config['destination']

        if self.config['soft']:
            command = 'ln -s {0} {1}'.format(source, dest)
        else:
            command = 'ln {0} {1}'.format(source, dest)

        if self.config['sudo']:
            return self.sudo(command)
        return self.run(command)


class Render(BaseServo):
    '''
    servo that renders data through a
    jinja template
    '''
    required = ['name', 'destination', 'data']
    defaults = {'sudo': False}

    def go(self):
        return self.template(
            self.config['name'],
            self.config['destination'],
            self.config['data'],
            sudo=self.config['sudo']
        )


class Payload(BaseServo):
    '''
    servo that puts a payload on the server.
    Depending on its file extension, it will
    open it and remove the package.
    '''
    required = ['payload', 'destination']
    defaults = {'temp': '/tmp'}
    extensions = {
        '.tar': Untar,
        '.gz': Untar,
        '.zip': Unzip
    }

    def validate(self):
        super(Payload, self).validate()
        ext = os.path.splitext(self.config['payload'])[1]
        self.undresser = self.extensions.get(ext, None)
        if not self.undresser:
            raise ServoMissingFieldsException(fields=['payload'])
        return self

    def go(self):
        local_payload = self.config['payload']
        payload_filename = ntpath.basename(local_payload)
        destination = self.config['destination']
        temp = self.config['temp']
        remote_payload = (os.path.join(temp, payload_filename))

        Put({
            'source': local_payload,
            'destination': temp
        }).go()

        self.undresser({
            'source': remote_payload,
            'destination': destination
        }).go()

        Remove({'target': remote_payload}).go()


# key/class map
manifest = {
    'handshake': HandShake,
    'install': Installer,
    'host': Host,
    'put': Put,
    'clone': Clone,
    'untar': Untar,
    'unzip': Unzip,
    'remove': Remove,
    'payload': Payload
}
