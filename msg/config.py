import yaml

from exceptions import ServoConfigException
from server import Accessor
from servos import manifest


class Kicker(object):
    '''
    Class that reads a config in and kicks off the whole process
    '''
    def __init__(self, path=None, data=None):
        '''
        parses a yaml formatted config
        either from a file path or
        passed data
        '''
        try:
            if data:
                self.data = yaml.load(data)
            elif path:
                with open(path) as file:
                    self.data = yaml.load(file)
            else:
                raise
        except:
            raise ServoConfigException('had an issue reading the config')

    def validate(self, host_string):

        # Check host
        try:
            host = self.data['host'][host_string]
        except:
            raise ServoConfigException(
                'could not figure out host', host=host_string)
        Accessor.host(host)

        # Validate servos
        errors = []
        servos = self.data.get('servos', None)
        if not servos or len(servos) < 1:
            raise ServoConfigException('no servos listed')

        self.servos = []
        for item in servos:
            try:
                for k, v in item.iteritems():
                    self.servos.append(manifest[k](v))
            except AttributeError:  # no associated data
                self.servos.append(manifest[item]())

        for obj in self.servos:
            try:
                obj.validate()
            except ServoConfigException as e:
                errors.append(e)

        if len(errors) > 0:
            print('There are {0} problems'.format(len(errors)))

        return self

    def go(self):
        '''
        let 'er rip
        '''
        for item in self.servos:
            item.go()
