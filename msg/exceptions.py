class MSGException(Exception):
    def __init__(self, *args, **kwargs):
        super(MSGException, self).__init__(args, kwargs)

    def report(self):
        print(self.message)
        exit(1)


class MSGConfigParseException(MSGException):
    message = '''There was an error parsing the config file.
Are you sure that's valid yaml?'''


class MSGMissingHostException(MSGException):
    def __init__(self, tried_host):
        super(MSGMissingHostException, self).__init__()
        self.host = tried_host

    def report(self):
        print('Could not find host "{0}" in config'.format(self.host))
        exit(1)


class MSGNoServosException(MSGException):
    message = 'No servos listed in config.  Nothing to do.'


class MSGErrorListException(MSGException):
    message = '''There were some problems with how things were set up:'''

    def __init__(self, errors):
        super(MSGException, self).__init__()
        self.errors = errors

    def report(self):
        print(self.message)
        for e in self.errors:
            e.report()
        exit(1)


class ServoException(MSGException):
    pass


class ServoMissingFieldsException(ServoException):
    def __init__(self, fields):
        super(ServoException, self).__init__()
        self.fields = fields

    def report(self):
        print('missing the following config items: {fields}'.format(
            fields=', '.join(self.fields)
        ))
