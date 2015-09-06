import yaml

from . import exceptions
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
            else:
                with open(path) as file:
                    self.data = yaml.load(file)
        except:
            raise exceptions.MSGConfigParseException

    def validate(self, host_string):
        try:
            Accessor.host(self.data['host'][host_string])
        except:
            raise exceptions.MSGMissingHostException(host_string)

        # Validate servos
        errors = []
        servos = self.data.get('servos', None)
        if not servos or len(servos) < 1:
            raise exceptions.MSGNoServosException

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
            except exceptions.ServoException as e:
                errors.append(e)

        if len(errors) > 0:
            raise exceptions.MSGErrorListException(errors)

        return self

    def go(self):
        '''
        let 'er rip
        '''
        for item in self.servos:
            item.go()
